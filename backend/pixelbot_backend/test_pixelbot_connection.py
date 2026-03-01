
from pixelbot_backend.pixelbot_storage.RemoteDataLoader import RemoteDataLoader
from pixelbot_backend.pixelbot_storage.DataLoader import DataLoader
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository
 
# Use only if you're connected to Pixelbot. 
'''dl = RemoteDataLoader("http://192.168.2.70:8000")
children = dl.load_all_children()
for child in children:
    print(child.get_id())
    for session in child.sessions:
        print(session.session_id, session.story_summary[:100])
        print()'''
        
# Use only if you're reading the files from your laptop.



repo = DataRepository() 
dl = DataLoader("C:/Users/aneca/OneDrive/Uni/pse_data_example/saved_drawing")

raw_children = dl.load_all_children()
children = repo.update_children(raw_children)
for child in children:
    print(child.get_id())
    for session in child.sessions:
        print(session.session_id, session.story_summary[:100])
        print()