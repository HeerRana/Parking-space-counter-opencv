import pickle
import cv2
import numpy as np
from utils import putTextRect  # Custom utility function for text with rectangle

# Define the width and height of a parking space rectangle
width, height = (107, 48)

# Load the saved parking space positions from a file
with open(file="car_park_pos", mode="rb") as file:
    positions_list = pickle.load(file)

# Load video file or webcam stream
webcam = cv2.VideoCapture("video.mp4")


# Checks each parking space and updates the visualization
def check_parking_space(processed_image):
    space_count = 0  # Counter for free parking spaces

    for pos in positions_list:
        x, y = pos
        # Crop the processed image to the size of the parking space
        cropped_image = processed_image[y : y + height, x : x + width]
        # Count non-zero pixels (occupied area)
        count = cv2.countNonZero(src=cropped_image)

        # Determine if parking space is free or occupied
        if count < 900:
            space_count += 1
            color = (0, 255, 0)  # Green for free space
            thickness = 5
        else:
            color = (0, 0, 255)  # Red for occupied space
            thickness = 2

        # Draw rectangle around the parking space
        cv2.rectangle(
            img=img,
            pt1=(x, y),
            pt2=(x + width, y + height),
            color=color,
            thickness=thickness,
        )

        # Display the pixel count on the rectangle
        putTextRect(
            img=img,
            text=str(count),
            pos=(x, y + height - 3),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=0.6,
            text_thickness=1,
            text_color=(255, 255, 255),
            rect_color=color,
            offset=0,
        )

    # Display total free spaces on the top-left of the image
    putTextRect(
        img=img,
        text=f"Free: {space_count}/{len(positions_list)}",
        pos=(100, 50),
        fontFace=cv2.FONT_HERSHEY_COMPLEX,
        fontScale=2,
        text_thickness=5,
        text_color=(255, 255, 255),
        rect_color=(0, 200, 0),
        offset=20,
    )


# Main loop
while True:
    # Reset video to start if we reach the end
    if webcam.get(propId=cv2.CAP_PROP_POS_FRAMES) == webcam.get(
        propId=cv2.CAP_PROP_FRAME_COUNT
    ):
        webcam.set(propId=cv2.CAP_PROP_POS_FRAMES, value=0)

    # Read frame from video
    _, img = webcam.read()

    # Preprocess the image for parking detection
    gray_image = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred_image = cv2.GaussianBlur(
        src=gray_image, ksize=(3, 3), sigmaX=1
    )  # Reduce noise
    thresholded_image = cv2.adaptiveThreshold(
        src=blurred_image,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=25,
        C=16,
    )
    median_filtered_image = cv2.medianBlur(
        src=thresholded_image, ksize=5
    )  # Remove small artifacts
    kernel = np.ones(shape=(3, 3), dtype=np.uint8)
    dilated_image = cv2.dilate(
        src=median_filtered_image, kernel=kernel, iterations=1
    )  # Highlight objects

    # Check parking spaces on the processed image
    check_parking_space(dilated_image)

    # Display the original frame with rectangles and counts
    cv2.imshow(winname="image", mat=img)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key to exit
        break
    elif key == ord("s"):  # 's' key to save an output
        cv2.imwrite(filename="output.png", img=img)

# Release resources
webcam.release()
cv2.destroyAllWindows()
