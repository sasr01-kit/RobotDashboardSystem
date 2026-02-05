from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository
from pixelbot_backend.pixelbot_controller.GlobalMetricsAPI import GlobalMetricsAPI

repository = DataRepository() 
api = ChildAPI("C:/Users/aneca/OneDrive/Uni/pse_data_example/saved_drawing", repository)
print(api.get_recap_data("07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e"))

globalAPI = GlobalMetricsAPI(api)  # child_api not needed for this test
recap = globalAPI.send_child_recap("07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e")

print(recap)