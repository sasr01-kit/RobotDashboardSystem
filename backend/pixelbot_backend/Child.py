class Child:
    def __init__(self, child_id: str, name: str, sessions: list):
        self.child_id = child_id
        self.name = name
        self.sessions = sessions  # List of Session objects
    
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

