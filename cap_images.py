import cv2
import os
import glob
import sys

# Camera setup
camera = cv2.VideoCapture(0)

# Check if camera opened successfully
if not camera.isOpened():
    print("Error: Could not open camera.")
    sys.exit()

# Function to display image in full screen
def display_fullscreen(image_path):
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow("Image", 1366, 0)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    image = cv2.imread(image_path)
    cv2.imshow("Image", image)

# Main loop
capture_count = 0
figure_images = sorted(glob.glob('graycode_pattern/*.png'))  # Assuming PNG format for figures
im_len = len(figure_images)
print(f"Found {im_len} images.")

# Wait for input in terminal
trial_count = input("Enter trial count: ")

for figure_image in figure_images:
    # Display camera image
    ret, frame = camera.read()
    if not ret:
        print("Error: Failed to capture image from camera.")
        break

    cv2.imshow("Camera", frame)

    # Display figure image in full screen
    display_fullscreen(figure_image)

    cv2.waitKey(100)

    

    # Capture and save camera image
    capture_folder = f"./capture_{trial_count}"
    os.makedirs(capture_folder, exist_ok=True)
    cv2.imwrite(f"{capture_folder}/graycode_{capture_count}.png", frame)

    capture_count += 1

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
