# FeedbackLogEntry.py

class FeedbackLogEntry:
    def __init__(
        self,
        duration: str = "",
        start_point: str = "",
        end_point: str = "",
        feedback: str = "",
    ) -> None:
        self._duration = duration
        self._start_point = start_point
        self._end_point = end_point
        self._feedback = feedback

    # Getters
    def get_duration(self) -> str:
        return self._duration

    def get_start_point(self) -> str:
        return self._start_point

    def get_end_point(self) -> str:
        return self._end_point

    def get_feedback(self) -> str:
        return self._feedback

    # Setters
    def set_duration(self, value: str) -> None:
        self._duration = value

    def set_start_point(self, value: str) -> None:
        self._start_point = value

    def set_end_point(self, value: str) -> None:
        self._end_point = value

    def set_feedback(self, value: str) -> None:
        self._feedback = value
