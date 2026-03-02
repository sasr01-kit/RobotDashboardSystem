
from pixelbot_backend.pixelbot_storage.RemoteDataLoader import RemoteDataLoader
from pixelbot_backend.pixelbot_storage.DataLoader import DataLoader
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository
repo = DataRepository() 
# Use only if you're connected to Pixelbot. 
dl = RemoteDataLoader("http://192.168.2.70:8000")
raw_children = dl.load_all_children()
children = repo.update_children(raw_children)
for child in children:
    print(child.get_id())
    for session in child.sessions:
        print(session.session_id, session.story_summary[:100])
        
