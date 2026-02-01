# session_api.py
from pixelbot_storage.DataRepository import DataRepository

class SessionAPI:
    def __init__(self, repository: DataRepository):
        self.repository = repository

    def send_session(self, child_id, session_id):
        children = self.repository.load_children()

        for child in children:
            if child.get("childId") == child_id:
                for session in child.get("sessions", []):
                    if session.get("sessionId") == session_id:
                        # Serialize session to a dictionary
                        return {
                            "sessionId": session.get("sessionId"),
                            "storySummary": session.get("storySummary"),
                            "transcript": session.get("transcript"),
                            "drawing": session.get("drawing", {}),
                            "speechWidth": session.get("speechWidth", {}),
                            "speechDepth": session.get("speechDepth", {}),
                            "drawingWidth": session.get("drawingWidth", {}),
                        }
        return None