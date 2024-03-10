import numpy as np
import cv2
import os
import glob
import sys
import pyrealsense2 as rs
import json

# RealSense camera setup
pipeline = rs.pipeline()
config = rs.config()

# Turn off the laser projector and set color stream to maximum resolution
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)  # Set color resolution to maximum
profile = pipeline.start(config)
depth_sensor = profile.get_device().first_depth_sensor()
depth_sensor.set_option(rs.option.laser_power, 0)
# カラー露光時間を設定
color_sensor = profile.get_device().query_sensors()[1]
color_sensor.set_option(rs.option.exposure, 100)

# Function to get and save internal camera parameters in JSON file
def save_internal_parameters_to_json():
    intrinsics = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
    camera_matrix = [
        intrinsics.fx, 0, intrinsics.ppx,
        0, intrinsics.fy, intrinsics.ppy,
        0, 0, 1
    ]
    params = {
        "camera": {
        "P": camera_matrix,
        "distortion": intrinsics.coeffs,
        "width": intrinsics.width,
        "height": intrinsics.height
                  }
            }
    with open('camera_parameters.json', 'w') as file:
        json.dump(params, file, indent=4)

# Function to display image in full screen
def display_fullscreen(image_path):
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow("Image", 1366, 0)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    image = cv2.imread(image_path)
    cv2.imshow("Image", image)

# Save internal parameters as JSON
save_internal_parameters_to_json()
capture_count = 0
figure_images = sorted(glob.glob('./graycode_pattern/*.png'))
im_len = len(figure_images)
print(f"Found {im_len} images.")

# Wait for input in terminal
trial_count = input("Enter trial count: ")

for figure_image in figure_images:
    # Display figure image in full screen
    display_fullscreen(figure_image)

    cv2.waitKey(500)

    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    if not color_frame:
        continue

    # Convert images to numpy arrays
    color_image = np.asanyarray(color_frame.get_data())
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    # 中央を切り出す
    #gray_image = gray_image[300:, 400:1600]
    #cv2.imshow("RealSense", color_image)

    # Capture and save camera image
    capture_folder = f"./capture_{trial_count}"
    os.makedirs(capture_folder, exist_ok=True)
    cv2.imwrite(f"{capture_folder}/graycode_{capture_count:02}.png", gray_image)

    capture_count += 1

# Stop the pipeline and close all OpenCV windows
pipeline.stop()
cv2.destroyAllWindows()