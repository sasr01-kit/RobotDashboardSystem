
class DrawingSelfDisclosureWidth:
    def __init__(self, stroke_count: int, total_stroke_length: float ,average_stroke_length: float, std_stroke_length: float,
                 color_used_count: int, pen_size_used_count: int, amount_filled_area: float):
        self.stroke_count = stroke_count
        self.total_stroke_length = total_stroke_length
        self.average_stroke_length = average_stroke_length
        self.std_stroke_length = std_stroke_length
        self.color_used_count = color_used_count
        self.pen_size_used_count = pen_size_used_count
        self.amount_filled_area = amount_filled_area

    def to_dict(self):
        return {
            "stroke_count": self.stroke_count,
            "total_stroke_length": self.total_stroke_length,
            "average_stroke_length": self.average_stroke_length,
            "std_stroke_length": self.std_stroke_length,
            "color_used_count": self.color_used_count,
            "pen_size_used_count": self.pen_size_used_count,
            "amount_filled_area": self.amount_filled_area
        }
    
    def getStrokeCount(self):
        return self.stroke_count        
    
    def getTotalStrokeLength(self):
        return self.total_stroke_length 
    
    def getAvgStrokeLength(self):
        return self.average_stroke_length
    
    def getStdStrokeLength(self):
        return self.std_stroke_length   
    
    def getColorUsedCount(self):
        return self.color_used_count
    
    def getPenSizeUsedCount(self):
        return self.pen_size_used_count
    
    def getAmountFilledArea(self):
        return self.amount_filled_area
    
    @staticmethod
    def from_dict(data):
        return DrawingSelfDisclosureWidth(
            stroke_count=data["stroke_count"],
            total_stroke_length=data["total_stroke_length"],
            average_stroke_length=data["average_stroke_length"],
            std_stroke_length=data["std_stroke_length"],
            color_used_count=data["color_used_count"],
            pen_size_used_count=data["pen_size_used_count"],
            amount_filled_area=data["amount_filled_area"]
        )