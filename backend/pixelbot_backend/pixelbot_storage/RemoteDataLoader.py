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
        # Remove trailiing slash to avoid double slashes in URLs
        self.pixelbot_url = pixelbot_url.rstrip(self.SLASH)

    def load_all_children(self):
        children = []
        resp = requests.get(f"{self.pixelbot_url}{self.CHILDREN_ENDPOINT}")
        children_names = resp.json()[self.JSON_KEY_CHILDREN]
        for child_name in children_names:
            child = self.load_child(child_name)
            children.append(child)
        return children


    def load_child(self, child_name):
        sessions = []
        # Get sessions for this child with the structured URL: pixelbot_url/child_name/sessions
        resp = requests.get(f"{self.pixelbot_url}{self.SLASH}{child_name}{self.SESSIONS_ENDPOINT}")
        session_ids = resp.json()[self.JSON_KEY_SESSIONS]

        for session_id in session_ids:
            session = self.load_session(child_name, session_id)
            sessions.append(session)  
        return Child(None, child_name, sessions)


    def load_session(self, child_name, session_id):
        # get drawing file path name. Then extract the date of the session 
        drawing_file_url = self.get_drawing_file(child_name, session_id)
        session_date = self.extract_day_from_file_url(drawing_file_url)
        
        resp = requests.get(drawing_file_url)
        drawing = DrawingData(resp.json()["base64"])

        transcript_text = self.loadTxt(child_name, session_id, self.TRANSCRIPT_FILE_NAME)
        transcript = self.parse_transcript(transcript_text)

        story_summary_text = self.loadTxt(child_name, session_id, self.STORY_SUMMARY_FILE_NAME)
        story_summary = self.parse_story_summary(story_summary_text)

        speech_depth_path = self.get_file_url(child_name, session_id, self.SPEECH_DEPTH_CSV)
        speech_width_path = self.get_file_url(child_name, session_id, self.SPEECH_WIDTH_CSV)
        drawing_width_path = self.get_file_url(child_name, session_id, self.DRAWING_WIDTH_CSV)

        speech_width = SpeechSelfDisclosureWidth(**self.loadCsv(speech_width_path))
        speech_depth = SpeechSelfDisclosureDepth(**self.loadCsv(speech_depth_path))
        drawing_width = DrawingSelfDisclosureWidth(**self.loadCsv(drawing_width_path))

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

    def get_file_url(self, child_name, session_id, filename):
        # Returns the URL to the file on Pixelbot with the structure:
        # pixelbot_url/file/child_name/session_id/filename
        return f"{self.pixelbot_url}{self.FILE_ENDPOINT}{child_name}{self.SLASH}{session_id}{self.SLASH}{filename}"

    def loadTxt(self, child_name, session_id, filename):
        url = self.get_file_url(child_name, session_id, filename)
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text
        return self.EMPTY_STRING

    def loadCsv(self, file_path):
        resp = requests.get(file_path)
        # If successful, read CSV into dictionary
        if resp.status_code == 200:
            # Use io.StringIO to treat the response text as a file
            f = io.StringIO(resp.text)
            reader = csv.DictReader(f)
            return next(reader)
        return {}
    
    def get_drawing_file(self, child_name, session_id):
        # Returns the URL to the file on Pixelbot with the structure:
        # pixelbot_url/file/child_name/session_id
        url_session = f"{self.pixelbot_url}{self.FILE_ENDPOINT}{child_name}{self.SLASH}{session_id}"
        
        resp = requests.get(url_session)
        if resp.status_code != 200:
            return None

        files = resp.json().get("files", [])

        for file in files:
            if file.endswith(self.GRAPHIC_FILE_FORMAT):
                return f"{url_session}{self.SLASH}{file}"
        return None
        
    def extract_day_from_file_url(self, file_url):
        file_name = os.path.basename(file_url)
        # remove extension (.png)
        base_name = os.path.splitext(file_name)[0]

        # Extract DD-MM-YYYY 
        match = re.search(r"(\d{2}-\d{2}-\d{4})", base_name)
        #return date object
        if match:
            date = match.group(1)
            return datetime.datetime.strptime(date, "%d-%m-%Y")
        return None
    
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
        except json.JSONDecodeError:
            return []
        summary_list = []
        for name, description in object_dict.items():
            summary_list.append({
                "name": name,
                "description": description
            })
        return summary_list

