
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
            "interventionCount": self.intervention_count,
            "totalWordCount": self.total_word_count,
            "avgWordCountPerIntervention": self.average_word_count_per_intervention,
            "stdWordCountPerIntervention": self.std_word_count_per_intervention,
            "totalSpeechTime": self.total_speech_time,
            "avgSpeechTimePerIntervention": self.average_speech_time_per_intervention,
            "stdSpeechTimePerIntervention": self.std_speech_time_per_intervention
        }
    
    def getInterventionCount(self):
        return self.intervention_count
    
    def getTotalWordCount(self):
        return self.total_word_count
    
    def getAvgWordCountPerIntervention(self):
        return self.average_word_count_per_intervention
    
    def getStdWordCountPerIntervention(self):
        return self.std_word_count_per_intervention
    
    def getTotalSpeechTime(self):
        return self.total_speech_time
    
    def getAvgSpeechTimePerIntervention(self):
        return self.average_speech_time_per_intervention
    
    def getStdSpeechTimePerIntervention(self):
        return self.std_speech_time_per_intervention
    
    @staticmethod
    def from_dict(data):
        return SpeechSelfDisclosureWidth(
            intervention_count=data["interventionCount"],
            total_word_count=data["totalWordCount"],
            average_word_count_per_intervention=data["avgWordCountPerIntervention"],
            std_word_count_per_intervention=data["stdWordCountPerIntervention"],
            total_speech_time=data["totalSpeechTime"],
            average_speech_time_per_intervention=data["avgSpeechTimePerIntervention"],
            std_speech_time_per_intervention=data["stdSpeechTimePerIntervention"]
        )