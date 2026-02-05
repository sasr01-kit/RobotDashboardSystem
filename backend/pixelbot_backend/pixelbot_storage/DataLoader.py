from pixelbot_backend.pixelbot_model.DrawingData import DrawingData
from pixelbot_backend.pixelbot_model.Session import Session
from pixelbot_backend.pixelbot_model.Child import Child
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureWidth import SpeechSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureDepth import SpeechSelfDisclosureDepth
from pixelbot_backend.pixelbot_model.DrawingSelfDisclosureWidth import DrawingSelfDisclosureWidth
import datetime
import os
import csv
import json
import re
import hashlib

class DataLoader:
    DRAWING_FILE_NAME = "drawing.png"
    TRANSCRIPT_FILE_NAME = "transcript.txt"
    STORY_SUMMARY_FILE_NAME = "drawing_description.txt"
  
    def __init__(self, data_root):
        self.data_root = data_root
        # self.imageData: Optional[str] = None


    def load_all_children(self):
        children = []
        # Iterate over each child directory
        for child_name in os.listdir(self.data_root):
            child_path = os.path.join(self.data_root, child_name)
            # Check if it's a directory (not a file)
            if os.path.isdir(child_path):
                child = self.load_child(child_name, child_path)
                children.append(child)
        return children

    def load_child(self, child_name, child_path):
        sessions = []
        # Iterate over each session directory
        for session_id in os.listdir(child_path):
            session_path = os.path.join(child_path, session_id)
            # Check if it's a directory (not a file)
            if os.path.isdir(session_path):
                session = self.load_session(session_id, session_path)
                sessions.append(session)
                child_id = self.short_hash(child_name, length=64)
        return Child(child_id=child_id, name=child_name, sessions=sessions)

    def load_session(self, session_id, session_path):
        drawing_path = self.find_drawing_file(session_path)
        if os.path.exists(drawing_path):
            drawing = DrawingData(drawing_path)
            session_date_string = self.extract_day_from_filename(drawing_path)
            session_date_obj = datetime.datetime.strptime(session_date_string, "%d-%m-%Y")
        else: 
            drawing = DrawingData("")
        
        transcript_path = os.path.join(session_path, self.TRANSCRIPT_FILE_NAME)
        transcript_text = self.loadTxt(transcript_path)
        transcript = self.parse_transcript(transcript_text)

        story_summary_path = os.path.join(session_path, self.STORY_SUMMARY_FILE_NAME)
        story_summary_text = self.loadTxt(story_summary_path)
        story_summary = self.parse_story_summary(story_summary_text)

        speech_depth_path = os.path.join(session_path, "speech_self_disclosure_depth_data.csv") 
        speech_width_path = os.path.join(session_path, "speech_self_disclosure_width_data.csv")
        drawing_width_path = os.path.join(session_path, "drawing_self_disclosure_width_data.csv")

        speech_width = SpeechSelfDisclosureWidth(**self.loadCsv(speech_width_path))
        speech_depth = SpeechSelfDisclosureDepth(**self.loadCsv(speech_depth_path))
        drawing_width = DrawingSelfDisclosureWidth(**self.loadCsv(drawing_width_path))
        
        return Session(
            session_id,
            session_date_obj,
            drawing,
            story_summary,
            transcript,
            speech_width, 
            speech_depth,
            drawing_width
        )
    
    # Helper to find drawing file with .png extension
    def find_drawing_file(self, session_path):
        for file in os.listdir(session_path):
            if file.lower().endswith(".png"):
                return os.path.join(session_path, file)
        return ""  

    def extract_day_from_filename(self, filename):
        # get base name without extension
        base_name = os.path.splitext(os.path.basename(filename))[0]
        # Extracts date in MM-DD-YYYY format from filename
        match = re.match(r".+_(\d{2}-\d{2}-\d{4})", base_name)
        if match:
            return match.group(1)
        return None

    # Helper to load text file
    def loadTxt(self, file_path):
        content = ""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        return content
    
    def parse_transcript(self, text):
        transcript_list = []

        for line in text.splitlines():
            if ": " in line:
                speaker, message = line.split(": ", 1)
                transcript_list.append({
                    "name": speaker.strip(),
                    "description": message.strip()
                })

        return transcript_list
    
    def parse_story_summary(self, text):
        try:
            object_dict = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"Error: Could not parse story summary as JSON. {e}")
            return []

        summary_list = []
        for name, description in object_dict.items():
            summary_list.append({
                "name": name,
                "description": description
            })
        return summary_list

    # Helper to load CSV file into a dictionary
    def loadCsv(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                return next(reader, {})
        return {}
    
    def short_hash(self, name, length=64):
        full_hash = hashlib.sha256(name.encode()).hexdigest()
        return full_hash[:length]
 # Encode PNG to base64
        # with open(png_path, "rb") as f: #turn this in to a method, make required variables in the file, 
           #  self._mapDataPNG = base64.b64encode(f.read()).decode("utf-8")
    
