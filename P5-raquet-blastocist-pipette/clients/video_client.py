import cv2
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

# Define the URL of the FastAPI server
SERVER_URL = "http://127.0.0.1:9051/predict/"
# SERVER_URL = "http://127.0.0.1:8000/predict/"

def send_frame(frame):
    # Encode the frame as JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()

    start_time = time.time()  # Start timing
    
    # Send POST request to FastAPI server
    response = requests.post(SERVER_URL, files={"file": ("frame.jpg", frame_bytes, "image/jpeg")})
    
    end_time = time.time()  # End timing
    response_time = end_time - start_time

    if response.status_code == 200:
        return response.json(), response_time
    else:
        print(f"Error: {response.status_code}")
        return None, response_time

def draw_bboxes(frame, detections):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image)

    # Define a font (you may need to adjust the path)
    try:
        font = ImageFont.truetype("arial.ttf", size=15)
    except IOError:
        font = ImageFont.load_default()

    # Iterate over each class in the response
    for class_name, objects in detections.items():
        for obj in objects:
            x1, y1, x2, y2 = obj["bounding_box"]
            confidence = obj["confidence"]
            label = f"{class_name} {confidence:.2f}"
            
            # Draw bounding box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            draw.text((x1, y1), label, fill="red", font=font)

    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    total_time = 0
    num_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Send frame to FastAPI server and get predictions
        result, response_time = send_frame(frame)

        total_time += response_time
        num_frames += 1

        if result:
            # Extract bounding boxes from the result
            detections = result["response"].get("response", {})
            
            # Draw bounding boxes on the frame
            frame = draw_bboxes(frame, detections)

        average_time = total_time / num_frames
        print(f"Average response time: {average_time:.3f} seconds")

        # Display the frame with annotations
        cv2.imshow('Video', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if num_frames > 0:
        average_time = total_time / num_frames
        print(f"Average response time: {average_time:.3f} seconds")
    else:
        print("No frames processed.")

if __name__ == "__main__":
    # Path to the video file
    video_path = r"/home/mario_reyes_m/Documents/APIs/P5-PerfTest_20240425_154226 TEST 3.mp4"
    # video_path = r"C:\ConceivableProjectsR\Pearl3\APIs\api-p3-sperm-needle\p3spermneedletip\Data\clip1.mp4"

    
    # Process the video
    process_video(video_path)
