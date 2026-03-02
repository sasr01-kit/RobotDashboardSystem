
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository 
from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI 
from pixelbot_backend.pixelbot_controller.SessionAPI import SessionAPI
from pixelbot_backend.pixelbot_controller.GlobalMetricsAPI import GlobalMetricsAPI

#Test file. Test if global summary method is sending all the data.
repository = DataRepository() 
# Set this to your local data folder or the pixelbot robot's URL: http://192.168.2.70:8000
child_api = ChildAPI("C:/Users/aneca/OneDrive/Uni/pse_data_example/saved_drawing", repository) 
global_metrics_api = GlobalMetricsAPI(child_api)
print(global_metrics_api.send_global_metrics_summary())
