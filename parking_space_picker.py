import cv2
import pickle

# Try to load existing parking positions from file
try:
    with open(file="car_park_pos", mode="rb") as file:
        positions_list = pickle.load(file)
except:
    positions_list = []

# Dimensions of a single parking space rectangle
width, height = (107, 48)


# Handles adding or removing parking space positions with mouse clicks.
def mouse_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Left click to add a new parking space
        positions_list.append((x, y))

    # Right click to remove a parking space if clicked inside its rectangle
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positions_list):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                positions_list.pop(i)

    # Save updated positions to file
    with open(file="car_park_pos", mode="wb") as file:
        pickle.dump(obj=positions_list, file=file)


# Main loop to display parking lot and handle mouse events
while True:
    img = cv2.imread("image.png")

    # Draw rectangles for all parking spaces
    for pos in positions_list:
        cv2.rectangle(
            img=img,
            pt1=(pos[0], pos[1]),
            pt2=(pos[0] + width, pos[1] + height),
            color=(255, 0, 255),
            thickness=2,
        )

    # Display the parking lot
    cv2.imshow(winname="Parking Lot", mat=img)

    # Set mouse callback to handle clicks
    cv2.setMouseCallback(window_name="Parking Lot", on_mouse=mouse_click)

    key = cv2.waitKey(1)  # ESC key to exit
    if key == 27:
        break

cv2.destroyAllWindows()
