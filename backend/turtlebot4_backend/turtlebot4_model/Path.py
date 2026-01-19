# Path.py
from typing import List, Dict, Any
from Subject import Subject
from PathLogEntry import PathLogEntry


class Path(Subject):
    def __init__(
        self,
        path_history: List[PathLogEntry] | None = None,
        is_path_module_active: bool = False,
    ) -> None:
        super().__init__()
        self._path_history: List[PathLogEntry] = path_history if path_history is not None else []
        self._is_path_module_active: bool = is_path_module_active

    # Getters
    def get_path_history(self) -> List[PathLogEntry]:
        return self._path_history

    def get_is_path_module_active(self) -> bool:
        return self._is_path_module_active

    # Setters
    def set_path_history(self, value: List[PathLogEntry]) -> None:
        self._path_history = value
        self.notifyObservers(self.toJSON())

    def set_is_path_module_active(self, value: bool) -> None:
        if self._is_path_module_active != value:
            self._is_path_module_active = value
            self.notifyObservers(self.toJSON())

    # Convenience methods for modifying the history
    def add_log_entry(self, entry: PathLogEntry) -> None:
        self._path_history.append(entry)
        self.notifyObservers(self.toJSON())

    def update_log_entry(self, index: int, entry: PathLogEntry) -> None:
        if 0 <= index < len(self._path_history):
            self._path_history[index] = entry
            self.notifyObservers(self.toJSON())

    # Serialization
    def toJSON(self) -> Dict[str, Any]:
        """
        Converts the Path state into a JSON-serializable structure.
        """
        return {
            "isPathModuleActive": self._is_path_module_active,
            "pathHistory": [
                {
                    "label": e.get_label(),
                    "id": e.get_id(),
                    "goalType": e.get_goal_type(),
                    "timestamp": e.get_timestamp().isoformat() if e.get_timestamp() else None,
                    "fuzzyOutput": e.get_fuzzy_output(),
                    "userFeedback": e.get_user_feedback(),
                }
                for e in self._path_history
            ],
        }
    def fromJSON(self, msg: Dict[str, Any]) -> None:
        """
        Updates the Path state from a frontend JSON message.
        This method is only responsible for updating the
        path module execution state.
        """
        new_value = bool(msg.get("isPathModuleActive", self._is_path_module_active))

        if self._is_path_module_active != new_value:
            self._is_path_module_active = new_value
            self.notifyObservers(self.toJSON())
