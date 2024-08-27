import requests
from PIL import Image, ImageDraw
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
    
    # Draw bounding boxes
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox["coc_in_r2_points"]
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
    
    # Show the image with bounding boxes
    image.show()

if __name__ == "__main__":
    # Path to the image file
    image_path = r"/mnt/c/ConceivableProjectsR/Pearl2/APIs/api-routine2-coc/routine2coc/Data/example1.jpg"
    
    # Send the image and get the predictions
    result = send_image(image_path)
    
    if result:
        # Extract bounding boxes from the result
        bboxes = result["response"].get("response", {}).get("coc_in_r2", [])
        
        print(bboxes)
        # Draw bounding boxes on the image
        draw_bboxes(image_path, bboxes)
