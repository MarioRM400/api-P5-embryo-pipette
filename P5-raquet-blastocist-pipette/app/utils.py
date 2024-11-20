import numpy as np

def process_image(image):
    # Preprocess the image if necessary
    return image

# Mapping of class IDs to class names (update this as needed)
CLASS_NAMES = {
    0: "embryo",
    1: "pipette_tip",
    2: "racket",
    3: "z_embryo",
    4: "z_pippet_tip",
}


def convert_results_to_dict(results):
    response_dict = {"response": {}}
    
    for i, pred in enumerate(results.pred[0]):
        x1, y1, x2, y2, conf, cls = pred.tolist()
        class_name = CLASS_NAMES.get(int(cls), "unknown")
        
        if class_name not in response_dict["response"]:
            response_dict["response"][class_name] = []
        
        response_dict["response"][class_name].append({
            "id": i,
            "bounding_box": [x1, y1, x2, y2],
            "confidence": round(conf, 2)
        })
    
    return response_dict


