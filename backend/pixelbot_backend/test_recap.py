from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository
from pixelbot_backend.pixelbot_controller.GlobalMetricsAPI import GlobalMetricsAPI

repository = DataRepository() 
api = ChildAPI("C:/Users/aneca/OneDrive/Uni/pse_data_example/saved_drawing", repository)

globalAPI = GlobalMetricsAPI(api)  
recap = globalAPI.send_child_recap("2360809f47514450b4d4437dd9a857b0")

print(recap)