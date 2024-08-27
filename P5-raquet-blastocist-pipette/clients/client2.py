import requests
from PIL import Image, ImageDraw, ImageFont
import io

# Define the URL of the FastAPI server
SERVER_URL = "http://127.0.0.1:8000/predict/"

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

def draw_bboxes(image_path, bboxes):
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Define a font (you may need to adjust the path)
    try:
        font = ImageFont.truetype("arial.ttf", size=15)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw bounding boxes and labels
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox["bbox"]
        label = bbox["label"]
        confidence = bbox["confidence"]
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        text = f"{label} {confidence:.2f}"
        draw.text((x1, y1), text, fill="red", font=font)
    
    # Show the image with bounding boxes
    image.show()

if __name__ == "__main__":
    # Path to the image file
    image_path = r"C:\Users\PC KAIJU\ConceivableProjectsTools\APIs\custom_api\custom_api\example1.jpg"

    
    # Send the image and get the predictions
    result = send_image(image_path)
    
    if result:
        # Extract bounding boxes from the result
        bboxes = result.get("predictions", [])
        
        # Draw bounding boxes on the image
        draw_bboxes(image_path, bboxes)
