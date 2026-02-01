import pixelbot_backend.pixelbot_model.Session as Session
from typing import List

class Child:
    def __init__(self, child_id: str, name: str, sessions: List[Session]):
        self.child_id = child_id
        self.name = name
        self.sessions = sessions  # List of Session objects

    def to_dict(self):
        return {
            "child_id": self.child_id,
            "name": self.name,
            "sessions": [session.to_dict() for session in self.sessions]
        }    
    
    def get_id(self): 
        return self.child_id

    def get_name(self):
        return self.name

    def get_sessions(self):
        return self.sessions

    def get_session_by_id(self, session_id: str):
        for session in self.sessions:
            if session.session_id == session_id:
                return session
        return None

    def get_session_ids(self):
        return [session.session_id for session in self.sessions]
    
    def get_number_of_sessions(self):
        return len(self.sessions)

    @staticmethod
    def from_dict(data):
        sessions = [Session.from_dict(s) for s in data.get("sessions", [])]
        return Child(
            child_id=data["child_id"],
            name=data["name"],
            sessions=sessions
        )
