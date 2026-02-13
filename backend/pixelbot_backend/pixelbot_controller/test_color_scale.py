
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository 
from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI 
from pixelbot_backend.pixelbot_controller.SessionAPI import SessionAPI
from pixelbot_backend.pixelbot_controller.GlobalMetricsAPI import GlobalMetricsAPI

repository = DataRepository() 
child_api = ChildAPI("C:/Users/aneca/OneDrive/Uni/pse_data_example/saved_drawing", repository) 
global_metrics_api = GlobalMetricsAPI(child_api)
print(global_metrics_api.send_global_metrics_summary())
