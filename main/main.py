# Main.py

import cv2

import Preprocess
import DetectChars
import library

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

urlOriginal = 'http://192.168.1.100'
url_cam = urlOriginal + '/cam'

url_up = urlOriginal + '/up'
url_down = urlOriginal + '/down'
url_left = urlOriginal + '/left'
url_right = urlOriginal + '/right'


###################################################################################################
def main():
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()

    if not blnKNNTrainingSuccessful:
        print("\nerror: KNN traning was not successful\n")
        return
    # end if
    cv2.destroyAllWindows()

    imgOriginalScene = cv2.imread("image/image7.jpg")
    cv2.imshow("0", imgOriginalScene)

    imgDetected, plate_images = library.detect_license_plate(imgOriginalScene)

    for plate_image in plate_images:
        imgGrayscale, imgThresh = Preprocess.preprocess(imgOriginalScene)
        cv2.imshow("1a", imgGrayscale)
        cv2.imshow("1b", imgThresh)



    cv2.waitKey(0)					# hold windows open until user presses a key
    return
# end function

###################################################################################################
if __name__ == "__main__":
    main()
