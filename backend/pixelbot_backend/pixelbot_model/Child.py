from pixelbot_backend.pixelbot_model.Session import Session

'''Child represents a child user of the Pixelbot robot, containing their unique ID, name, and a list of their sessions.'''
class Child:
    def __init__(self, child_id: str, name: str, sessions: list):
        self.child_id = child_id
        self.name = name
        self.sessions = self.order_sessions_by_id(sessions)  # List of Session objects

    '''Convert the Child object to a dictionary for JSON serialization.'''
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
    
    def get_drawings(self):
        drawings = []
        for session in self.sessions:
            if session.drawing:
             drawings.append(session.drawing)
        return drawings

    def get_session_by_id(self, session_id: str):
        for session in self.sessions:
            if session.session_id == session_id:
                return session
        return None

    def get_session_ids(self):
        return [session.session_id for session in self.sessions]
    
    def get_number_of_sessions(self):
        return len(self.sessions)
    
    def get_total_word_count(self):
        return sum(int(session.get_total_word_count()) for session in self.sessions)
    
    def get_avg_intimacy_score(self):
        total_score = sum(session.get_avg_intimacy_score() for session in self.sessions)
        return total_score / len(self.sessions)

    def order_sessions_by_id(self, sessions):
        return sorted(sessions, key=lambda session: int(session.session_id.split("_")[1]))

    ''''Reconstruct a Child object from a dictionary (loaded from JSON)'''
    @staticmethod
    def from_dict(data):
        sessions = [Session.from_dict(s) for s in data.get("sessions", [])]
        return Child(
            child_id=data["child_id"],
            name=data["name"],
            sessions=sessions
        )
