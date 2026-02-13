from typing import List, Dict, Any

from PathLogEntry import PathLogEntry
from FeedbackLogEntry import FeedbackLogEntry

class Feedback:
    """Track navigation feedback metrics and history entries."""

    def __init__(self) -> None:
        """Initialize feedback storage and counters.

        Params:
            self: Feedback instance.

        Returns:
            None.
        """
        self._path_history: List[PathLogEntry] = []
        self._total_good_ratings: int = 0
        self._total_bad_ratings: int = 0
        self._feedback_history: List[FeedbackLogEntry] = []

    # Getters
    def get_path_history(self) -> List[PathLogEntry]:
        """Return the stored path history.

        Params:
            self: Feedback instance.

        Returns:
            List[PathLogEntry]: Path log entries associated with this feedback.
        """
        return self._path_history

    def get_total_good_ratings(self) -> int:
        """Return the total count of good ratings.

        Params:
            self: Feedback instance.

        Returns:
            int: Total number of good ratings.
        """
        return self._total_good_ratings

    def get_total_bad_ratings(self) -> int:
        """Return the total count of bad ratings.

        Params:
            self: Feedback instance.

        Returns:
            int: Total number of bad ratings.
        """
        return self._total_bad_ratings

    def get_feedback_history(self) -> List[FeedbackLogEntry]:
        """Return the feedback log history.

        Params:
            self: Feedback instance.

        Returns:
            List[FeedbackLogEntry]: Logged feedback entries.
        """
        return self._feedback_history

    # Setters
    def set_path_history(self, history: List[PathLogEntry]) -> None:
        """Replace the stored path history.

        Params:
            self: Feedback instance.
            history: New path log entries to store.

        Returns:
            None.
        """
        self._path_history = history

    def set_total_good_ratings(self, value: int) -> None:
        """Set the total count of good ratings.

        Params:
            self: Feedback instance.
            value: New total of good ratings.

        Returns:
            None.
        """
        self._total_good_ratings = value

    def set_total_bad_ratings(self, value: int) -> None:
        """Set the total count of bad ratings.

        Params:
            self: Feedback instance.
            value: New total of bad ratings.

        Returns:
            None.
        """
        self._total_bad_ratings = value

    def set_feedback_history(self, history: List[FeedbackLogEntry]) -> None:
        """Replace the feedback log history.

        Params:
            self: Feedback instance.
            history: New feedback log entries to store.

        Returns:
            None.
        """
        self._feedback_history = history

    def calculate_feedback_ratio(self, path_history: List[PathLogEntry]) -> float:
        """Calculate the percentage of good feedback with the currently saved user feedback.

        Params:
            self: Feedback instance.
            path_history: Path log entries to analyze.

        Returns:
            float: Ratio of good feedback over total feedback entries.
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
        """Create feedback log entries for new user feedback.

        Params:
            self: Feedback instance.
            path_history: Path log entries to process.

        Returns:
            None.
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
        """Serialize the feedback state to a JSON-compatible dict.

        Params:
            self: Feedback instance.

        Returns:
            Dict[str, Any]: JSON-compatible feedback.
        """
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
        """Update path entries from user feedback received from frontend.

        Params:
            self: Feedback instance.
            msg: JSON containing feedback updates.

        Returns:
            None.
        """
        entry_id = msg.get("id")
        feedback = msg.get("feedback")

        if entry_id is None:
            return

        for entry in self._path_history:
            if entry.get_id() == entry_id:
                entry.set_user_feedback(feedback)
                break
