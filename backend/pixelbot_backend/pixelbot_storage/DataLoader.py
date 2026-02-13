import base64
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



class DataLoader:
    DRAWING_FILE_NAME = "drawing.png"
    TRANSCRIPT_FILE_NAME = "transcript.txt"
    STORY_SUMMARY_FILE_NAME = "drawing_description.txt"
  
    def __init__(self, data_root):      
        # Store the root directory containing all child data folders
        self.data_root = data_root


    def load_all_children(self):
        children = []

        # Iterate over each child directory in the root folder
        for child_name in os.listdir(self.data_root):
            child_path = os.path.join(self.data_root, child_name)

            # Only process directories (skip files)
            if os.path.isdir(child_path):
                child = self.load_child(child_name, child_path)
                children.append(child)
        return children

    def load_child(self, child_name, child_path):
        sessions = []

        # Iterate over each session directory for this child
        for session_id in os.listdir(child_path):
            session_path = os.path.join(child_path, session_id)

            # Only process directories (skip files)
            if os.path.isdir(session_path):
                session = self.load_session(session_id, session_path)
                sessions.append(session)
        return Child(child_id=None, name=child_name, sessions=sessions)

    def load_session(self, session_id, session_path):
        # Find the drawing file (.png) for this session
        drawing_path = self.find_drawing_file(session_path)
        
        if os.path.exists(drawing_path):    
            # Load drawing as base64 and extract session date from filename
            drawing = self.getDrawingDataObject(drawing_path)
            session_date_string = self.extract_day_from_filename(drawing_path)
            session_date_obj = datetime.datetime.strptime(session_date_string, "%d-%m-%Y")
        else: 
            drawing = DrawingData("")
        
        
        # Load and parse transcript text file
        transcript_path = os.path.join(session_path, self.TRANSCRIPT_FILE_NAME)
        transcript_text = self.loadTxt(transcript_path)
        transcript = self.parse_transcript(transcript_text)

        
        # Load and parse story summary text file
        story_summary_path = os.path.join(session_path, self.STORY_SUMMARY_FILE_NAME)
        story_summary_text = self.loadTxt(story_summary_path)
        story_summary = self.parse_story_summary(story_summary_text)

        
        # Load CSV metric files and parse into metric objects
        speech_depth_path = os.path.join(session_path, "speech_self_disclosure_depth_data.csv") 
        speech_width_path = os.path.join(session_path, "speech_self_disclosure_width_data.csv")
        drawing_width_path = os.path.join(session_path, "drawing_self_disclosure_width_data.csv")

        
        # Load metric data from CSV files and instantiate metric objects. 
        # The ** operator unpacks the dictionary as keyword arguments to the class constructor.
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
        
        # Parse each line in transcript into speaker/message dict
        for line in text.splitlines():
            if ": " in line:
                speaker, message = line.split(": ", 1)
                transcript_list.append({
                    "name": speaker.strip(),
                    "description": message.strip()
                })

        return transcript_list
    
    def parse_story_summary(self, text):
        
        # Parse story summary as JSON (object name, description)
        try:
            object_dict = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"Error: Could not parse story summary as JSON. {e}")
            return []

        summary_list = []
        
        # Convert JSON object into list of dicts for frontend
        for name, description in object_dict.items():
            summary_list.append({
                "name": name,
                "description": description
            })
        return summary_list

    # Helper to load CSV file into a dictionary
    def loadCsv(self, file_path):
        if os.path.exists(file_path):
            
        # Open the file in read mode with UTF-8 encoding
            with open(file_path, "r", encoding="utf-8") as f:           
        # Create a DictReader to parse the CSV into dictionaries (one per row)
                reader = csv.DictReader(f)
                return next(reader, {})
        return {}
    
    def getDrawingDataObject(self, drawing_path):
        # Read drawing file as binary and encode as base64 string
        with open(drawing_path, "rb") as file:
            b64_format = base64.b64encode(file.read()).decode("utf-8")
        return DrawingData(b64_format)
    
    
