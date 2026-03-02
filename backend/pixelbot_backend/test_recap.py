from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository
from pixelbot_backend.pixelbot_controller.GlobalMetricsAPI import GlobalMetricsAPI

repository = DataRepository() 
# Use your path here. If using Pixelbot robot connection, use this path: http://192.168.2.70:8000
api = ChildAPI("C:/Users/aneca/OneDrive/Uni/pse_data_example/saved_drawing", repository)

globalAPI = GlobalMetricsAPI(api)  
# Test the recap method for a specific child ID. Replace with an actual child ID from your data.
recap = globalAPI.send_child_recap("f26fd8a02e104ca0b2bff5244f4c27ef")

print(recap)