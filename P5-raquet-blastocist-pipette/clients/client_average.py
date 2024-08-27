import os
import requests
from PIL import Image, ImageDraw, ImageFont
import time

# Define the URL of the FastAPI server
SERVER_URL = "http://127.0.0.1:8000/predict/"

def send_image(image_path):
    start_time = time.time()  # Start timing
    
    # Open the image file
    with open(image_path, "rb") as image_file:
        # Send POST request to FastAPI server
        response = requests.post(SERVER_URL, files={"file": image_file})
        
        end_time = time.time()  # End timing
        
        # Check if the request was successful
        if response.status_code == 200:
            # Process the response
            return response.json(), end_time - start_time
        else:
            print(f"Error: {response.status_code}")
            return None, end_time - start_time

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

def process_images_from_folder(folder_path):
    total_time = 0
    num_images = 0
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            
            # Send the image and get the predictions
            result, response_time = send_image(image_path)
            
            # Accumulate the total time and count the images
            total_time += response_time
            num_images += 1
            
            if result:
                # Extract bounding boxes from the result
                bboxes = result.get("predictions", [])
                average_time = total_time / num_images
                
                print(f"Average response time: {average_time:.2f} seconds")
                
                # Draw bounding boxes on the image
                # draw_bboxes(image_path, bboxes)
    
    if num_images > 0:
        average_time = total_time / num_images
        print(f"Average response time: {average_time:.2f} seconds")
    else:
        print("No images processed.")

if __name__ == "__main__":
    # Path to the folder containing images
    folder_path = r"C:\Users\PC KAIJU\ConceivableProjectsTools\sperm-needle_tip-v0.0.2\images"
    
    # Process images from the folder and calculate average response time
    process_images_from_folder(folder_path)
