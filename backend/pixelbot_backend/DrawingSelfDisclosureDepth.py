
class DrawingSelfDisclosureWidth:
    def __init__(self, surface_percentage: float, num_strokes: int, avg_stroke_length: float, std_stroke_length: float,
                 number_colors_used: int, number_pen_sizes_used: int):
        self.surface_percentage = surface_percentage
        self.num_strokes = num_strokes
        self.avg_stroke_length = avg_stroke_length
        self.std_stroke_length = std_stroke_length
        self.number_colors_used = number_colors_used
        self.number_pen_sizes_used = number_pen_sizes_used

    def to_dict(self):
        return {
            "surfacePercentage": self.surface_percentage,
            "numStrokes": self.num_strokes,
            "avgStrokeLength": self.avg_stroke_length,
            "stdStrokeLength": self.std_stroke_length,
            "numberColorsUsed": self.number_colors_used,
            "numberPenSizedUsed": self.number_pen_sizes_used
        } 
    
    def getSurfacePercentage(self):
        return self.surface_percentage
    
    def getNumStrokes(self):
        return self.num_strokes 
    
    def getAvgStrokeLength(self):
        return self.avg_stroke_length   
    
    def getStdStrokeLength(self):
        return self.std_stroke_length   
    
    def getNumberColorsUsed(self):
        return self.number_colors_used
    
    def getNumberPenSizesUsed(self):
        return self.number_pen_sizes_used   
    