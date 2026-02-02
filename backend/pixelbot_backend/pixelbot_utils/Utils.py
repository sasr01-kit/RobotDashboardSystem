class Utils:
    @staticmethod
    def calculate_average(values: list):
        if not values:
            return 0.0  
        return sum(values) / len(values)        
