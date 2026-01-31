# child_api.py
from pixelbot_storage.DataRepository import DataRepository

class ChildAPI:
    def __init__(self, repository: DataRepository):
        self.repository = repository

    def send_children(self):
        children = self.repository.load_children()
        # Serialize each child to a dictionary
        return [
            {
                "childId": child.get("childId"),
                "name": child.get("name"),
                # Creates a list of sessions for each child
                "sessions": [
                    {"sessionId": s["sessionId"]} for s in child.get("sessions", [])
                ]
            }
            for child in children
        ]

    def send_child(self, child_id):
        child = self.repository.get_child(child_id)
        if not child:
            return None
        # Serialize child to a dictionary
        return {
            "childId": child.get("childId"),
            "name": child.get("name"),
            # Creates a list of sessions for the child
            "sessions": [
                {"sessionId": s["sessionId"]} for s in child.get("sessions", [])
            ]
        }