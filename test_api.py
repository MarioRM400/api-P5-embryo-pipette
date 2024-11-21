import requests
from PIL import Image, ImageDraw
import io
import os
import cv2

# Define the URL of the FastAPI server
SERVER_URL = "http://127.0.0.1:9051/predict/"


def send_image(image_path):
    # Open the image file
    with open(image_path, "rb") as image_file:
        # Send POST request to FastAPI server
        response = requests.post(SERVER_URL, files={"file": image_file})

        # Check if the request was successful
        if response.status_code == 200:
            # Process the response
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None


def draw_bbox_on_image(
    img: str,
    rectangles_with_labels: tuple,
    rectangle_color=(0, 255, 0),
    text_color=(0, 0, 255),
    thickness=2,
    sz=0.6,
    background_rectangle=True,
):
    img = cv2.imread(str(img))
    font = cv2.FONT_HERSHEY_SIMPLEX
    for rect, ci, label in rectangles_with_labels:
        x1, y1, x2, y2 = rect
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        img = cv2.rectangle(img, (x1, y1), (x2, y2), rectangle_color, thickness)
        text_x, text_y = x1, max(10, y1 - 10)
        text = f"{label}: {ci:.2f}"

        if background_rectangle:
            (text_width, text_height), baseline = cv2.getTextSize(
                text, font, sz, thickness
            )
            cv2.rectangle(
                img,
                (text_x, text_y - text_height - baseline),
                (text_x + text_width, text_y + baseline),
                rectangle_color,
                cv2.FILLED,
            )
        else:
            pass

        cv2.putText(
            img, text, (text_x, text_y), font, sz, text_color, thickness=thickness
        )
    return img


def draw_bboxes(image_path: str, data: dict):
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    rectangles_with_labels = []

    # Draw bounding boxes
    if isinstance(data, dict):
        for category, objects in data.items():
            for obj in objects:
                bbox = obj.get(f"{'bounding_box'}", [])
                confidence = obj.get(f"{'confidence'}", [])
                if len(bbox) == 4:
                    rectangles_with_labels.append((bbox, confidence, category))

        img = draw_bbox_on_image(image_path, rectangles_with_labels)
        cv2.imwrite(os.path.join("output/", image_path), img)

    # Show the image with bounding boxes
    # image.show()


if __name__ == "__main__":
    # Path to the image file
    image_path = os.path.join("test_inference.jpg")

    # Send the image and get the predictions
    result = send_image(image_path)

    print(result)
    if result:
        # Extract bounding boxes from the result
        data = result.get("response", [])

        # Draw bounding boxes on the image
        draw_bboxes(image_path, data)
