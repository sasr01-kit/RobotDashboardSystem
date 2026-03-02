from pixelbot_backend.pixelbot_storage.RemoteDataLoader import RemoteDataLoader
from pixelbot_backend.pixelbot_storage.DataLoader import DataLoader
import os
import requests

class ChildAPI:

    def __init__(self, data_root, repository):
        # Store the root path (can be a URL or local directory) and repository for saving/loading children
        self.data_root = data_root
        self.repository = repository

    def load_children_objects(self):
        children = []
        # If data_root is a URL, try to load children from the robot remotely
        if self.data_root.startswith("http://") and self.is_robot_available(self.data_root):
            try: 
                # Use RemoteDataLoader to fetch children from the robot
                raw_children = RemoteDataLoader(self.data_root).load_all_children()          
                # Update repository with new children (handles ID assignment and persistence)
                children = self.repository.update_children(raw_children)
                return children
            except Exception as e:
                print("Remote load failed:", e)

        # If data_root is a local directory, try to load children from local files
        elif os.path.exists(self.data_root):
            print(f"Loading children from local directory: {self.data_root}")
            try:
                # Use DataLoader to fetch children from local data
                raw_children = DataLoader(self.data_root).load_all_children()
                children = self.repository.update_children(raw_children)
                return children
            except Exception as e:
                print("Local load failed:", e)
        
        
        # If neither remote nor local loading is possible, fall back to stored data in repository
        print("Falling back to repository data...")
        return self.repository.load_children() or []

    def is_robot_available(self, url: str) -> bool:
        try:
            requests.head(url, timeout=1)
            return True
        except Exception:
            print(f"Robot not available at {url}")
            return False


    # Public API function to return children
    def send_children(self):
        children = self.load_children_objects()
        return [child.to_dict() for child in children]
    
    

    


    

