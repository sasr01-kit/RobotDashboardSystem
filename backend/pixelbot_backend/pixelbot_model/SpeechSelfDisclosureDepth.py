'''SpeechSelfDisclosureDepth represents the depth of self-disclosure in the child's speech during a session.'''
class SpeechSelfDisclosureDepth:
    def __init__(self, average_intimacy_score: float, std_intimacy_score: float):
        self.average_intimacy_score = average_intimacy_score
        self.std_intimacy_score = std_intimacy_score

    '''Convert the SpeechSelfDisclosureDepth object to a dictionary for JSON serialization.'''
    def to_dict(self):
        return {
            "average_intimacy_score": self.average_intimacy_score,
            "std_intimacy_score": self.std_intimacy_score
        }
    
    def get_avg_intimacy_score(self):
        return float(self.average_intimacy_score)
    
    def get_std_intimacy_score(self):
        return float(self.std_intimacy_score)
    
    '''Reconstruct a SpeechSelfDisclosureDepth object from a dictionary (loaded from JSON)'''
    @staticmethod
    def from_dict(data):
        return SpeechSelfDisclosureDepth(
            average_intimacy_score=data["average_intimacy_score"],
            std_intimacy_score=data["std_intimacy_score"]
        )