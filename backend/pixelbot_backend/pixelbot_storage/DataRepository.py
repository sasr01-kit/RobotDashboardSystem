from pixelbot_model.Child import Child
from pixelbot_model.Session import Session
import json
import os
from datetime import datetime

"Repository to save and load Child and Session data as JSON files"

class DataRepository:
    DATA_FILE = "children_data.json"
    #  stores metadata such as when the data was last updated
    META_FILE = "children_meta.json"

    # save child as JSON
    def save_children(self, children_objects):
        # Convert Child objects to dictionaries
        children_dicts = [child.to_dict() for child in children_objects]
        # Save to JSON file. This file can now be read anytime.
        with open(self.DATA_FILE, 'w') as f:
            json.dump(children_dicts, f, indent=4)

        # Save metadata
        meta = {
            "last_updated": datetime.now().isoformat()
        }   
        with open(self.META_FILE, 'w') as f:
            json.dump(meta, f, indent=4) 

        # Log success message, optional, only for debugging
        # print("[Repository] Successfully saved children data.")
    
    # load child from JSON
    def load_children(self):
        if not os.path.exists(self.DATA_FILE):
            # message, optional, only for debugging
            # print("[Repository] No data file found.")
            return None

        # Read JSON file
        with open(self.DATA_FILE, 'r') as f:
            children_dicts = json.load(f)

        # Convert dictionaries back to Child objects
        children_objects = []
        for child_dict in children_dicts:
            sessions = []
            for session_dict in child_dict['sessions']:
                session = Session.from_dict(session_dict)
                sessions.append(session)
            child = Child(child_dict['child_id'], child_dict['name'], sessions)
            children_objects.append(child)

        # Log success message, optional, only for debugging
        # print("[Repository] Successfully loaded children data.")
        return children_objects
    
    # get last updated time
    def get_last_updated(self):
        if not os.path.exists(self.META_FILE):
            # message, optional, only for debugging
            # print("[Repository] No meta file found.")
            return None

        with open(self.META_FILE, 'r') as f:
            meta = json.load(f)

        last_updated_str = meta.get("last_updated", None)
        if last_updated_str:
            return datetime.fromisoformat(last_updated_str)
        return None