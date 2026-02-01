from pixelbot_backend.pixelbot_model.DrawingData import DrawingData
from pixelbot_backend.pixelbot_model.Session import Session
from pixelbot_backend.pixelbot_model.Child import Child
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureWidth import SpeechSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureDepth import SpeechSelfDisclosureDepth
from pixelbot_backend.pixelbot_model.DrawingSelfDisclosureWidth import DrawingSelfDisclosureWidth
import os
import csv
import json

class DataLoader:
    DRAWING_FILE_NAME = "drawing.png"
    TRANSCRIPT_FILE_NAME = "transcript.txt"
    STORY_SUMMARY_FILE_NAME = "drawing_description.txt"
  
    def __init__(self, data_root):
        self.data_root = data_root

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
        return Child(child_name, child_name , sessions)

    def load_session(self, session_id, session_path):
        drawing_path = self.find_drawing_file(session_path)
        if os.path.exists(drawing_path):
            drawing = DrawingData(drawing_path)
        else: 
            drawing = DrawingData("")
        
        transcript_path = os.path.join(session_path, self.TRANSCRIPT_FILE_NAME)
        transcript = self.loadTxt(transcript_path)

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

    # Helper to load text file
    def loadTxt(self, file_path):
        content = ""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        return content
    
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
