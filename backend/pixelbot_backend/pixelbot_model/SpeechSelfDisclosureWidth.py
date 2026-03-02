
class SpeechSelfDisclosureWidth:
    def __init__(self, intervention_count: int, total_word_count: int, average_word_count_per_intervention: float,
                 std_word_count_per_intervention: float, total_speech_time: float, average_speech_time_per_intervention: float,
                 std_speech_time_per_intervention: float):
        self.intervention_count = intervention_count
        self.total_word_count = total_word_count
        self.average_word_count_per_intervention = average_word_count_per_intervention
        self.std_word_count_per_intervention = std_word_count_per_intervention
        self.total_speech_time = total_speech_time
        self.average_speech_time_per_intervention = average_speech_time_per_intervention
        self.std_speech_time_per_intervention = std_speech_time_per_intervention

    def to_dict(self):
        return {
            "intervention_count": self.intervention_count,
            "total_word_count": self.total_word_count,
            "average_word_count_per_intervention": self.average_word_count_per_intervention,
            "std_word_count_per_intervention": self.std_word_count_per_intervention,
            "total_speech_time": self.total_speech_time,
            "average_speech_time_per_intervention": self.average_speech_time_per_intervention,
            "std_speech_time_per_intervention": self.std_speech_time_per_intervention,
        }
    
    def get_intervention_count(self):
        return self.intervention_count
    
    def get_total_word_count(self):
        return self.total_word_count
    
    def get_avg_word_count_per_intervention(self):
        return self.average_word_count_per_intervention
    
    def get_std_word_count_per_intervention(self):
        return self.std_word_count_per_intervention
    
    def get_total_speech_time(self):
        return self.total_speech_time
    
    def get_avg_speech_time_per_intervention(self):
        return self.average_speech_time_per_intervention
    
    def get_std_speech_time_per_intervention(self):
        return self.std_speech_time_per_intervention
    
    @staticmethod
    def from_dict(data):
        return SpeechSelfDisclosureWidth(
            intervention_count=data["intervention_count"],
            total_word_count=data["total_word_count"],
            average_word_count_per_intervention=data["average_word_count_per_intervention"],
            std_word_count_per_intervention=data["std_word_count_per_intervention"],
            total_speech_time=data["total_speech_time"],
            average_speech_time_per_intervention=data["average_speech_time_per_intervention"],
            std_speech_time_per_intervention=data["std_speech_time_per_intervention"]
        )