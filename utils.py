import cv2
import numpy as np


# Ensure that each image in a row is colored (BGR format) and optionally labeled
def ensure_color(row, row_label=[]):
    colored_row = []
    # If the image is grayscale, convert it to BGR
    for i, image in enumerate(row):
        if len(image.shape) == 2:
            colored_image = cv2.cvtColor(src=image, code=cv2.COLOR_GRAY2BGR)
        else:
            colored_image = image

        # If labels are provided, draw them on top of the image
        if len(row_label) != 0:
            label = row_label[i]
            output_image = colored_image.copy()

            # Get text size for background rectangle
            (text_width, text_height), _ = cv2.getTextSize(
                text=label, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2
            )

            # Draw background rectangle for label
            cv2.rectangle(
                img=output_image,
                pt1=(0, 0),
                pt2=(30 + text_width, 20 + text_height),
                color=(255, 255, 255),
                thickness=cv2.FILLED,
            )

            # Put the label text on the image
            cv2.putText(
                img=output_image,
                text=label,
                org=(10, 30),
                fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=1,
                color=(230, 0, 255),
                thickness=2,
            )

            colored_row.append(output_image)

        else:
            colored_row.append(colored_image)

    return colored_row


# Resize all images in a row by a given scale factor
def resize_image(colored_row, scale):
    colored_resized_row = []
    for image in colored_row:
        resized_image = cv2.resize(src=image, dsize=None, fx=scale, fy=scale)
        colored_resized_row.append(resized_image)
    return colored_resized_row


# Stack multiple rows of images into one big image grid
def stackImages(rows, scale, labels=[]):
    colored_resized_rows = []
    for i, row in enumerate(rows):
        if len(labels) == 0:
            colored_row = ensure_color(row)
        else:
            colored_row = ensure_color(row, labels[i])
        colored_resized_row = resize_image(colored_row, scale)
        colored_resized_rows.append(colored_resized_row)

    # Horizontally stack each row
    horizontally_stacked_rows = []
    for colored_resized_row in colored_resized_rows:
        horizontally_stacked_row = np.hstack(tup=colored_resized_row)
        horizontally_stacked_rows.append(horizontally_stacked_row)

    # Vertically stack all rows into one final image
    vertically_stacked_image = np.vstack(tup=horizontally_stacked_rows)
    return vertically_stacked_image


# Draw only corner edges of a rectangle
def cornerRectangle(
    img, pt1, pt2, color, corner_length, corner_thickness, line_thickness=1
):
    x1, y1 = pt1
    x2, y2 = pt2

    # Draw full rectangle outline if thickness > 0
    if line_thickness > 0:
        cv2.rectangle(img=img, pt1=pt1, pt2=pt2, color=color, thickness=line_thickness)

    # Top Left corner
    cv2.line(
        img=img,
        pt1=(x1, y1),
        pt2=(x1 + corner_length, y1),
        color=color,
        thickness=corner_thickness,
    )
    cv2.line(
        img=img,
        pt1=(x1, y1),
        pt2=(x1, y1 + corner_length),
        color=color,
        thickness=corner_thickness,
    )

    # Top Right corner
    cv2.line(
        img=img,
        pt1=(x2, y1),
        pt2=(x2 - corner_length, y1),
        color=color,
        thickness=corner_thickness,
    )
    cv2.line(
        img=img,
        pt1=(x2, y1),
        pt2=(x2, y1 + corner_length),
        color=color,
        thickness=corner_thickness,
    )

    # Bottom Left corner
    cv2.line(
        img=img,
        pt1=(x1, y2),
        pt2=(x1 + corner_length, y2),
        color=color,
        thickness=corner_thickness,
    )
    cv2.line(
        img=img,
        pt1=(x1, y2),
        pt2=(x1, y2 - corner_length),
        color=color,
        thickness=corner_thickness,
    )

    # Bottom Right corner
    cv2.line(
        img=img,
        pt1=(x2, y2),
        pt2=(x2 - corner_length, y2),
        color=color,
        thickness=corner_thickness,
    )
    cv2.line(
        img=img,
        pt1=(x2, y2),
        pt2=(x2, y2 - corner_length),
        color=color,
        thickness=corner_thickness,
    )

    return img


# Overlay a transparent PNG onto a background image at a given position
def overlayPNG(background, foreground, position=(0, 0)):
    x, y = position
    foreground_height, foreground_width, _ = foreground.shape

    # Extract alpha channel and normalize
    alpha = foreground[:, :, 3] / 255
    rgb_foreground = foreground[:, :, :3]

    # Blend each color channel based on alpha
    for i in range(3):
        overlayed = (rgb_foreground[:, :, i] * alpha) + (
            background[y : y + foreground_height, x : x + foreground_width, i]
            * (1 - alpha)
        )
        background[y : y + foreground_height, x : x + foreground_width, i] = overlayed

    return background


# Rotate an image by a certain angle (optionally adjusting size to fit)
def rotateImage(image, angle, scale=1, adjust_size=True):
    image_height, image_width, _ = image.shape
    prevoius_center = (image_width / 2, image_height / 2)

    # Get rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(
        center=prevoius_center, angle=angle, scale=scale
    )

    if adjust_size:
        abs_cos = abs(rotation_matrix[0][0])
        abs_sin = abs(rotation_matrix[0][1])

        # Compute new image bounds
        new_width = int(image_width * abs_cos + image_height * abs_sin)
        new_height = int(image_height * abs_cos + image_width * abs_sin)

        # Adjust transformation to keep image centered
        rotation_matrix[0][2] += (new_width / 2) - prevoius_center[0]
        rotation_matrix[1][2] += (new_height / 2) - prevoius_center[1]

        rotated_image = cv2.warpAffine(
            src=image, M=rotation_matrix, dsize=(new_width, new_height)
        )
    else:
        rotated_image = cv2.warpAffine(
            src=image, M=rotation_matrix, dsize=(image_width, image_height)
        )

    return rotated_image


# Draw text with a filled rectangle background and return bounding box coordinates
def putTextRect(
    img,
    text,
    pos,
    fontFace,
    fontScale,
    text_thickness,
    text_color,
    rect_color,
    offset=10,
):
    """Draw text inside a colored rectangle and return its bounding box."""
    ox, oy = pos

    # Get size of the text
    (text_width, text_height), _ = cv2.getTextSize(
        text=text, fontFace=fontFace, fontScale=fontScale, thickness=text_thickness
    )

    # Compute rectangle coordinates
    x1, y1, x2, y2 = (
        ox - offset,
        oy + offset,
        ox + text_width + offset,
        oy - text_height - offset,
    )

    # Draw rectangle background
    cv2.rectangle(
        img=img, pt1=(x1, y2), pt2=(x2, y1), color=rect_color, thickness=cv2.FILLED
    )

    # Draw the text
    cv2.putText(
        img=img,
        text=text,
        org=(ox, oy),
        fontFace=fontFace,
        fontScale=fontScale,
        color=text_color,
        thickness=text_thickness,
    )

    return {"x1": x1, "y1": y2, "x2": x2, "y2": y1}
