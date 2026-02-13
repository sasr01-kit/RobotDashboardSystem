from datetime import datetime
from typing import Optional

class PathLogEntry:
    """
    Represents a single navigation goal entry in the path history.

    This stores goal metadata and feedback so the UI can display the
    navigation timeline and user assessments.
    """
    def __init__(
        self,
        label: str = "",
        id: str = "",
        goal_type: str = "",
        timestamp: Optional[datetime] = None, 
        fuzzy_output: str = "",
        user_feedback: str = "",
    ) -> None:
        """
        Initialize a path log entry.

        This captures the label, goal type, timestamp, and feedback for a
        single navigation decision.

        Params:
            label: Human-readable label for the entry.
            id: Unique identifier for the goal entry.
            goal_type: Type of goal (e.g., global or intermediate).
            timestamp: When the entry was created; None means unknown.
            fuzzy_output: Rule or planner output text for the entry.
            user_feedback: User-provided feedback (e.g., good/bad).

        Return:
            None.
        """
        self._label = label
        self._id = id
        self._goal_type = goal_type
        self._timestamp = timestamp  # remains None if not provided
        self._fuzzy_output = fuzzy_output
        self._user_feedback = user_feedback

    # Getters
    def get_label(self) -> str:
        """
        Get the display label for this entry.

        This is shown in the UI to describe the goal or rule entry.

        Params:
            None.

        Return:
            Label string.
        """
        return self._label

    def get_id(self) -> str:
        """
        Get the unique identifier for this entry.

        This is used to match feedback or updates to the correct record.

        Params:
            None.

        Return:
            Entry identifier string.
        """
        return self._id

    def get_goal_type(self) -> str:
        """
        Get the goal type for this entry.

        This indicates whether the goal is global or intermediate.

        Params:
            None.

        Return:
            Goal type string.
        """
        return self._goal_type

    def get_timestamp(self) -> Optional[datetime]:
        """
        Get the timestamp for this entry.

        This is used to compute durations between goals and to sort history.

        Params:
            None.

        Return:
            Datetime when created, or None if unknown.
        """
        return self._timestamp

    def get_fuzzy_output(self) -> str:
        """
        Get the fuzzy or rule output associated with this entry.

        This captures the reasoning or rule that produced the goal.

        Params:
            None.

        Return:
            Fuzzy output string.
        """
        return self._fuzzy_output

    def get_user_feedback(self) -> str:
        """
        Get the user feedback for this entry.

        This indicates whether the user judged the goal as good or bad.

        Params:
            None.

        Return:
            Feedback string.
        """
        return self._user_feedback

    # Setters
    def set_label(self, value: str) -> None:
        """
        Set the display label for this entry.

        This updates how the entry appears in the UI.

        Params:
            value: New label string.

        Return:
            None.
        """
        self._label = value

    def set_id(self, value: str) -> None:
        """
        Set the unique identifier for this entry.

        This updates the ID used to match feedback and edits.

        Params:
            value: New identifier string.

        Return:
            None.
        """
        self._id = value

    def set_goal_type(self, value: str) -> None:
        """
        Set the goal type for this entry.

        This updates the category of the goal for reporting.

        Params:
            value: New goal type string.

        Return:
            None.
        """
        self._goal_type = value

    def set_timestamp(self, value: Optional[datetime]) -> None:
        """
        Set the timestamp for this entry.

        This records when the goal entry was created or updated.

        Params:
            value: New datetime or None.

        Return:
            None.
        """
        self._timestamp = value

    def set_fuzzy_output(self, value: str) -> None:
        """
        Set the fuzzy or rule output for this entry.

        This updates the recorded reasoning text for the goal.

        Params:
            value: New fuzzy output string.

        Return:
            None.
        """
        self._fuzzy_output = value

    def set_user_feedback(self, value: str) -> None:
        """
        Set the user feedback for this entry.

        This updates whether the user rated the goal as good or bad.

        Params:
            value: New feedback string.

        Return:
            None.
        """
        self._user_feedback = value
