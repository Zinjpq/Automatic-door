# Main.py

import cv2

import DetectChars
import DetectPlates
import library

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False


def main():
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Phát hiện và vẽ hộp bao quanh biển số xe
        frame, plate_images = library.detect_license_plate(frame)
        cv2.imshow('detection', frame)
        imgOriginalScene = cv2.imread(cap)

        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates
        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

        if len(listOfPossiblePlates) != 0:
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
            # suppose the plate with the most recognized chars (the first plate in sorted by string length descending
            # order) is the actual plate
            licPlate = listOfPossiblePlates[0]
            print(licPlate.strChars)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break


if __name__ == "__main__":
    main()
