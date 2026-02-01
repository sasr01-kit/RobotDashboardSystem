
class DrawingData:
    def __init__(self, image_path: str):
        self.image_path = image_path

    def to_dict(self):
        return {
            "imagePath": self.image_path
        }
    
    def getImagePath(self):
        return self.image_path 
    
    @staticmethod
    def from_dict(data):
        return DrawingData(
            image_path=data["imagePath"]
        )
