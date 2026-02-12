import base64

class DrawingData:
    def __init__(self, base64_data: str):
        self.base64 = base64_data

    def load_base64(self, file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")    
    
    
    def to_dict(self):
        return [f"data:image/png;base64,{self.base64}"]
    
    @staticmethod
    def from_dict(data):
        obj = DrawingData("")

        # data is ["data:image/png;base64,...."]
        if isinstance(data, list) and len(data) > 0:
            prefixed = data[0]
            # remove prefix
            obj.base64 = prefixed.replace("data:image/png;base64,", "")
        
        return obj

