from pixelbot_backend.pixelbot_model.Child import Child
from pixelbot_backend.pixelbot_model.Session import Session
import json
import os
from datetime import datetime
import uuid

"Repository to save and load Child and Session data as JSON files"

class DataRepository:
    def __init__(self):
        
        # Get the absolute directory path of this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Build absolute paths to JSON files 
        self.DATA_FILE = os.path.join(base_dir, "children_data.json") 
        self.META_FILE = os.path.join(base_dir, "children_meta.json")

    # save child as JSON
    def save_children(self, children_objects):
        # Convert Child objects to dictionaries
        children_dicts = [child.to_dict() for child in children_objects]
        # Save to JSON file. This file can now be read anytime.
        with open(self.DATA_FILE, 'w') as f:
            json.dump(children_dicts, f, indent=4)

        # Save metadata
        meta = {
            "last_updated": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        }   
        with open(self.META_FILE, 'w') as f:
            json.dump(meta, f, indent=4) 
    

    def update_children(self, raw_children):       
        # load already saved children
        existing_children = self.load_children()
        
        # Build a lookup dictionary by child name for quick access
        existing_by_name = {c.name: c for c in existing_children}

        children = []

        for child in raw_children:
            
            # If child already exists, reuse its child_id
            if child.name in existing_by_name:
                child.child_id = existing_by_name[child.name].child_id
            
            # If child_id is missing, generate a new unique ID
            if child.child_id is None:
                id = uuid.uuid4().hex
                child.child_id = id
            
            children.append(child)
        
        # Save the updated children list to disk    
        self.save_children(children)
        return children


    # Load children from the JSON file
    def load_children(self):
        
        # If the data file doesn't exist, return an empty list
        if not os.path.exists(self.DATA_FILE):
            return []

        # Read the JSON file into a list of dictionaries
        with open(self.DATA_FILE, 'r') as f:
            children_dicts = json.load(f)

        # Convert dictionaries back to Child objects
        children_objects = []
        for child_dict in children_dicts:
            sessions = []
            for session_dict in child_dict['sessions']:       
                # Use Session.from_dict to reconstruct each session
                session = Session.from_dict(session_dict)
                sessions.append(session)
                
            # Rebuild the Child object with its sessions
            child = Child(child_dict['child_id'], child_dict['name'], sessions)
            children_objects.append(child)

        return children_objects
    
    # get last updated time (for testing purposes)
    def get_last_updated(self):
        # If the meta file doesn't exist, return None
        if not os.path.exists(self.META_FILE):
            return None

        # Read the meta file and extract the last_updated string
        with open(self.META_FILE, 'r') as f:
            meta = json.load(f)

        last_updated_str = meta.get("last_updated", None)
        
        # Convert the string to a datetime object if present
        if last_updated_str:
            return datetime.fromisoformat(last_updated_str)
        return None