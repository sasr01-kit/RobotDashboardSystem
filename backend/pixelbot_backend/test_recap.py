from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository
from pixelbot_backend.pixelbot_controller.GlobalMetricsAPI import GlobalMetricsAPI

repository = DataRepository() 
api = ChildAPI("C:/Users/aneca/OneDrive/Uni/pse_data_example/saved_drawing", repository)

globalAPI = GlobalMetricsAPI(api)  
recap = globalAPI.send_child_recap("f26fd8a02e104ca0b2bff5244f4c27ef")

print(recap)