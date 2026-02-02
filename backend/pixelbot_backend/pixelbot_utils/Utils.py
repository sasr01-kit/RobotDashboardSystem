class Utils:
    @staticmethod
    def calculate_average(values: list):
        if not values:
            return 0.0  
        return sum(values) / len(values) 

    @staticmethod
    def calculate_average_sessions_per_child(children: list):
        total_sessions = sum(child.get_number_of_sessions() for child in children)
        total_children = len(children)
        return total_sessions / total_children if total_children > 0 else 0       
