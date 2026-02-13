# child_api.py
from pixelbot_backend.pixelbot_storage.RemoteDataLoader import RemoteDataLoader
from pixelbot_backend.pixelbot_storage.DataLoader import DataLoader
import os

class ChildAPI:

    def __init__(self, data_root, repository):
        self.data_root = data_root
        self.repository = repository

    def load_children_objects(self):
        if self.data_root.startswith("http://"): 
            # if pixelbot connections fails, JSON file with children data remains safe
            try:
                # use RemoteDataLoader if using pixelbot connection
                children = RemoteDataLoader(self.data_root).load_all_children()
            except Exception as e:
                print("Remote load failed:", e)
    
            # save fresh data to repository
            self.repository.save_children(children)
            return children

        # Use locally robot data
        elif os.path.exists(self.data_root):
            children = DataLoader(self.data_root).load_all_children()
            # save fresh data to repository
            self.repository.save_children(children)
            return children
        
        # Fallback to stored data
        return self.repository.load_children() or []

    # Public API function
    def send_children(self):
        children = self.load_children_objects()
        return [child.to_dict() for child in children]

    def send_child(self, child_id):
        children = self.load_children_objects()
        for child in children:
            if child.child_id == child_id:
                return child.to_dict()
        return None
    
    

    


    

