import cv2
import numpy as np
import random
import Main  # assuming Main contains necessary variables like showSteps, SCALAR_WHITE, SCALAR_RED
import Preprocess
import DetectChars
import DetectPlates


def detectPlatesInScene(imgOriginalScene):
    listOfPossiblePlates = []
    height, width, numChannels = imgOriginalScene.shape

    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if Main.showSteps:
        cv2.imshow("0", imgOriginalScene)

    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)

    if Main.showSteps:
        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)

    listOfPossibleCharsInScene = DetectPlates.findPossibleCharsInScene(imgThreshScene)

    if Main.showSteps:
        print(f"step 2 - len(listOfPossibleCharsInScene) = {len(listOfPossibleCharsInScene)}")

        imgContours = np.zeros((height, width, 3), np.uint8)
        contours = [possibleChar.contour for possibleChar in listOfPossibleCharsInScene]
        cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)
        cv2.imshow("2b", imgContours)

    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

    if Main.showSteps:
        print(f"step 3 - listOfListsOfMatchingCharsInScene.Count = {len(listOfListsOfMatchingCharsInScene)}")

        imgContours = np.zeros((height, width, 3), np.uint8)
        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            intRandomBlue, intRandomGreen, intRandomRed = random.randint(0, 255), random.randint(0,
                                                                                                 255), random.randint(0,
                                                                                                                      255)
            contours = [matchingChar.contour for matchingChar in listOfMatchingChars]
            cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
        cv2.imshow("3", imgContours)

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
        possiblePlate = DetectPlates.extractPlate(imgOriginalScene, listOfMatchingChars)
        if possiblePlate.imgPlate is not None:
            listOfPossiblePlates.append(possiblePlate)

    print(f"\n{len(listOfPossiblePlates)} possible plates found")

    if Main.showSteps:
        for i, possiblePlate in enumerate(listOfPossiblePlates):
            p2fRectPoints = cv2.boxPoints(possiblePlate.rrLocationOfPlateInScene)
            for j in range(4):
                cv2.line(imgContours, tuple(p2fRectPoints[j]), tuple(p2fRectPoints[(j + 1) % 4]), Main.SCALAR_RED, 2)

            cv2.imshow("4a", imgContours)
            cv2.imshow("4b", possiblePlate.imgPlate)
            cv2.waitKey(0)

        print("\nplate detection complete, click on any image and press a key to begin char recognition.\n")
        cv2.waitKey(0)

    return listOfPossiblePlates


# Webcam Test using cv2.VideoCapture(0)
def testWithWebcam():
    cap = cv2.VideoCapture(0)  # Capture video from the default webcam

    if not cap.isOpened():
        print("Error: Unable to open the webcam.")
        return

    while True:
        ret, frame = cap.read()  # Read a frame from the webcam

        if not ret:
            print("Failed to grab frame.")
            break

        possiblePlates = detectPlatesInScene(frame)  # Process each frame for plate detection

        for plate in possiblePlates:
            cv2.imshow('Detected Plate', plate.imgPlate)  # Display each detected plate

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Run the test
testWithWebcam()
