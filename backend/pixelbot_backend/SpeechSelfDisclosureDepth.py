
class SpeechSelfDisclosureDepth:
    def __init__(self, avg_intimacy_score: float, std_intimacy_score: float):
        self.avg_intimacy_score = avg_intimacy_score
        self.std_intimacy_score = std_intimacy_score

    def to_dict(self):
        return {
            "avgIntimacyScore": self.avg_intimacy_score,
            "stdIntimacyScore": self.std_intimacy_score
        }
    
    def getAvgIntimacyScore(self):
        return self.avg_intimacy_score
    
    def getStdIntimacyScore(self):
        return self.std_intimacy_score