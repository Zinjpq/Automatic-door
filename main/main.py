# Main.py

import cv2

import Preprocess
import DetectChars
import library
import DetectPlates

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

###################################################################################################
def main():
    cap = cv2.VideoCapture(0)  # Mở camera mặc định của laptop
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)

    while True:
        ret, imgOriginalScene = cap.read()  # Đọc frame từ camera
        if not ret:
            break
        cv2.imshow('detection', imgOriginalScene)
        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates

        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        cv2.imshow("imgPlate", licPlate.imgPlate)           # show crop of plate and threshold of plate
        cv2.imshow("imgThresh", licPlate.imgThresh)

        print("\nlicense plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
        print("----------------------------------------")

        cv2.imshow("imgOriginalScene", imgOriginalScene)                # re-show scene image

        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)           # write image out to file




        key = cv2.waitKey(5)
        if key == ord('q'):  # Nhấn phím 'q' để thoát
            break


    cap.release()
    cv2.destroyAllWindows()
# end function

###################################################################################################
if __name__ == "__main__":
    main()
