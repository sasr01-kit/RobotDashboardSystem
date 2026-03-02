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
        # SpeechSelfDisclosureWidth object (speech metrics: word count, interventions, etc.)
        self.speech_width = speech_width
        # SpeechSelfDisclosureDepth object (speech intimacy metrics)
        self.speech_depth = speech_depth
        # DrawingSelfDisclosureWidth object (drawing metrics: strokes, colors, area)
        self.drawing_width = drawing_width

    def to_dict(self):
        return {
            "sessionId": self.session_id,
            "sessionDate": self.session_date.strftime("%d-%m-%Y"),
            "drawing": self.drawing.to_dict(),
            "storySummary": self.story_summary,
            "transcript": self.transcript,
            "speechWidth": self.speech_width.to_dict(),
            "speechDepth": self.speech_depth.to_dict(),
            "drawingWidth": self.drawing_width.to_dict()
        }
    def get_total_word_count(self):
        return int(self.speech_width.get_total_word_count())
    
    def get_avg_intimacy_score(self):
        return float(self.speech_depth.get_avg_intimacy_score())
    
    def get_intervention_count(self):
        return self.speech_width.get_intervention_count()
    
    def get_total_speech_time(self):
        return float(self.speech_width.get_total_speech_time())
    
    def get_stroke_count_drawing(self):
        return int(self.drawing_width.get_stroke_count())
    
    def get_colors_used_count_drawing(self):
        return int(self.drawing_width.get_color_used_count())
    
    def get_filled_area_drawing(self):
        return float(self.drawing_width.get_amount_filled_area())
    
    def get_session_id(self):
        return self.session_id
    
    def get_session_date(self):
        return self.session_date
    
    def get_drawing(self):
        return self.drawing
    
    def get_story_summary(self):
        return self.story_summary
    
    def get_transcript(self):
        return self.transcript  
    
    def get_speech_width(self):
        return self.speech_width
    
    def get_speech_depth(self):
        return self.speech_depth
    
    def get_drawing_width(self):
        return self.drawing_width
   
    @staticmethod
    def from_dict(data):
    
        # Reconstruct a Session object from a dictionary (loaded from JSON)
        session_id = data["sessionId"]
        session_date_str = data["sessionDate"]

        # Convert date string to datetime object if present
        session_date = None
        if session_date_str:
            session_date = datetime.datetime.strptime(session_date_str, "%d-%m-%Y")

        drawing = DrawingData.from_dict(data["drawing"])
        story_summary = data["storySummary"]
        transcript = data["transcript"]
        
        # Reconstruct metric objects using dictionary unpacking
        speech_width = SpeechSelfDisclosureWidth(**data["speechWidth"])
        speech_depth = SpeechSelfDisclosureDepth(**data["speechDepth"])
        drawing_width = DrawingSelfDisclosureWidth(**data["drawingWidth"])

        return Session(
            session_id,
            session_date,
            drawing,
            story_summary,
            transcript,
            speech_width,
            speech_depth,
            drawing_width,
        )
    