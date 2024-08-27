import torch

class YOLOv5Model:
    def __init__(self, model_path: str):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path,
                                    force_reload=True)
        self.model.to(torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu'))
        self.model.compute_iou = .55
        self.model.conf = .5
        self.model.eval()

    def predict(self, image):
        # Perform prediction
        results = self.model(image)
        return results
