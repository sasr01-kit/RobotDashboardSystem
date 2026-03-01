import base64

class DrawingData:
    def __init__(self, base64_data: str): 
        # Store the base64-encoded PNG image data (without prefix)
        self.base64 = base64_data      
    
    def to_dict(self):
        
        # Return the image as a list with the proper data URI prefix for frontend rendering
        return [f"data:image/png;base64,{self.base64}"]
    
    @staticmethod
    def from_dict(data):
        # Create a DrawingData object from a list containing a prefixed base64 string
        obj = DrawingData("")

        # data is ["data:image/png;base64,...."]
        if isinstance(data, list) and len(data) > 0:
            prefixed = data[0]
            # Remove the data URI prefix to store only the raw base64 string
            obj.base64 = prefixed.replace("data:image/png;base64,", "")
        
        return obj

