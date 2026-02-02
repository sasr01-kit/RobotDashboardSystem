# child_api.py
from pixelbot_storage.DataLoader import DataLoader
import os

class ChildAPI:

    def __init__(self, data_root, repository):
        self.data_root = data_root
        self.repository = repository

    def _load_children_objects(self):
        # Prefer live robot data
        if os.path.exists(self.data_root):
            # use RemoteDataLoader if using robot connection
            children = DataLoader(self.data_root).load_all_children()
            # save fresh data to repository
            self.repository.save_children(children)
            return children
        
        # Fallback to stored data
        return self.repository.load_children() or []

    # Public API function
    def send_children(self):
        children = self._load_children_objects()
        return [child.to_dict() for child in children]

    def send_child(self, child_id):
        children = self._load_children_objects()
        for child in children:
            if child.child_id == child_id:
                return child.to_dict()
        return None