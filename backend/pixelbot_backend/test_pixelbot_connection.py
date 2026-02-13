
from pixelbot_storage.RemoteDataLoader import RemoteDataLoader
from pixelbot_storage.DataLoader import DataLoader
 
# Use only if you're connected to Pixelbot. 
dl = RemoteDataLoader("http://192.168.2.70:8000")
children = dl.load_all_children()
for child in children:
    print(child.get_id())
    for session in child.sessions:
        print(session.session_id, session.story_summary[:100])
        print()
        
# Use only if you're reading the files from your laptop.
dl = DataLoader("/mnt/c/Users/kelly/Desktop/Uni/PSE/pse_data_example/saved_drawing")

children = dl.load_all_children()
for child in children:
    print(child.get_id())
    for session in child.sessions:
        print(session.session_id, session.story_summary[:100])
        print()