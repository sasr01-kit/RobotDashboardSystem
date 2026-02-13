class FeedbackLogEntry:
    """Store a single feedback log entry for a completed path segment."""

    def __init__(
        self,
        duration: str = "",
        start_point: str = "",
        end_point: str = "",
        feedback: str = "",
    ) -> None:
        """Initialize a feedback log entry.

        Params:
            self: FeedbackLogEntry instance.
            duration: Duration or timestamp for the path segment.
            start_point: Start location label.
            end_point: End location label.
            feedback: User feedback text.

        Returns:
            None.
        """
        self._duration = duration
        self._start_point = start_point
        self._end_point = end_point
        self._feedback = feedback

    # Getters
    def get_duration(self) -> str:
        """Return the stored duration value.

        Params:
            self: FeedbackLogEntry instance.

        Returns:
            str: Duration or timestamp for the path segment.
        """
        return self._duration

    def get_start_point(self) -> str:
        """Return the stored start point label.

        Params:
            self: FeedbackLogEntry instance.

        Returns:
            str: Start location label.
        """
        return self._start_point

    def get_end_point(self) -> str:
        """Return the stored end point label.

        Params:
            self: FeedbackLogEntry instance.

        Returns:
            str: End location label.
        """
        return self._end_point

    def get_feedback(self) -> str:
        """Return the stored feedback text.

        Params:
            self: FeedbackLogEntry instance.

        Returns:
            str: User feedback text.
        """
        return self._feedback

    # Setters
    def set_duration(self, value: str) -> None:
        """Set the duration value.

        Params:
            self: FeedbackLogEntry instance.
            value: Duration or timestamp for the path segment.

        Returns:
            None.
        """
        self._duration = value

    def set_start_point(self, value: str) -> None:
        """Set the start point label.

        Params:
            self: FeedbackLogEntry instance.
            value: Start location label.

        Returns:
            None.
        """
        self._start_point = value

    def set_end_point(self, value: str) -> None:
        """Set the end point label.

        Params:
            self: FeedbackLogEntry instance.
            value: End location label.

        Returns:
            None.
        """
        self._end_point = value

    def set_feedback(self, value: str) -> None:
        """Set the feedback text.

        Params:
            self: FeedbackLogEntry instance.
            value: User feedback text.

        Returns:
            None.
        """
        self._feedback = value
