from pixelbot_backend.pixelbot_storage.RemoteDataLoader import RemoteDataLoader
import requests
import threading
import time
from datetime import datetime

'''ChildAPI is responsible for managing the child data, including loading from the repository, refreshing from the source (robot), 
    and providing an API to send child data to the frontend. 
    It also includes a background thread that periodically checks for robot availability and refreshes data accordingly.'''
class ChildAPI:

    def __init__(self, data_root, repository, refresh_interval_seconds = 60):
        # Store the root path (can be a URL or local directory) and repository for saving/loading children
        self.data_root = data_root
        self.repository = repository
        self.refresh_interval_seconds = refresh_interval_seconds

    '''Start the background thread for refreshing data from the source. This should be called once when the application starts.'''
    def start(self):
        threading.Thread(target=self.background_refresh, daemon=True).start()

    '''Load all children from the repository, returning a list of Child objects.'''
    def load_children_objects(self):
        return self.repository.load_children() or []    
    
    '''Refresh the data from the source (e.g. robot) if available, and update the repository with the new data. 
        The data needs to be snychronized to the system once per session or at the end of the day.'''
    def background_refresh(self):
        robot_was_available = False
        while True:
            # just checking availability every minute to see if robot came online or if it's end of day for daily sync.
            time.sleep(60)  
            now = datetime.now()
            robot_is_available = self.is_robot_available(self.data_root)

            # Trigger 1: robot just came online (only syncs once per session)
            if robot_is_available and not robot_was_available:
                self.refresh_from_source() 

             # Trigger 2: end of day sync (e.g. 20:00)
            is_end_of_day = now.hour == 20 and now.minute < 1

            if is_end_of_day and robot_is_available:
                self.refresh_from_source()
            
            # Update state for next iteration to correctly detect robot availability changes
            robot_was_available = robot_is_available

    '''Refresh the children data from the source (e.g. robot) if the robot is available, and update the repository with the new data.'''
    def refresh_from_source(self):
        try:
            if self.data_root.startswith("http://") and self.is_robot_available(self.data_root):
                raw_children = RemoteDataLoader(self.data_root).load_all_children()
                self.repository.update_children(raw_children)
        except Exception as e:
            print(f"Refresh failed: {e}")

    
    ''' Check if the robot is available at the given URL '''
    def is_robot_available(self, url: str) -> bool:
        try:
            requests.head(url, timeout=1)
            return True
        except Exception:
            print(f"Robot not available at {url}")
            return False
    
    ''' Sends children data to the frontend by loading from the repository and converting to dictionaries. '''
    def send_children(self):
        children = self.load_children_objects()
        return [child.to_dict() for child in children]
    
    

    


    

