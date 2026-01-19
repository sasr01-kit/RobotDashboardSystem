# Feedback.py
from typing import List, Dict, Any

from PathLogEntry import PathLogEntry
from FeedbackLogEntry import FeedbackLogEntry


class Feedback:
    def __init__(self) -> None:
        self._path_history: List[PathLogEntry] = []
        self._total_good_ratings: int = 0
        self._total_bad_ratings: int = 0
        self._feedback_history: List[FeedbackLogEntry] = []

    # Getters
    def get_path_history(self) -> List[PathLogEntry]:
        return self._path_history

    def get_total_good_ratings(self) -> int:
        return self._total_good_ratings

    def get_total_bad_ratings(self) -> int:
        return self._total_bad_ratings

    def get_feedback_history(self) -> List[FeedbackLogEntry]:
        return self._feedback_history

    # Setters
    def set_path_history(self, history: List[PathLogEntry]) -> None:
        self._path_history = history

    def set_total_good_ratings(self, value: int) -> None:
        self._total_good_ratings = value

    def set_total_bad_ratings(self, value: int) -> None:
        self._total_bad_ratings = value

    def set_feedback_history(self, history: List[FeedbackLogEntry]) -> None:
        self._feedback_history = history

    # Core behavior

    def calculate_feedback_ratio(self, path_history: List[PathLogEntry]) -> float:
        """
        Calculates the percentage of good feedback over all path entries
        that contain user feedback.
        """
        if not path_history:
            return 0.0

        good = 0
        total = 0

        for entry in path_history:
            feedback = entry.get_user_feedback()
            if feedback is not None:
                total += 1
                if feedback.lower() == "good":
                    good += 1

        if total == 0:
            return 0.0

        self._total_good_ratings = good
        self._total_bad_ratings = total - good

        return good / total

    def update_feedback_log(self, path_history: List[PathLogEntry]) -> None:
        """
        Creates FeedbackLogEntry objects for any PathLogEntry that now
        contains user feedback and has not yet been logged.
        """
        self._path_history = path_history

        for entry in path_history:
            feedback = entry.get_user_feedback()
            if feedback is None:
                continue

            # Check if this entry has already been logged
            already_logged = any(
                log.get_start_point() == entry.get_id()
                for log in self._feedback_history
            )

            if not already_logged:
                log = FeedbackLogEntry(
                    duration=str(entry.get_timestamp()),
                    start_point=entry.get_label(),
                    end_point=entry.get_goal_type(),
                    feedback=feedback,
                )
                self._feedback_history.append(log)

    def toJSON(self) -> Dict[str, Any]:
        return {
            "totalGoodRatings": self._total_good_ratings,
            "totalBadRatings": self._total_bad_ratings,
            "feedbackRatio": (
                self._total_good_ratings /
                (self._total_good_ratings + self._total_bad_ratings)
                if (self._total_good_ratings + self._total_bad_ratings) > 0
                else 0.0
            ),
            "feedbackHistory": [
                {
                    "duration": f.get_duration(),
                    "startPoint": f.get_start_point(),
                    "endPoint": f.get_end_point(),
                    "feedback": f.get_feedback(),
                }
                for f in self._feedback_history
            ],
        }

    def fromJSON(self, msg: Dict[str, Any]) -> None:
        """
        Interprets user interaction data sent from the frontend.
        Expected to carry feedback for a specific PathLogEntry.
        """
        entry_id = msg.get("id")
        feedback = msg.get("feedback")

        if entry_id is None:
            return

        for entry in self._path_history:
            if entry.get_id() == entry_id:
                entry.set_user_feedback(feedback)
                break
