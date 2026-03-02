# session_api.py

class SessionAPI:

    def __init__(self):
        pass

    def send_session(self, child_id, session_id, children):
        for child in children:
            if child.child_id == child_id:
                for session in child.sessions:
                    
        # Return the session data as a dictionary (for JSON response)
                    if session.get_session_id() == session_id:
                        return session.to_dict()

        return None
    
    
    def send_all_sessions(self, children):
        all_sessions = []

        for child in children:
            for session in child.sessions:
                session_dict = session.to_dict()
                # add child ID to session data
                session_dict["childId"] = child.child_id
            
        # Returns a list of all session dictionaries, each with its childId
                all_sessions.append(session_dict)
