from typing import List, Dict, Any
from turtlebot4_backend.turtlebot4_model.Subject import Subject
from turtlebot4_backend.turtlebot4_model.PathLogEntry import PathLogEntry

class Path(Subject):
    """
    Stores path state, history, and feedback for the navigation module.

    This model notifies observers when its state changes so the frontend can
    stay in sync with navigation activity and user feedback.
    """
    def __init__(
        self,
        path_history: List[PathLogEntry] | None = None,
        is_path_module_active: bool = False,
        is_docked: bool = False,
    ) -> None:
        """
        Initialize path state and observer support.

        This sets starting values for the path module and prepares the model
        to publish updates to observers.

        Params:
            path_history: Optional initial list of PathLogEntry records.
            is_path_module_active: Whether the path module starts enabled.
            is_docked: Whether the robot starts in a docked state.

        Return:
            None.
        """
        super().__init__()
        self._path_history: List[PathLogEntry] = path_history if path_history is not None else []
        self._is_path_module_active: bool = is_path_module_active
        self._is_docked: bool = is_docked
        self._path_controller = None 

    # Getters
    def get_path_history(self) -> List[PathLogEntry]:
        """
        Return the stored path log entries.

        This exposes the history for UI display and analytics.

        Params:
            None.

        Return:
            List of PathLogEntry items.
        """
        return self._path_history

    def get_is_path_module_active(self) -> bool:
        """
        Return whether the path module is active.

        This indicates if navigation features should be running.

        Params:
            None.

        Return:
            True if active, otherwise False.
        """
        return self._is_path_module_active

    def get_is_docked(self) -> bool:
        """
        Return whether the robot is docked.

        This status is used by the UI and by dock/undock logic.

        Params:
            None.

        Return:
            True if docked, otherwise False.
        """
        return self._is_docked

    # Setters
    async def set_path_history(self, value: List[PathLogEntry]) -> None:
        """
        Replace the entire path history.

        This is used when the history is loaded or reset and notifies
        observers so the UI updates immediately.

        Params:
            value: New list of PathLogEntry items.

        Return:
            None.
        """
        self._path_history = value
        await self.notify_observers({ 
                "type": "PATH_UPDATE", 
                **self.toJSON() 
        })

    async def set_is_path_module_active(self, value: bool) -> None:
        """
        Enable or disable the path module.

        This toggles navigation behavior and notifies observers when the
        status changes.

        Params:
            value: True to enable, False to disable.

        Return:
            None.
        """
        if self._is_path_module_active != value:
            self._is_path_module_active = value
            await self.notify_observers({ 
                "type": "PATH_UPDATE", 
                **self.toJSON() 
            })

    async def set_is_docked(self, value: bool) -> None:
        """
        Update the docked state and notify observers.

        This keeps the UI in sync with docking status.

        Params:
            value: True if docked, False otherwise.

        Return:
            None.
        """
        if self._is_docked != value:
            self._is_docked = value
            await self.notify_observers({ 
                "type": "PATH_UPDATE", 
                **self.toJSON() 
            })

    def set_path_controller(self, controller) -> None:
        """
        Store a controller reference for command callbacks.

        This allows the model to trigger dock/undock or cancel actions when
        UI messages request them.

        Params:
            controller: PathController instance used to issue commands.

        Return:
            None.
        """
        self._path_controller = controller

    async def add_log_entry(self, entry: PathLogEntry) -> None:
        """
        Append a new log entry and notify observers.

        This is used when new goals or rule outputs are generated.

        Params:
            entry: PathLogEntry to add to history.

        Return:
            None.
        """
        self._path_history.append(entry)
        await self.notify_observers({ 
            "type": "PATH_UPDATE", 
            **self.toJSON() 
        })

    async def update_log_entry(self, index: int, entry: PathLogEntry) -> None:
        """
        Replace a specific log entry and notify observers.

        This updates a single history item, commonly after feedback changes.

        Params:
            index: Position of the entry to replace.
            entry: New PathLogEntry to store at the index.

        Return:
            None.
        """
        if 0 <= index < len(self._path_history):
            self._path_history[index] = entry
            await self.notify_observers({ 
                "type": "PATH_UPDATE", 
                **self.toJSON() 
            })
    
    # Handles user feedback updates from the frontend, matching them to the correct PathLogEntry 
    # and updating the feedback summary.
    async def apply_feedback(self, msg: Dict[str, Any]) -> None:
        """
        Apply user feedback to the matching goal entry.

        This matches feedback to a log entry, updates it, and emits summary
        data so the UI can show progress and quality metrics.

        Params:
            msg: Dict containing a goalId and feedback value.

        Return:
            None.
        """
        goal_id = msg.get("goalId")
        feedback = msg.get("feedback")

        if not goal_id or feedback is None:
            print("[Path] Invalid feedback message:", msg)
            return

        # Find the entry
        for i, entry in enumerate(self._path_history):
            if entry.get_id() == goal_id:
                entry.set_user_feedback(feedback)

                # Update entry and notify frontend
                await self.update_log_entry(i, entry)
                print(f"[Path] Feedback updated for {goal_id}: {feedback}")

                end_point = entry.get_goal_type()

                # Start point = previous entry (if exists)
                if i > 0:
                    prev = self._path_history[i - 1]
                    start_point = prev.get_goal_type()

                    # Duration = difference between timestamps
                    if prev.get_timestamp() and entry.get_timestamp():
                        duration = (entry.get_timestamp() - prev.get_timestamp()).total_seconds()
                    else:
                        duration = 0
                else:
                    start_point = "START"
                    duration = 0

                # Notify frontend of new feedback entry
                await self.notify_observers({
                    "type": "FEEDBACK_ENTRY",
                    "startPoint": start_point,
                    "endPoint": end_point,
                    "duration": duration,
                    "feedback": feedback
                })

                # Send summary of good/bad ratios for all feedback received so far
                await self._send_feedback_summary()
                return

        print(f"[Path] No matching goal entry found for feedback: {goal_id}")

    async def _send_feedback_summary(self):
        """
        Compute and send aggregate feedback ratios.

        This summarizes good/bad feedback to help the UI show overall trends.

        Params:
            None.

        Return:
            None.
        """
        total = len(self._path_history)
        if total == 0:
            good_ratio = bad_ratio = 0
        else:
            good = sum(1 for e in self._path_history if e.get_user_feedback() == "good")
            bad = sum(1 for e in self._path_history if e.get_user_feedback() == "bad")
            good_ratio = good / total
            bad_ratio = bad / total

        await self.notify_observers({
            "type": "FEEDBACK_SUMMARY",
            "goodRatio": good_ratio,
            "badRatio": bad_ratio
        })

    def toJSON(self) -> Dict[str, Any]:
        """
        Convert the Path state into a JSON-serializable structure.

        This formats internal fields so observers and the frontend can
        consume the path state safely.

        Params:
            None.

        Return:
            Dictionary containing path module state and history.
        """
        print()
        return {
            "isPathModuleActive": self._is_path_module_active,
            "isDocked": self._is_docked,
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

    async def fromJSON(self, msg: Dict[str, Any]) -> None:
        """
        Update the Path state based on a frontend message.

        This interprets UI commands to toggle path mode and docking state,
        then triggers any required controller actions. Specifically handles:
        - Path module activation/deactivation
        - Dock/undock commands

        Params:
            msg: Dict containing state changes from the frontend.

        Return:
            None.
        """
        # Handle path module activation state
        new_path_active = bool(msg.get("isPathModuleActive", self._is_path_module_active))
        old_path_active = self._is_path_module_active

        if self._is_path_module_active != new_path_active:
            self._is_path_module_active = new_path_active
            await self.notify_observers({ 
                "type": "PATH_UPDATE", 
                **self.toJSON() 
            })
            
            # If changing from True to False, cancel navigation
            if old_path_active == True and new_path_active == False:
                if self._path_controller is not None:
                    self._path_controller.cancelNavigation()
                    print("[Path] Navigation cancelled - module deactivated")

        # Handle dock status changes
        if "dockStatus" in msg:
            new_dock_status = bool(msg.get("dockStatus"))
            old_dock_status = self._is_docked

            if old_dock_status != new_dock_status:
                self._is_docked = new_dock_status
                await self.notify_observers({ 
                    "type": "PATH_UPDATE", 
                    **self.toJSON() 
                })

                # Trigger dock/undock command based on state change
                if self._path_controller is not None:
                    if new_dock_status == True:
                        # User wants to dock
                        self._path_controller.dock()
                        print("[Path] Dock command triggered")
                    else:
                        # User wants to undock
                        self._path_controller.undock()
                        print("[Path] Undock command triggered")
                else:
                    print("[Path] Warning: PathController not set, cannot execute dock/undock command")