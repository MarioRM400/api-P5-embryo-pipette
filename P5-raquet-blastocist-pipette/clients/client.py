import requests
from PIL import Image, ImageDraw, ImageFont
import json
import os

# Define the URL of the FastAPI server
# SERVER_URL = "http://127.0.0.1:8000/predict/"
SERVER_URL = "http://127.0.0.1:9051/predict/"


def send_image(image_path):
    """
    Sends an image to the FastAPI server for prediction.

    Args:
        image_path (str): Path to the image file to send.

    Returns:
        dict: JSON response from the server.
    """
    with open(image_path, "rb") as image_file:
        response = requests.post(SERVER_URL, files={"file": image_file})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def draw_bboxes(image_path, response, output_dir):
    """
    Draws bounding boxes from the response on the image and saves it.

    Args:
        image_path (str): Path to the original image.
        response (dict): JSON response containing predictions.
        output_dir (str): Directory to save the annotated image.
    """
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Define a font
    try:
        font = ImageFont.truetype("arial.ttf", size=15)
    except IOError:
        font = ImageFont.load_default()
    
    # Parse and draw bounding boxes
    response_data = response.get("response", {}).get("response", {})
    for label, objects in response_data.items():
        for obj in objects:
            bbox = obj["bounding_box"]
            confidence = obj["confidence"]
            x1, y1, x2, y2 = bbox
            
            # Draw bounding box and label
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            text = f"{label} {confidence:.2f}"
            draw.text((x1, y1 - 15), text, fill="red", font=font)

    # Save the annotated image
    annotated_image_name = f"annotated_{os.path.basename(image_path)}"
    annotated_image_path = os.path.join(output_dir, annotated_image_name)
    image.save(annotated_image_path)
    print(f"Annotated image saved to: {annotated_image_path}")

    return annotated_image_path

def save_json(response, image_path, output_dir):
    """
    Saves the JSON response to a file.

    Args:
        response (dict): JSON response to save.
        image_path (str): Path to the original image for naming.
        output_dir (str): Directory to save the JSON file.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Create the JSON file path
    json_file_name = os.path.splitext(os.path.basename(image_path))[0] + "_predictions.json"
    json_path = os.path.join(output_dir, json_file_name)

    # Save the JSON data
    with open(json_path, "w") as json_file:
        json.dump(response, json_file, indent=4)
    print(f"JSON response saved to: {json_path}")

if __name__ == "__main__":
    # Path to the input image
    image_path = r"/mnt/d/ConceivableProjectsR/Pearl5/APIs/api-P5-raquet-blastocist-pipette/Data/proto_data_5_frame_00293.jpg"
    
    # Directory to save results
    output_dir = "./results"

    # Send the image and get the predictions
    result = send_image(image_path)
    
    if result:
        # Save the JSON response
        save_json(result, image_path, output_dir)

        # Draw bounding boxes and save the annotated image
        draw_bboxes(image_path, result, output_dir)
