from pixelbot_backend.pixelbot_model.DrawingSelfDisclosureWidth import DrawingSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureWidth import SpeechSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureDepth import SpeechSelfDisclosureDepth
from pixelbot_backend.pixelbot_model.DrawingData import DrawingData
import datetime

class Session:
    def __init__(self, session_id: str, session_date: datetime , drawing: DrawingData, story_summary: list, transcript: list,
                 speech_width: SpeechSelfDisclosureWidth, speech_depth: SpeechSelfDisclosureDepth,
                 drawing_width: DrawingSelfDisclosureWidth):
        self.session_id = session_id
        # Date in format "DD_MM_YYYY"
        self.session_date = session_date
        self.drawing = drawing
        self.story_summary = story_summary
        self.transcript = transcript
        self.speech_width = speech_width
        self.speech_depth = speech_depth
        self.drawing_width = drawing_width

    def to_dict(self):
        return {
            "sessionId": self.session_id,
            "sessionDate": self.session_date,
            "sessionDate": self.session_date.strftime("%d-%m-%Y"),
            "drawing": self.drawing.to_dict(),
            "storySummary": self.story_summary,
            "transcript": self.transcript,
            "speechWidth": self.speech_width.to_dict(),
            "speechDepth": self.speech_depth.to_dict(),
            "drawingWidth": self.drawing_width.to_dict()
        }
    def getTotalWordCount(self):
        return int(self.speech_width.getTotalWordCount())
    
    def getAvgIntimacyScore(self):
        return float(self.speech_depth.getAvgIntimacyScore())
    
    def getInterventionCount(self):
        return int(self.speech_width.getInterventionCount())
    
    def getTotalSpeechTime(self):
        return float(self.speech_width.getTotalSpeechTime())
    
    def getStrokeCountDrawing(self):
        return int(self.drawing_width.getStrokeCount())
    
    def getColorsUsedCountDrawing(self):
        return int(self.drawing_width.getColorUsedCount())
    
    def getFilledAreaDrawing(self):
        return float(self.drawing_width.getAmountFilledArea())
    
    def getSessionId(self):
        return self.session_id
    
    def getSessionDate(self):
        return self.session_date
    
    def getDrawing(self):
        return self.drawing
    
    def getStorySummary(self):
        return self.story_summary
    
    def getTranscript(self):
        return self.transcript  
    
    def getSpeechWidth(self):
        return self.speech_width
    
    def getSpeechDepth(self):
        return self.speech_depth
    
    def getDrawingWidth(self):
        return self.drawing_width
   
    @staticmethod
    def from_dict(data):
        return Session(
            session_id=data["sessionId"],
            session_date=data["sessionDate"],
            drawing=DrawingData.from_dict(data["drawing"]),
            story_summary=data["storySummary"],
            transcript=data["transcript"],
            speech_width=SpeechSelfDisclosureWidth.from_dict(data["speechWidth"]),
            speech_depth=SpeechSelfDisclosureDepth.from_dict(data["speechDepth"]),
            drawing_width=DrawingSelfDisclosureWidth.from_dict(data["drawingWidth"])
        )
   