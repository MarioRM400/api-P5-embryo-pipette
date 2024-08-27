from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from PIL import Image
import io
import torch
from app.model import YOLOv5Model
from app.utils import process_image, convert_results_to_dict
import os

app = FastAPI()

current_path = os.getcwd()
weights_path = os.path.join(current_path, "Weights", "P5-raquet-blastocist-pipette-v0.0.1.pt")

# Initialize the YOLOv5 model
model = YOLOv5Model(weights_path)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Read the image file
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Process and predict
    results = model.predict(image)
    
    # Convert results to dict
    results_dict = convert_results_to_dict(results)
    
    return {"response": results_dict}
