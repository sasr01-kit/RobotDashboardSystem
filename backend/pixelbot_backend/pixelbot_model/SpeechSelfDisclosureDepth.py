
class SpeechSelfDisclosureDepth:
    def __init__(self, average_intimacy_score: float, std_intimacy_score: float):
        self.average_intimacy_score = average_intimacy_score
        self.std_intimacy_score = std_intimacy_score

    def to_dict(self):
        return {
            "average_intimacy_score": self.average_intimacy_score,
            "std_intimacy_score": self.std_intimacy_score
        }
    
    def getAvgIntimacyScore(self):
        return self.average_intimacy_score
    
    def getStdIntimacyScore(self):
        return self.std_intimacy_score
    
    @staticmethod
    def from_dict(data):
        return SpeechSelfDisclosureDepth(
            average_intimacy_score=data["average_intimacy_score"],
            std_intimacy_score=data["std_intimacy_score"]
        )