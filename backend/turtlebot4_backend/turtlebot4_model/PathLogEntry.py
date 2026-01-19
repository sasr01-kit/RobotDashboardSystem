# PathLogEntry.py
from datetime import datetime
from typing import Optional


class PathLogEntry:
    def __init__(
        self,
        label: str = "",
        id: str = "",
        goal_type: str = "",
        timestamp: Optional[datetime] = None, 
        #Optional[X] is equivalent to Union[X, None].
        fuzzy_output: str = "",
        user_feedback: str = "",
    ) -> None:
        self._label = label
        self._id = id
        self._goal_type = goal_type
        self._timestamp = timestamp  # remains None if not provided
        self._fuzzy_output = fuzzy_output
        self._user_feedback = user_feedback

    # Getters
    def get_label(self) -> str:
        return self._label

    def get_id(self) -> str:
        return self._id

    def get_goal_type(self) -> str:
        return self._goal_type

    def get_timestamp(self) -> Optional[datetime]:
        return self._timestamp

    def get_fuzzy_output(self) -> str:
        return self._fuzzy_output

    def get_user_feedback(self) -> str:
        return self._user_feedback

    # Setters
    def set_label(self, value: str) -> None:
        self._label = value

    def set_id(self, value: str) -> None:
        self._id = value

    def set_goal_type(self, value: str) -> None:
        self._goal_type = value

    def set_timestamp(self, value: Optional[datetime]) -> None:
        self._timestamp = value

    def set_fuzzy_output(self, value: str) -> None:
        self._fuzzy_output = value

    def set_user_feedback(self, value: str) -> None:
        self._user_feedback = value
