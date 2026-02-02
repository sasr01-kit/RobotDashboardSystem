import pixelbot_backend.pixelbot_utils.Utils as Utils   

class GlobalMetricsAPI:
    children = []

    def __init__(self, child_api):
        self.child_api = child_api 
        self.children = self.child_api._load_children_objects() 

    def send_global_metrics(self):
        total_sessions = sum(child.get_number_of_sessions() for child in self.children)
        sessions_per_child = Utils.calculate_average_sessions_per_child(self.children)

        return {
            "totalSessions": total_sessions,
            "SessionsPerChild": sessions_per_child        
        }