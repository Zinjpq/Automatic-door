import cv2
import os

# Define the path to the image
image_path = 'image/image2.jpg'

# Check if the image file exists
if not os.path.exists(image_path):
    print(f"Error: The file at {image_path} does not exist.")
else:
    # Load the image
    img = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if img is None:
        print(f"Error: Failed to load the image from {image_path}")
    else:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Load the license plate cascade
        plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

        # Detect plates
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        plate_images = []

        # Loop over detected plates
        for (x, y, w, h) in plates:
            # Draw rectangles around detected plates
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Crop and store the grayscale images of the plates
            cropped_plate = gray[y:y + h, x:x + w]
            plate_images.append(cropped_plate)

        # Convert each cropped plate from grayscale to BGR format (if needed)
        plate_images_bgr = [cv2.cvtColor(plate, cv2.COLOR_GRAY2BGR) for plate in plate_images]

        # Process the plate images (assuming Preprocess is a valid class in your code)
        # imgGrayscale, imgThresh = Preprocess.preprocess(plate_images_bgr)
