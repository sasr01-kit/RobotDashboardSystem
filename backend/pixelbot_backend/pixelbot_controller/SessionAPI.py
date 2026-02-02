# session_api.py

class SessionAPI:

    def __init__(self, child_api):
        self.child_api = child_api
        self.children = self.child_api._load_children_objects()

    def send_session(self, child_id, session_id):
        for child in self.children:
            if child.child_id == child_id:
                for session in child.sessions:
                    if session.session_id == session_id:
                        return session.to_dict()

        return None
    
    
    def send_all_sessions(self):
        all_sessions = []

        for child in self.children:
            for session in child.sessions:
                session_dict = session.to_dict()
                # add child ID to session data
                session_dict["childId"] = child.child_id
                all_sessions.append(session_dict)
