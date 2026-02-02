import pixelbot_backend.pixelbot_utils.Utils as Utils   

class GlobalMetricsAPI:
    children = []

    def __init__(self, child_api):
        self.child_api = child_api 
        self.children = self.child_api._load_children_objects() 

    def send_global_metrics(self):


        return {
            "totalSessions": total_sessions,
            "SessionsPerChild": self.calculate_average_sessions_per_child(total_sessions)           
        }
    
    def calculate_average_sessions_per_child(self):
        total_sessions = sum(child.get_number_of_sessions() for child in self.children)
        total_children = len(self.children)
        average_sessions = total_sessions / total_children if total_children > 0 else 0

        return {
            "averageSessionsPerChild": average_sessions
        }