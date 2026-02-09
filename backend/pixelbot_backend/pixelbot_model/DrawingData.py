import base64

class DrawingData:
    def __init__(self, image_path: str):
        self.base64 = self.load_base64(image_path)

    def load_base64(self, file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")    
    
    
    def to_dict(self):
        return [f"data:image/png;base64,{self.base64}"]
    
    @staticmethod
    def from_dict(data):
        obj = DrawingData("")
        obj.base64 = data.get("image")
        return obj

