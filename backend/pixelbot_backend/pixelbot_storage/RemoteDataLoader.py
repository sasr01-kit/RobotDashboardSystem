from pixelbot_backend.pixelbot_model.DrawingData import DrawingData
from pixelbot_backend.pixelbot_model.Session import Session
from pixelbot_backend.pixelbot_model.Child import Child
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureWidth import SpeechSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureDepth import SpeechSelfDisclosureDepth
from pixelbot_backend.pixelbot_model.DrawingSelfDisclosureWidth import DrawingSelfDisclosureWidth
import requests
import io, csv
import os, re
import datetime
import json

"""
RemoteDataLoader is responsible for loading child and session data from the Pixelbot robot via HTTP requests.
It reconstructs model objects from remote files, enabling backend operation with live robot data.
"""
class RemoteDataLoader:

    GRAPHIC_FILE_FORMAT = ".png"
    TRANSCRIPT_FILE_NAME = "transcript.txt"
    STORY_SUMMARY_FILE_NAME = "drawing_description.txt"
    SPEECH_DEPTH_CSV = "speech_self_disclosure_depth_data.csv"
    SPEECH_WIDTH_CSV = "speech_self_disclosure_width_data.csv"
    DRAWING_WIDTH_CSV = "drawing_self_disclosure_width_data.csv"
    CHILDREN_ENDPOINT = "/children"
    SESSIONS_ENDPOINT = "/sessions"
    FILE_ENDPOINT = "/file/"
    JSON_KEY_CHILDREN = "children"
    JSON_KEY_SESSIONS = "sessions"
    SLASH = '/'
    EMPTY_STRING = ""
    
    def __init__(self, pixelbot_url):
        # Remove trailing slash to avoid double slashes in URLs
        self.pixelbot_url = pixelbot_url.rstrip(self.SLASH)

    ''' Load all children and their sessions from the Pixelbot robot. This is the main entry point for fetching data.'''
    def load_all_children(self):
        children = []
        
        # Fetch the list of child names from the pixelbot's /children endpoint
        resp = requests.get(f"{self.pixelbot_url}{self.CHILDREN_ENDPOINT}")
        children_names = resp.json()[self.JSON_KEY_CHILDREN]
        
        # For each child, load their sessions and build a Child object
        for child_name in children_names:
            child = self.load_child(child_name)
            children.append(child)
        return children

    ''' Load a single child's data including all sessions. Returns a Child object.'''
    def load_child(self, child_name):
        sessions = []
        # Get sessions for this child with the structured URL: pixelbot_url/child_name/sessions
        resp = requests.get(f"{self.pixelbot_url}{self.SLASH}{child_name}{self.SESSIONS_ENDPOINT}")
        session_ids = resp.json()[self.JSON_KEY_SESSIONS]

        # For each session, load the session data and build a Session object
        for session_id in session_ids:
            session = self.load_session(child_name, session_id)
            sessions.append(session)  
        
        # child_id is None since it will be implemented in the DataRepository class   
        return Child(None, child_name, sessions)

    ''' Load a single session's data including drawing, transcript, story summary, and metrics. Returns a Session object.'''
    def load_session(self, child_name, session_id):
        # get drawing file path name. Then extract the date of the session 
        drawing_file_url = self.get_drawing_file(child_name, session_id)
        session_date = self.extract_day_from_file_url(drawing_file_url)
        
        # Download the drawing file and create DrawingData object
        drawing = DrawingData("")
        try:
            resp = requests.get(drawing_file_url)
            drawing = DrawingData(resp.json()["base64"])
        except Exception as e:
            print(f"Failed to load drawing for {session_id}: {e}")
        
        # Load transcript text file and parse it into a structured list
        transcript_text = self.load_txt(child_name, session_id, self.TRANSCRIPT_FILE_NAME)
        transcript = self.parse_transcript(transcript_text)
        
        # Load story summary text file and parse it into a structured list
        story_summary_text = self.load_txt(child_name, session_id, self.STORY_SUMMARY_FILE_NAME)
        story_summary = self.parse_story_summary(story_summary_text)

        
        # Build URLs for CSV metric files and load their contents
        speech_depth_path = self.get_file_url(child_name, session_id, self.SPEECH_DEPTH_CSV)
        speech_width_path = self.get_file_url(child_name, session_id, self.SPEECH_WIDTH_CSV)
        drawing_width_path = self.get_file_url(child_name, session_id, self.DRAWING_WIDTH_CSV)

        # Parse CSVs into metric objects with error handling to ensure robustness against missing files or malformed data
        try:
            speech_width = SpeechSelfDisclosureWidth(**self.load_csv(speech_width_path))
        except Exception as e:
            print(f"Failed to load speech_width for {child_name} for {session_id}: {e}")
            speech_width = SpeechSelfDisclosureWidth(0, 0, 0.0, 0.0, 0.0, 0.0, 0.0)

        try:
            speech_depth = SpeechSelfDisclosureDepth(**self.load_csv(speech_depth_path))
        except Exception as e:
            print(f"Failed to load speech_depth for {child_name} for {session_id}: {e}")    
            speech_depth = SpeechSelfDisclosureDepth(0.0, 0.0)

        try:
            drawing_width = DrawingSelfDisclosureWidth(**self.load_csv(drawing_width_path))
        except Exception as e:
            print(f"Failed to load drawing_width for {child_name} for {session_id}: {e}")
            drawing_width = DrawingSelfDisclosureWidth(0, 0.0, 0.0, 0.0, 0, 0, 0.0)        

        return Session(
            session_id,
            session_date,
            drawing,
            story_summary,
            transcript,
            speech_width,
            speech_depth,
            drawing_width
        )

    ''' Helper function to construct the URL for a given file based on child name, session ID, and file name. '''
    def get_file_url(self, child_name, session_id, file_name):
        # Returns the URL to the file on Pixelbot with the structure:
        # pixelbot_url/file/child_name/session_id/file_name
        return f"{self.pixelbot_url}{self.FILE_ENDPOINT}{child_name}{self.SLASH}{session_id}{self.SLASH}{file_name}"

    ''' Load a text file from the Pixelbot robot given the child name, session ID, and file name. 
        Returns empty string if file not found or error. '''
    def load_txt(self, child_name, session_id, file_name):
        url = self.get_file_url(child_name, session_id, file_name)
        resp = requests.get(url)
        if resp.status_code == 200:
        # Return empty string if file not found or error
            return resp.text
        return self.EMPTY_STRING

    ''' Load a CSV file from the Pixelbot robot and parse the first row into a dictionary.'''
    def load_csv(self, file_path):   
        # Download a CSV file and parse the first row into a dictionary
        resp = requests.get(file_path)
        # If successful, read CSV into dictionary
        if resp.status_code == 200:
            # Use io.StringIO to treat the response text as a file
            f = io.StringIO(resp.text)
            reader = csv.DictReader(f)
            return next(reader)
        return {}
    
    ''' Get the URL of the drawing file for a given child and session with the structure: pixelbot_url/file/child_name/session_id. 
        Returns None if not found. '''
    def get_drawing_file(self, child_name, session_id):
        url_session = f"{self.pixelbot_url}{self.FILE_ENDPOINT}{child_name}{self.SLASH}{session_id}"
        
        resp = requests.get(url_session)
        # If not successful, return None
        if resp.status_code != 200:
            return None

        files = resp.json().get("files", [])

        # Return the URL of the first .png file found
        for file in files:
            if file.endswith(self.GRAPHIC_FILE_FORMAT):
                return f"{url_session}{self.SLASH}{file}"
        return None

    ''' Extract the session date from the drawing file name (format: DD-MM-YYYY). Returns a datetime object or None if not found. '''    
    def extract_day_from_file_url(self, file_url):
        # Extract the session date 
        file_name = os.path.basename(file_url)
        # remove extension (.png)
        base_name = os.path.splitext(file_name)[0]

        # Extract DD-MM-YYYY 
        match = re.search(r"(\d{2}-\d{2}-\d{4})", base_name)

        #if the file has  name matching the date format, return the date 
        if match:
            date = match.group(1)
            # Convert string date to datetime object
            return datetime.datetime.strptime(date, "%d-%m-%Y")
        return None
    
    ''' Parse the transcript text into a structured list of dictionaries with speaker and message. 
        Assumes format "Speaker: Message" per line. '''
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

    ''' Parse the story summary text (which is expected to be a JSON string) into a structured list of dictionaries 
        with object name and description.'''
    def parse_story_summary(self, text):  
        try:
            object_dict = json.loads(text)
        except json.JSONDecodeError:
            return []
        summary_list = []
        for name, description in object_dict.items():
            summary_list.append({
                "name": name,
                "description": description
            })
        return summary_list

