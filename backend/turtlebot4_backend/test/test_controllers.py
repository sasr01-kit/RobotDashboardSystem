"""
test_controllers.py — all controller and coverage-gap tests in one file.

Covers:
  - MapController    (_map_callback, _humans_callback, _robot_pose_callback,
                      _send_initial_map_png, shutdown)
  - PathController   (_pose_callback, _rule_callback, _global_goal_callback,
                      dock, undock, cancelNavigation, get_records, stop)
  - TeleopController (_publish_drive_command, _on_teleop_update, stop)
  - Path             (add_log_entry, update_log_entry, apply_feedback,
                      _send_feedback_summary, toJSON, fromJSON)
  - Feedback         (all methods)
  - ConcreteObserver (all methods)
  - RobotState       (set_mode, set_docked)
  - StatusController (_notify_listeners, stop)

No ROS, no FastAPI, no hardware required.

Run with:
    PYTHONPATH=backend pytest backend/turtlebot4_backend/test/test_controllers.py -v
"""

import asyncio
import json
import sys
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Must be before controller imports that transitively import ROS deps.
sys.modules['geometry_msgs'] = MagicMock()
sys.modules['geometry_msgs.msg'] = MagicMock()
sys.modules['roslibpy'] = MagicMock()
sys.modules['fastapi'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['matplotlib'] = MagicMock()
sys.modules['matplotlib.pyplot'] = MagicMock()

from turtlebot4_backend.turtlebot4_controller.MapController import MapController
from turtlebot4_backend.turtlebot4_controller.PathController import PathController
from turtlebot4_backend.turtlebot4_controller.RosbridgeConnection import RosbridgeConnection
from turtlebot4_backend.turtlebot4_controller.StatusController import StatusController
from turtlebot4_backend.turtlebot4_controller.TeleopController import TeleopController
from turtlebot4_backend.turtlebot4_model.ConcreteObserver import ConcreteObserver
from turtlebot4_backend.turtlebot4_model.Feedback import Feedback
from turtlebot4_backend.turtlebot4_model.FeedbackLogEntry import FeedbackLogEntry
from turtlebot4_backend.turtlebot4_model.Human import Human
from turtlebot4_backend.turtlebot4_model.Map import Map
from turtlebot4_backend.turtlebot4_model.Observer import Observer
from turtlebot4_backend.turtlebot4_model.Path import Path
from turtlebot4_backend.turtlebot4_model.PathLogEntry import PathLogEntry
from turtlebot4_backend.turtlebot4_model.RobotState import RobotState
from turtlebot4_backend.turtlebot4_model.Teleoperate import Teleoperate


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def make_mock_observer():

    class _Obs(Observer):
        def __init__(self):
            self.received = []
        async def update(self, source, data):
            self.received.append(data)

    return _Obs()


def make_path(active=False):
    return Path(is_path_module_active=active)


def make_entry(id="goal_1", feedback="", timestamp=None, label="Test", goal_type="global"):
    
    return PathLogEntry(label=label, id=id, goal_type=goal_type,
                        timestamp=timestamp, fuzzy_output="rule", user_feedback=feedback)


def make_map_model():
    
    m = Map()
    m._convert_mapdata_to_png = MagicMock()
    m._mapDataPNG = "fakepng"
    m.set_mapData = AsyncMock()
    m.set_robotPose = AsyncMock()
    m.set_globalGoal = AsyncMock()
    m.set_intermediateWaypoints = AsyncMock()
    m.set_detectedHumans = AsyncMock()
    return m


def make_map_controller(map_model):
    with patch("turtlebot4_backend.turtlebot4_controller.MapController.RosbridgeConnection") as MockRos:
        mock_ros = MagicMock()
        mock_ros.isConnected = True
        MockRos.return_value = mock_ros
        ctrl = MapController(map_model=map_model)
    return ctrl, mock_ros

def make_path_controller(path_model, map_model):
    with patch("turtlebot4_backend.turtlebot4_controller.PathController.RosbridgeConnection") as MockRos:
        mock_ros = MagicMock()
        mock_ros.isConnected = True
        MockRos.return_value = mock_ros
        PathController._dock_status_callback = lambda self, msg: None
        ctrl = PathController(path_model=path_model, map_model=map_model)
    return ctrl, mock_ros

def make_teleop_controller():
    teleop = Teleoperate()
    loop = asyncio.get_event_loop()
    with patch("turtlebot4_backend.turtlebot4_controller.TeleopController.RosbridgeConnection") as MockRos:
        mock_ros = MagicMock()
        mock_ros.isConnected = True
        MockRos.return_value = mock_ros
        ctrl = TeleopController(teleop=teleop, loop=loop)
    return ctrl, teleop, mock_ros


def make_status_controller():
    robot_state = RobotState(path_model=make_path())
    loop = asyncio.get_event_loop()
    with patch("turtlebot4_backend.turtlebot4_controller.StatusController.RosbridgeConnection") as MockRos, \
         patch("threading.Thread"):
        MockRos.return_value = MagicMock()
        sc = StatusController(robot_state=robot_state, loop=loop)
    return sc, robot_state


# ═════════════════════════════════════════════
# MapController
# ═════════════════════════════════════════════

class TestMapControllerMapCallback:

    def _make(self):
        m = make_map_model()
        ctrl, ros = make_map_controller(m)
        ctrl._loop = MagicMock()
        return ctrl, m

    def test_first_message_sets_map_received(self):
        ctrl, _ = self._make()
        ctrl._map_callback({"info": {"resolution": 0.05, "width": 10, "height": 10}, "data": [0]*100})
        assert ctrl._map_received is True

    def test_second_message_is_ignored(self):
        ctrl, _ = self._make()
        msg = {"info": {"resolution": 0.05, "width": 2, "height": 2}, "data": [0]*4}
        ctrl._map_callback(msg)
        first_count = ctrl._loop.call_soon_threadsafe.call_count
        ctrl._map_callback(msg)
        assert ctrl._loop.call_soon_threadsafe.call_count == first_count

    def test_schedules_async_map_update(self):
        ctrl, _ = self._make()
        ctrl._map_callback({"info": {"resolution": 0.05, "width": 4, "height": 4}, "data": [0]*16})
        ctrl._loop.call_soon_threadsafe.assert_called_once()

    def test_missing_info_uses_defaults(self):
        ctrl, _ = self._make()
        ctrl._map_callback({"info": {}, "data": []})
        assert ctrl._map_received is True

    def test_empty_data_does_not_raise(self):
        ctrl, _ = self._make()
        ctrl._map_callback({"info": {"resolution": 0.05, "width": 0, "height": 0}, "data": []})
        assert ctrl._map_received is True


class TestMapControllerHumansCallback:

    def _make(self):
        ctrl, _ = make_map_controller(make_map_model())
        ctrl._loop = MagicMock()
        return ctrl

    def test_schedules_update_with_humans(self):
        ctrl = self._make()
        ctrl._humans_callback({"poses": [{"position": {"x": 1.0, "y": 2.0, "z": 0.0}}]})
        ctrl._loop.call_soon_threadsafe.assert_called_once()

    def test_empty_poses_still_schedules(self):
        ctrl = self._make()
        ctrl._humans_callback({"poses": []})
        ctrl._loop.call_soon_threadsafe.assert_called_once()

    def test_missing_poses_key_does_not_raise(self):
        ctrl = self._make()
        ctrl._humans_callback({})
        ctrl._loop.call_soon_threadsafe.assert_called_once()

    def test_human_ids_are_sequential(self):
        poses = [{"position": {"x": float(i), "y": 0.0, "z": 0.0}} for i in range(3)]
        humans = [Human(human_id=f"human_{i+1}",
                        position={"x": p["position"]["x"], "y": 0.0, "z": 0.0})
                  for i, p in enumerate(poses)]
        assert [h.get_id() for h in humans] == ["human_1", "human_2", "human_3"]


class TestMapControllerRobotPoseCallback:

    def _make(self):
        ctrl, _ = make_map_controller(make_map_model())
        ctrl._loop = MagicMock()
        return ctrl

    def _valid_msg(self, x=1.0, y=2.0):
        return {"pose": {"pose": {
            "position": {"x": x, "y": y, "z": 0.0},
            "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
        }}}

    def test_valid_pose_schedules_update(self):
        ctrl = self._make()
        ctrl._robot_pose_callback(self._valid_msg())
        ctrl._loop.call_soon_threadsafe.assert_called_once()

    def test_empty_pose_returns_early(self):
        ctrl = self._make()
        ctrl._robot_pose_callback({"pose": {"pose": {}}})
        ctrl._loop.call_soon_threadsafe.assert_not_called()

    def test_missing_pose_key_returns_early(self):
        ctrl = self._make()
        ctrl._robot_pose_callback({})
        ctrl._loop.call_soon_threadsafe.assert_not_called()

    def test_missing_sub_keys_use_defaults(self):
        ctrl = self._make()
        ctrl._robot_pose_callback({"pose": {"pose": {"position": {}, "orientation": {}}}})
        ctrl._loop.call_soon_threadsafe.assert_called_once()


class TestMapControllerMisc:

    def test_send_initial_png_schedules_when_png_exists(self):
        m = make_map_model()
        m._mapDataPNG = "fakepng"
        ctrl, _ = make_map_controller(m)
        ctrl._loop = MagicMock()
        ctrl._send_initial_map_png()
        ctrl._loop.call_soon_threadsafe.assert_called_once()

    def test_send_initial_png_skips_when_no_png(self):
        m = make_map_model()
        m._mapDataPNG = None
        ctrl, _ = make_map_controller(m)
        ctrl._loop = MagicMock()
        ctrl._send_initial_map_png()
        ctrl._loop.call_soon_threadsafe.assert_not_called()

    def test_shutdown_calls_terminate(self):
        ctrl, mock_ros = make_map_controller(make_map_model())
        ctrl.shutdown()
        mock_ros.terminate.assert_called_once()

    def test_shutdown_safe_when_terminate_raises(self):
        ctrl, mock_ros = make_map_controller(make_map_model())
        mock_ros.terminate.side_effect = Exception("err")
        ctrl.shutdown()  # should not raise


# ═════════════════════════════════════════════
# PathController
# ═════════════════════════════════════════════

class TestPathControllerPoseCallback:

    def _make(self, active=False):
        ctrl, _ = make_path_controller(make_path(active), make_map_model())
        ctrl._loop = MagicMock()
        return ctrl

    def _msg(self):
        return {"pose": {"pose": {
            "position": {"x": 1.0, "y": 0.0, "z": 0.0},
            "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
        }}}

    def test_skipped_when_path_inactive(self):
        ctrl = self._make(active=False)
        ctrl._pose_callback(self._msg())
        ctrl._loop.call_soon_threadsafe.assert_not_called()

    def test_schedules_when_path_active(self):
        ctrl = self._make(active=True)
        ctrl._pose_callback(self._msg())
        ctrl._loop.call_soon_threadsafe.assert_called_once()

    def test_empty_pose_returns_early(self):
        ctrl = self._make(active=True)
        ctrl._pose_callback({"pose": {"pose": {}}})
        ctrl._loop.call_soon_threadsafe.assert_not_called()

    def test_missing_pose_returns_early(self):
        ctrl = self._make(active=True)
        ctrl._pose_callback({})
        ctrl._loop.call_soon_threadsafe.assert_not_called()


class TestPathControllerRuleCallback:

    def _make(self, active=True):
        ctrl, _ = make_path_controller(make_path(active), make_map_model())
        ctrl._loop = MagicMock()
        return ctrl

    def test_skipped_when_path_inactive(self):
        ctrl = self._make(active=False)
        ctrl._rule_callback({"data": {"goal_type": "global", "position": {}, "rule": "R1"}})
        ctrl._loop.call_soon_threadsafe.assert_not_called()

    def test_accepts_dict_data(self):
        ctrl = self._make()
        ctrl._rule_callback({"data": {"goal_type": "global", "position": {"x": 1.0}, "rule": "R1"}})
        assert ctrl._loop.call_soon_threadsafe.call_count >= 1

    def test_accepts_json_string(self):
        ctrl = self._make()
        ctrl._rule_callback({"data": json.dumps({"goal_type": "intermediate", "position": {}, "rule": "R2"})})
        assert ctrl._loop.call_soon_threadsafe.call_count >= 1

    def test_invalid_json_does_not_raise(self):
        ctrl = self._make()
        ctrl._rule_callback({"data": "not { valid json"})
        ctrl._loop.call_soon_threadsafe.assert_not_called()

    def test_unexpected_type_does_not_raise(self):
        ctrl = self._make()
        ctrl._rule_callback({"data": 12345})
        ctrl._loop.call_soon_threadsafe.assert_not_called()

    def test_intermediate_type_schedules_waypoint_and_log(self):
        ctrl = self._make()
        ctrl._rule_callback({"data": {"goal_type": "intermediate", "position": {"x": 3.0}, "rule": "R3"}})
        assert ctrl._loop.call_soon_threadsafe.call_count >= 2

    def test_global_type_schedules_goal_and_log(self):
        ctrl = self._make()
        ctrl._rule_callback({"data": {"goal_type": "global", "position": {"x": 5.0}, "rule": "R4"}})
        assert ctrl._loop.call_soon_threadsafe.call_count >= 2

    def test_unknown_type_still_logs_entry(self):
        ctrl = self._make()
        ctrl._rule_callback({"data": {"goal_type": "unknown", "position": {}, "rule": "R5"}})
        ctrl._loop.call_soon_threadsafe.assert_called_once()


class TestPathControllerGlobalGoalCallback:

    def _make(self, active=True):
        ctrl, _ = make_path_controller(make_path(active), make_map_model())
        ctrl._loop = MagicMock()
        return ctrl

    def test_skipped_when_inactive(self):
        ctrl = self._make(active=False)
        ctrl._global_goal_callback({"pose": {"position": {"x": 1.0, "y": 0.0, "z": 0.0}}})
        ctrl._loop.call_soon_threadsafe.assert_not_called()

    def test_schedules_when_active(self):
        ctrl = self._make()
        ctrl._global_goal_callback({"pose": {"position": {"x": 1.0, "y": 0.0, "z": 0.0}}})
        ctrl._loop.call_soon_threadsafe.assert_called_once()

    def test_missing_position_uses_defaults(self):
        ctrl = self._make()
        ctrl._global_goal_callback({"pose": {}})
        ctrl._loop.call_soon_threadsafe.assert_called_once()


class TestPathControllerCommands:

    def _make(self):
        path_model = make_path()
        ctrl, mock_ros = make_path_controller(path_model, make_map_model())
        return ctrl, path_model, mock_ros

    def test_dock_calls_send_action_goal(self):
        ctrl, _, mock_ros = self._make()
        ctrl._connected = True
        ctrl.dock()
        mock_ros.send_action_goal.assert_called_once()

    def test_dock_skipped_when_not_connected(self):
        ctrl, _, mock_ros = self._make()
        ctrl._connected = False
        ctrl.dock()
        mock_ros.send_action_goal.assert_not_called()

    def test_dock_safe_when_action_raises(self):
        ctrl, _, mock_ros = self._make()
        ctrl._connected = True
        mock_ros.send_action_goal.side_effect = Exception("fail")
        ctrl.dock()  # should not raise

    def test_undock_calls_send_action_goal(self):
        ctrl, _, mock_ros = self._make()
        ctrl._connected = True
        ctrl.undock()
        mock_ros.send_action_goal.assert_called_once()

    def test_undock_skipped_when_not_connected(self):
        ctrl, _, mock_ros = self._make()
        ctrl._connected = False
        ctrl.undock()
        mock_ros.send_action_goal.assert_not_called()

    def test_undock_safe_when_action_raises(self):
        ctrl, _, mock_ros = self._make()
        ctrl._connected = True
        mock_ros.send_action_goal.side_effect = Exception("fail")
        ctrl.undock()  # should not raise

    def test_cancel_navigation_publishes_to_cmd_vel(self):
        ctrl, _, mock_ros = self._make()
        ctrl.cancelNavigation()
        mock_ros.publish.assert_called_once()
        assert mock_ros.publish.call_args[0][0] == "/cmd_vel"

    def test_get_records_returns_path_history(self):
        ctrl, path_model, _ = self._make()
        assert ctrl.get_records() == path_model.get_path_history()

    def test_stop_sets_connected_false(self):
        ctrl, _, _ = self._make()
        ctrl.stop()
        assert ctrl._connected is False

    def test_stop_calls_terminate(self):
        ctrl, _, mock_ros = self._make()
        ctrl.stop()
        mock_ros.terminate.assert_called_once()


# ═════════════════════════════════════════════
# TeleopController
# ═════════════════════════════════════════════

class TestTeleopControllerPublishDriveCommand:

    def _make(self):
        ctrl, teleop, mock_ros = make_teleop_controller()
        mock_ros.publish.reset_mock()
        return ctrl, teleop, mock_ros

    def test_forward_publishes_to_cmd_vel(self):
        ctrl, teleop, mock_ros = self._make()
        teleop.add_command("FORWARD")
        run(ctrl._publish_drive_command())
        mock_ros.publish.assert_called_once()
        assert mock_ros.publish.call_args[0][0] == "/cmd_vel"

    def test_backward_publishes(self):
        ctrl, teleop, mock_ros = self._make()
        teleop.add_command("BACKWARD")
        run(ctrl._publish_drive_command())
        mock_ros.publish.assert_called_once()

    def test_left_publishes(self):
        ctrl, teleop, mock_ros = self._make()
        teleop.add_command("LEFT")
        run(ctrl._publish_drive_command())
        mock_ros.publish.assert_called_once()

    def test_right_publishes(self):
        ctrl, teleop, mock_ros = self._make()
        teleop.add_command("RIGHT")
        run(ctrl._publish_drive_command())
        mock_ros.publish.assert_called_once()

    def test_stop_publishes(self):
        ctrl, teleop, mock_ros = self._make()
        teleop.add_command("STOP")
        run(ctrl._publish_drive_command())
        mock_ros.publish.assert_called_once()

    def test_empty_queue_does_not_publish(self):
        ctrl, _, mock_ros = self._make()
        run(ctrl._publish_drive_command())
        mock_ros.publish.assert_not_called()

    def test_unknown_command_does_not_raise(self):
        ctrl, teleop, _ = self._make()
        teleop.add_command("NOT_REAL")
        run(ctrl._publish_drive_command())  # should not raise


class TestTeleopControllerMisc:

    def test_on_teleop_update_schedules_publish(self):
        ctrl, _, _ = make_teleop_controller()
        ctrl._loop = MagicMock()
        ctrl._on_teleop_update(source=None, data=None)
        ctrl._loop.call_soon_threadsafe.assert_called_once()

    def test_observer_attached_on_init(self):
        ctrl, teleop, _ = make_teleop_controller()
        assert ctrl._on_teleop_update in teleop._observers

    def test_stop_unadvertises_and_terminates(self):
        ctrl, _, mock_ros = make_teleop_controller()
        ctrl.stop()
        mock_ros.unadvertise.assert_called_once_with('/cmd_vel')
        mock_ros.terminate.assert_called_once()

    def test_stop_safe_when_unadvertise_raises(self):
        ctrl, _, mock_ros = make_teleop_controller()
        mock_ros.unadvertise.side_effect = Exception("err")
        ctrl.stop()  # should not raise
        mock_ros.terminate.assert_called_once()

    def test_stop_safe_when_terminate_raises(self):
        ctrl, _, mock_ros = make_teleop_controller()
        mock_ros.terminate.side_effect = Exception("err")
        ctrl.stop()  # should not raise


# ═════════════════════════════════════════════
# Path — add_log_entry, update_log_entry,
#         apply_feedback, _send_feedback_summary,
#         toJSON, fromJSON
# ═════════════════════════════════════════════

class TestPathNewMethods:

    def test_add_log_entry_appends_and_notifies(self):
        p = make_path()
        obs = make_mock_observer()
        p.attach(obs)
        run(p.add_log_entry(make_entry()))
        assert len(p.get_path_history()) == 1
        assert any(d["type"] == "PATH_UPDATE" for d in obs.received)

    def test_add_log_entry_multiple(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1")))
        run(p.add_log_entry(make_entry(id="g2")))
        assert len(p.get_path_history()) == 2

    def test_update_log_entry_replaces_correct_index(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1")))
        run(p.update_log_entry(0, make_entry(id="g1_updated")))
        assert p.get_path_history()[0].get_id() == "g1_updated"

    def test_update_log_entry_notifies(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1")))
        obs = make_mock_observer()
        p.attach(obs)
        run(p.update_log_entry(0, make_entry(id="g1_new")))
        assert any(d["type"] == "PATH_UPDATE" for d in obs.received)

    def test_update_log_entry_out_of_bounds_ignored(self):
        p = make_path()
        run(p.add_log_entry(make_entry()))
        obs = make_mock_observer()
        p.attach(obs)
        run(p.update_log_entry(99, make_entry(id="bad")))
        assert len(obs.received) == 0

    def test_apply_feedback_first_entry_uses_START(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1", timestamp=datetime(2024, 1, 1, 12, 0, 0))))
        obs = make_mock_observer()
        p.attach(obs)
        run(p.apply_feedback({"goalId": "g1", "feedback": "good"}))
        events = [d for d in obs.received if d.get("type") == "FEEDBACK_ENTRY"]
        assert events[0]["startPoint"] == "START"
        assert events[0]["feedback"] == "good"

    def test_apply_feedback_computes_duration_from_timestamps(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1", timestamp=datetime(2024, 1, 1, 12, 0, 0))))
        run(p.add_log_entry(make_entry(id="g2", timestamp=datetime(2024, 1, 1, 12, 0, 10))))
        obs = make_mock_observer()
        p.attach(obs)
        run(p.apply_feedback({"goalId": "g2", "feedback": "bad"}))
        events = [d for d in obs.received if d.get("type") == "FEEDBACK_ENTRY"]
        assert events[0]["duration"] == 10.0

    def test_apply_feedback_no_timestamps_duration_zero(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1", timestamp=None)))
        run(p.add_log_entry(make_entry(id="g2", timestamp=None)))
        obs = make_mock_observer()
        p.attach(obs)
        run(p.apply_feedback({"goalId": "g2", "feedback": "good"}))
        events = [d for d in obs.received if d.get("type") == "FEEDBACK_ENTRY"]
        assert events[0]["duration"] == 0

    def test_apply_feedback_no_match_does_nothing(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1")))
        obs = make_mock_observer()
        p.attach(obs)
        run(p.apply_feedback({"goalId": "nonexistent", "feedback": "good"}))
        assert not any(d.get("type") == "FEEDBACK_ENTRY" for d in obs.received)

    def test_apply_feedback_missing_goal_id_returns_early(self):
        p = make_path()
        obs = make_mock_observer()
        p.attach(obs)
        run(p.apply_feedback({"feedback": "good"}))
        assert len(obs.received) == 0

    def test_apply_feedback_none_feedback_returns_early(self):
        p = make_path()
        obs = make_mock_observer()
        p.attach(obs)
        run(p.apply_feedback({"goalId": "g1", "feedback": None}))
        assert len(obs.received) == 0

    def test_apply_feedback_also_sends_summary(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1")))
        obs = make_mock_observer()
        p.attach(obs)
        run(p.apply_feedback({"goalId": "g1", "feedback": "good"}))
        assert any(d.get("type") == "FEEDBACK_SUMMARY" for d in obs.received)

    def test_feedback_summary_empty_history(self):
        p = make_path()
        obs = make_mock_observer()
        p.attach(obs)
        run(p._send_feedback_summary())
        s = [d for d in obs.received if d.get("type") == "FEEDBACK_SUMMARY"][0]
        assert s["goodRatio"] == 0 and s["badRatio"] == 0

    def test_feedback_summary_mixed(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1", feedback="good")))
        run(p.add_log_entry(make_entry(id="g2", feedback="bad")))
        obs = make_mock_observer()
        p.attach(obs)
        run(p._send_feedback_summary())
        s = [d for d in obs.received if d.get("type") == "FEEDBACK_SUMMARY"][0]
        assert s["goodRatio"] == 0.5 and s["badRatio"] == 0.5

    def test_feedback_summary_all_good(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1", feedback="good")))
        run(p.add_log_entry(make_entry(id="g2", feedback="good")))
        obs = make_mock_observer()
        p.attach(obs)
        run(p._send_feedback_summary())
        s = [d for d in obs.received if d.get("type") == "FEEDBACK_SUMMARY"][0]
        assert s["goodRatio"] == 1.0 and s["badRatio"] == 0.0

    def test_toJSON_contains_expected_keys(self):
        j = make_path().toJSON()
        assert "isPathModuleActive" in j
        assert "isDocked" in j
        assert "pathHistory" in j

    def test_toJSON_timestamp_present(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1", timestamp=datetime(2024, 1, 1))))
        assert p.toJSON()["pathHistory"][0]["timestamp"] is not None

    def test_toJSON_timestamp_none(self):
        p = make_path()
        run(p.add_log_entry(make_entry(id="g1", timestamp=None)))
        assert p.toJSON()["pathHistory"][0]["timestamp"] is None

    def test_fromJSON_activates_path_module(self):
        p = make_path()
        obs = make_mock_observer()
        p.attach(obs)
        run(p.fromJSON({"isPathModuleActive": True}))
        assert p.get_is_path_module_active() is True
        assert any(d["type"] == "PATH_UPDATE" for d in obs.received)

    def test_fromJSON_no_change_no_notify(self):
        p = make_path()
        obs = make_mock_observer()
        p.attach(obs)
        run(p.fromJSON({"isPathModuleActive": False}))
        assert len(obs.received) == 0

    def test_fromJSON_deactivate_calls_cancel_navigation(self):
        p = make_path()
        p._is_path_module_active = True
        mock_ctrl = MagicMock()
        p.set_path_controller(mock_ctrl)
        run(p.fromJSON({"isPathModuleActive": False}))
        mock_ctrl.cancelNavigation.assert_called_once()

    def test_fromJSON_dock_triggers_dock(self):
        p = make_path()
        mock_ctrl = MagicMock()
        p.set_path_controller(mock_ctrl)
        run(p.fromJSON({"dockStatus": True}))
        mock_ctrl.dock.assert_called_once()

    def test_fromJSON_undock_triggers_undock(self):
        p = make_path()
        p._is_docked = True
        mock_ctrl = MagicMock()
        p.set_path_controller(mock_ctrl)
        run(p.fromJSON({"dockStatus": False}))
        mock_ctrl.undock.assert_called_once()

    def test_fromJSON_dock_no_controller_is_safe(self):
        p = make_path()
        run(p.fromJSON({"dockStatus": True}))
        assert p.get_is_docked() is True

    def test_fromJSON_dock_same_value_no_notify(self):
        p = make_path()
        obs = make_mock_observer()
        p.attach(obs)
        run(p.fromJSON({"dockStatus": False}))
        assert len(obs.received) == 0


# ═════════════════════════════════════════════
# Feedback
# ═════════════════════════════════════════════

class TestFeedback:

    def _make(self):
        return Feedback()

    def _entry(self, id="g1", feedback="", timestamp=None, label="L", goal_type="global"):
        return PathLogEntry(label=label, id=id, goal_type=goal_type,
                            timestamp=timestamp, user_feedback=feedback)

    def test_initial_state(self):
        f = self._make()
        assert f.get_path_history() == []
        assert f.get_total_good_ratings() == 0
        assert f.get_total_bad_ratings() == 0
        assert f.get_feedback_history() == []

    def test_setters(self):
        f = self._make()
        f.set_path_history([self._entry()])
        f.set_total_good_ratings(3)
        f.set_total_bad_ratings(1)
        f.set_feedback_history([FeedbackLogEntry(duration="5s", start_point="A",
                                                  end_point="B", feedback="good")])
        assert len(f.get_path_history()) == 1
        assert f.get_total_good_ratings() == 3
        assert f.get_total_bad_ratings() == 1
        assert len(f.get_feedback_history()) == 1

    def test_calculate_ratio_empty(self):
        assert self._make().calculate_feedback_ratio([]) == 0.0

    def test_calculate_ratio_all_good(self):
        f = self._make()
        entries = [self._entry(id=f"g{i}", feedback="good") for i in range(3)]
        assert f.calculate_feedback_ratio(entries) == 1.0
        assert f.get_total_good_ratings() == 3
        assert f.get_total_bad_ratings() == 0

    def test_calculate_ratio_mixed(self):
        f = self._make()
        entries = [self._entry(id="g1", feedback="good"),
                   self._entry(id="g2", feedback="bad"),
                   self._entry(id="g3", feedback="bad")]
        assert abs(f.calculate_feedback_ratio(entries) - 1/3) < 0.001
        assert f.get_total_good_ratings() == 1
        assert f.get_total_bad_ratings() == 2

    def test_calculate_ratio_none_feedback_skipped(self):
        assert self._make().calculate_feedback_ratio(
            [PathLogEntry(id="g1", user_feedback=None)]) == 0.0

    def test_update_log_adds_entry(self):
        f = self._make()
        f.update_feedback_log([self._entry(id="g1", feedback="good",
                                            timestamp=datetime(2024, 1, 1),
                                            label="Goal1", goal_type="global")])
        log = f.get_feedback_history()[0]
        assert log.get_feedback() == "good"
        assert log.get_start_point() == "Goal1"
        assert log.get_end_point() == "global"

    def test_update_log_skips_none_feedback(self):
        f = self._make()
        f.update_feedback_log([PathLogEntry(id="g1", user_feedback=None)])
        assert len(f.get_feedback_history()) == 0

    def test_toJSON_structure(self):
        f = self._make()
        f.set_total_good_ratings(2)
        f.set_total_bad_ratings(1)
        j = f.toJSON()
        assert j["totalGoodRatings"] == 2
        assert j["totalBadRatings"] == 1
        assert abs(j["feedbackRatio"] - 2/3) < 0.001
        assert "feedbackHistory" in j

    def test_toJSON_zero_ratio(self):
        assert self._make().toJSON()["feedbackRatio"] == 0.0

    def test_fromJSON_updates_matching_entry(self):
        f = self._make()
        f.set_path_history([self._entry(id="g5", feedback="")])
        f.fromJSON({"id": "g5", "feedback": "good"})
        assert f.get_path_history()[0].get_user_feedback() == "good"

    def test_fromJSON_no_id_does_nothing(self):
        f = self._make()
        f.set_path_history([self._entry(id="g5", feedback="")])
        f.fromJSON({"feedback": "good"})
        assert f.get_path_history()[0].get_user_feedback() == ""

    def test_fromJSON_no_matching_id_does_nothing(self):
        f = self._make()
        f.set_path_history([self._entry(id="g5", feedback="")])
        f.fromJSON({"id": "nonexistent", "feedback": "good"})
        assert f.get_path_history()[0].get_user_feedback() == ""


# ═════════════════════════════════════════════
# ConcreteObserver
# ═════════════════════════════════════════════

class TestConcreteObserver:

    def _make(self):
        mock_ws = MagicMock()
        mock_ws.send_json = AsyncMock()
        return ConcreteObserver(mock_ws), mock_ws

    def test_stores_client(self):
        obs, mock_ws = self._make()
        assert obs._client is mock_ws

    def test_update_sends_payload(self):
        obs, mock_ws = self._make()
        run(obs.update(None, {"type": "TEST"}))
        mock_ws.send_json.assert_called_once_with({"type": "TEST"})

    def test_update_multiple_times(self):
        obs, mock_ws = self._make()
        run(obs.update(None, {"n": 1}))
        run(obs.update(None, {"n": 2}))
        assert mock_ws.send_json.call_count == 2

    def test_source_argument_ignored(self):
        obs, mock_ws = self._make()
        run(obs.update(source="anything", data={"k": "v"}))
        mock_ws.send_json.assert_called_once_with({"k": "v"})


# ═════════════════════════════════════════════
# RobotState — set_mode and set_docked
# ═════════════════════════════════════════════

class TestRobotStateDerivedMethods:

    def _make(self, active=False):
        return RobotState(path_model=make_path(active))

    def test_set_mode_notifies(self):
        state = self._make()
        obs = make_mock_observer()
        state.attach(obs)
        run(state.set_mode())
        assert any(d.get("type") == "STATUS_UPDATE" for d in obs.received)

    def test_set_mode_payload_has_mode_key(self):
        state = self._make()
        obs = make_mock_observer()
        state.attach(obs)
        run(state.set_mode())
        assert "mode" in obs.received[0]

    def test_set_mode_no_local_field(self):
        state = self._make()
        run(state.set_mode())
        assert not hasattr(state, "_mode")

    def test_set_docked_notifies(self):
        state = self._make()
        obs = make_mock_observer()
        state.attach(obs)
        run(state.set_docked())
        assert any(d.get("type") == "STATUS_UPDATE" for d in obs.received)

    def test_set_docked_payload_has_isDocked_key(self):
        state = self._make()
        obs = make_mock_observer()
        state.attach(obs)
        run(state.set_docked())
        assert "isDocked" in obs.received[0]

    def test_set_docked_no_local_field(self):
        state = self._make()
        run(state.set_docked())
        assert not hasattr(state, "_is_docked")

# test status controller. 
class TestStatusController:
    """
    Combined tests for StatusController covering:
      - updateBattery, updateWifi, updatePiConnection, updateCommsConnection
      - _extract_bool_from_msg
      - attach_listener / detach
      - _notify_listeners
      - _battery_cb, _wifi_cb, _pi_cb, _comms_cb  (bridge callbacks)
      - _connect_and_subscribe success and failure paths
      - stop
    """

    def _make(self):
        robot_state = RobotState(path_model=Path())
        loop = asyncio.get_event_loop()
        with patch("turtlebot4_backend.turtlebot4_controller.StatusController.RosbridgeConnection") as MockRos, \
             patch("threading.Thread"):
            MockRos.return_value = MagicMock()
            sc = StatusController(robot_state=robot_state, loop=loop)
        return sc, robot_state

    # ── updateBattery ──────────────────────────────────────────────────────────

    def test_battery_normalizes_0_to_1_range(self):
        sc, state = self._make()
        run(sc.updateBattery({"percentage": 0.75}))
        assert state.get_battery_percentage() == 75.0

    def test_battery_keeps_0_to_100_range(self):
        sc, state = self._make()
        run(sc.updateBattery({"percentage": 80.0}))
        assert state.get_battery_percentage() == 80.0

    def test_battery_clamps_above_100(self):
        sc, state = self._make()
        run(sc.updateBattery({"percentage": 150.0}))
        assert state.get_battery_percentage() == 100.0

    def test_battery_clamps_below_0(self):
        sc, state = self._make()
        run(sc.updateBattery({"percentage": -10.0}))
        assert state.get_battery_percentage() == 0.0

    def test_battery_missing_key_ignored(self):
        sc, state = self._make()
        run(sc.updateBattery({}))
        assert state.get_battery_percentage() is None

    def test_battery_none_value_ignored(self):
        sc, state = self._make()
        run(sc.updateBattery({"percentage": None}))
        assert state.get_battery_percentage() is None

    def test_battery_notifies_listeners(self):
        sc, _ = self._make()
        received = []
        async def cb(d): received.append(d)
        sc.attach_listener(cb)
        run(sc.updateBattery({"percentage": 0.5}))
        assert len(received) == 1
        assert "isOn" in received[0]

    # ── updateWifi / Pi / Comms ────────────────────────────────────────────────

    def test_wifi_sets_true(self):
        sc, state = self._make()
        run(sc.updateWifi({"data": True}))
        assert state.get_is_wifi_connected() is True

    def test_wifi_sets_false(self):
        sc, state = self._make()
        run(sc.updateWifi({"data": False}))
        assert state.get_is_wifi_connected() is False

    def test_wifi_notifies_listeners(self):
        sc, _ = self._make()
        received = []
        async def cb(d): received.append(d)
        sc.attach_listener(cb)
        run(sc.updateWifi({"data": True}))
        assert len(received) == 1

    def test_wifi_none_val_not_applied(self):
        sc, state = self._make()
        run(sc.updateWifi({}))  # _extract_bool returns None — no update
        assert state.get_is_wifi_connected() is None

    def test_pi_sets_true(self):
        sc, state = self._make()
        run(sc.updatePiConnection({"data": True}))
        assert state.get_is_raspberry_pi_connected() is True

    def test_pi_notifies_listeners(self):
        sc, _ = self._make()
        received = []
        async def cb(d): received.append(d)
        sc.attach_listener(cb)
        run(sc.updatePiConnection({"data": True}))
        assert len(received) == 1

    def test_comms_sets_true(self):
        sc, state = self._make()
        run(sc.updateCommsConnection({"value": True}))
        assert state.get_is_comms_connected() is True

    def test_comms_notifies_listeners(self):
        sc, _ = self._make()
        received = []
        async def cb(d): received.append(d)
        sc.attach_listener(cb)
        run(sc.updateCommsConnection({"value": False}))
        assert len(received) == 1

    # ── _extract_bool_from_msg ─────────────────────────────────────────────────

    def test_extract_bool_direct_true(self):
        sc, _ = self._make()
        assert sc._extract_bool_from_msg(True) is True

    def test_extract_bool_direct_false(self):
        sc, _ = self._make()
        assert sc._extract_bool_from_msg(False) is False

    def test_extract_bool_from_data_key(self):
        sc, _ = self._make()
        assert sc._extract_bool_from_msg({"data": True}) is True

    def test_extract_bool_from_value_key(self):
        sc, _ = self._make()
        assert sc._extract_bool_from_msg({"value": False}) is False

    def test_extract_bool_none_returns_none(self):
        sc, _ = self._make()
        assert sc._extract_bool_from_msg(None) is None

    def test_extract_bool_unknown_dict_returns_none(self):
        sc, _ = self._make()
        assert sc._extract_bool_from_msg({"other": 1}) is None

    # ── attach_listener / detach ───────────────────────────────────────────────

    def test_attach_returns_callable_detach(self):
        sc, _ = self._make()
        assert callable(sc.attach_listener(AsyncMock()))

    def test_detach_removes_listener(self):
        sc, _ = self._make()
        cb = AsyncMock()
        detach = sc.attach_listener(cb)
        detach()
        assert cb not in sc._listeners

    def test_detach_twice_is_safe(self):
        sc, _ = self._make()
        cb = AsyncMock()
        detach = sc.attach_listener(cb)
        detach()
        detach()  # should not raise

    # ── _notify_listeners ──────────────────────────────────────────────────────

    def test_notify_calls_all_listeners(self):
        sc, _ = self._make()
        cb1, cb2 = AsyncMock(), AsyncMock()
        sc.attach_listener(cb1)
        sc.attach_listener(cb2)
        run(sc._notify_listeners())
        cb1.assert_called_once()
        cb2.assert_called_once()

    def test_notify_passes_robot_state_json(self):
        sc, _ = self._make()
        received = []
        async def cb(d): received.append(d)
        sc.attach_listener(cb)
        run(sc._notify_listeners())
        assert "isOn" in received[0]

    def test_notify_ignores_failing_listener(self):
        sc, _ = self._make()
        async def bad(d): raise RuntimeError("boom")
        sc.attach_listener(bad)
        run(sc._notify_listeners())  # should not raise

    def test_notify_no_listeners_is_safe(self):
        sc, _ = self._make()
        run(sc._notify_listeners())  # should not raise

    # ── bridge callbacks (_battery_cb, _wifi_cb, _pi_cb, _comms_cb) ───────────

    def test_battery_cb_schedules_update(self):
        sc, _ = self._make()
        sc._loop = MagicMock()
        sc._battery_cb({"percentage": 0.8})
        sc._loop.call_soon_threadsafe.assert_called_once()

    def test_wifi_cb_schedules_update(self):
        sc, _ = self._make()
        sc._loop = MagicMock()
        sc._wifi_cb({"data": True})
        sc._loop.call_soon_threadsafe.assert_called_once()

    def test_pi_cb_schedules_update(self):
        sc, _ = self._make()
        sc._loop = MagicMock()
        sc._pi_cb({"data": True})
        sc._loop.call_soon_threadsafe.assert_called_once()

    def test_comms_cb_schedules_update(self):
        sc, _ = self._make()
        sc._loop = MagicMock()
        sc._comms_cb({"data": True})
        sc._loop.call_soon_threadsafe.assert_called_once()

    # ── _connect_and_subscribe success / failure paths ─────────────────────────

    def test_connect_success_sets_is_on_true(self):
        robot_state = RobotState(path_model=Path())
        loop = asyncio.get_event_loop()

        with patch("turtlebot4_backend.turtlebot4_controller.StatusController.RosbridgeConnection") as MockRos, \
             patch("threading.Thread") as MockThread:
            mock_ros = MagicMock()
            MockRos.return_value = mock_ros
            captured_target = {}

            def capture_thread(**kwargs):
                captured_target['fn'] = kwargs.get('target')
                m = MagicMock()
                m.start = MagicMock()
                return m

            MockThread.side_effect = capture_thread
            sc = StatusController(robot_state=robot_state, loop=loop)

        # Run the thread target directly — simulates successful connection
        mock_ros.connect.return_value = None
        mock_ros.subscribe = MagicMock()
        captured_target['fn']()

        # Flush the scheduled coroutine
        run(asyncio.sleep(0))
        assert robot_state.get_is_on() is True

    def test_connect_failure_sets_is_on_false(self):
        robot_state = RobotState(path_model=Path())
        run(robot_state.set_is_on(True))  # start as on
        loop = asyncio.get_event_loop()

        with patch("turtlebot4_backend.turtlebot4_controller.StatusController.RosbridgeConnection") as MockRos, \
             patch("threading.Thread") as MockThread:
            mock_ros = MagicMock()
            MockRos.return_value = mock_ros
            captured_target = {}

            def capture_thread(**kwargs):
                captured_target['fn'] = kwargs.get('target')
                m = MagicMock()
                m.start = MagicMock()
                return m

            MockThread.side_effect = capture_thread
            sc = StatusController(robot_state=robot_state, loop=loop)

        # Simulate connection failure
        mock_ros.connect.side_effect = Exception("connection refused")
        captured_target['fn']()

        run(asyncio.sleep(0))
        assert robot_state.get_is_on() is False

    # ── stop ──────────────────────────────────────────────────────────────────

    def test_stop_calls_terminate(self):
        sc, _ = self._make()
        sc.stop()
        sc._ros.terminate.assert_called_once()

    def test_stop_safe_when_terminate_raises(self):
        sc, _ = self._make()
        sc._ros.terminate.side_effect = Exception("err")
        sc.stop()  # should not raise

# ═════════════════════════════════════════════
# RosbridgeConnection
# ═════════════════════════════════════════════

class TestRosbridgeConnection:
    """
    All roslibpy calls are mocked — no real socket or ROS instance needed.
    Each method's logic branches are tested directly.
    """

    def _make(self, connected=False):
        """Return a RosbridgeConnection with roslibpy fully mocked."""
        rc = RosbridgeConnection(host='localhost', port=9090)
        if connected:
            rc.client = MagicMock()
            rc.isConnected = True
        return rc

    def _make_topic(self):
        t = MagicMock()
        t.subscribe = MagicMock()
        t.unsubscribe = MagicMock()
        t.publish = MagicMock()
        return t

    # ── __init__ ──────────────────────────────────────────────────────────────

    def test_init_defaults(self):
        rc = self._make()
        assert rc.host == 'localhost'
        assert rc.port == 9090
        assert rc.client is None
        assert rc.isConnected is False
        assert rc._topics == {}
        assert rc._services == {}

    def test_init_custom_host_port(self):
        rc = RosbridgeConnection(host='192.168.1.1', port=1234)
        assert rc.host == '192.168.1.1'
        assert rc.port == 1234

    # ── connect ───────────────────────────────────────────────────────────────

    def test_connect_sets_is_connected(self):
        rc = self._make()
        mock_ros = MagicMock()
        mock_ros.is_connected = True
        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.Ros.return_value = mock_ros
            rc.connect()
        assert rc.isConnected is True
        assert rc.client is mock_ros

    def test_connect_skips_if_already_connected(self):
        rc = self._make(connected=True)
        existing_client = rc.client
        rc.connect()  # should return immediately
        assert rc.client is existing_client

    def test_connect_raises_on_timeout(self):
        rc = self._make()
        mock_ros = MagicMock()
        mock_ros.is_connected = False  # never becomes connected
        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy, \
             patch('time.sleep'), \
             patch('time.time', side_effect=[0, 0, 10]):  # instant timeout
            mock_roslibpy.Ros.return_value = mock_ros
            with pytest.raises(RuntimeError, match='Could not connect'):
                rc.connect(timeout=5.0)

    # ── subscribe ─────────────────────────────────────────────────────────────

    def test_subscribe_raises_when_not_connected(self):
        rc = self._make()
        with pytest.raises(RuntimeError, match='Not connected'):
            rc.subscribe('/test', 'std_msgs/msg/Bool', lambda m: None)

    def test_subscribe_creates_and_caches_topic(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.Topic.return_value = mock_topic
            cb = lambda m: None
            result = rc.subscribe('/battery', 'sensor_msgs/msg/BatteryState', cb)
        assert '/battery' in rc._topics
        assert result is mock_topic
        mock_topic.subscribe.assert_called_once_with(cb)

    def test_subscribe_reuses_existing_topic(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        rc._topics['/battery'] = mock_topic
        cb = lambda m: None
        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            rc.subscribe('/battery', 'sensor_msgs/msg/BatteryState', cb)
            mock_roslibpy.Topic.assert_not_called()
        mock_topic.subscribe.assert_called_once_with(cb)

    def test_subscribe_returns_topic(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.Topic.return_value = mock_topic
            result = rc.subscribe('/odom', 'nav_msgs/msg/Odometry', lambda m: None)
        assert result is mock_topic

    # ── unsubscribe ───────────────────────────────────────────────────────────

    def test_unsubscribe_unknown_topic_is_safe(self):
        rc = self._make(connected=True)
        rc.unsubscribe('/nonexistent')  # should not raise

    def test_unsubscribe_all_callbacks(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        rc._topics['/test'] = mock_topic
        rc.unsubscribe('/test')
        mock_topic.unsubscribe.assert_called_once_with()

    def test_unsubscribe_specific_callback(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        rc._topics['/test'] = mock_topic
        cb = lambda m: None
        rc.unsubscribe('/test', callback=cb)
        mock_topic.unsubscribe.assert_called_once_with(cb)

    def test_unsubscribe_safe_when_raises(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        mock_topic.unsubscribe.side_effect = Exception("err")
        rc._topics['/test'] = mock_topic
        rc.unsubscribe('/test')  # should not raise

    # ── publish ───────────────────────────────────────────────────────────────

    def test_publish_raises_when_not_connected(self):
        rc = self._make()
        with pytest.raises(RuntimeError, match='Not connected'):
            rc.publish('/cmd_vel', {}, msg_type='geometry_msgs/msg/Twist')

    def test_publish_raises_without_msg_type_for_new_topic(self):
        rc = self._make(connected=True)
        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy'):
            with pytest.raises(ValueError, match='msg_type is required'):
                rc.publish('/cmd_vel', {})

    def test_publish_creates_topic_on_first_use(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.Topic.return_value = mock_topic
            mock_roslibpy.Message.return_value = MagicMock()
            rc.publish('/cmd_vel', {'linear': {'x': 1.0}}, msg_type='geometry_msgs/msg/Twist')
        assert '/cmd_vel' in rc._topics
        mock_topic.publish.assert_called_once()

    def test_publish_reuses_existing_topic(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        rc._topics['/cmd_vel'] = mock_topic
        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.Message.return_value = MagicMock()
            mock_roslibpy.Topic.return_value = MagicMock()
            rc.publish('/cmd_vel', {'linear': {'x': 0.0}})
            mock_roslibpy.Topic.assert_not_called()
        mock_topic.publish.assert_called_once()

    # ── call_service ──────────────────────────────────────────────────────────

    def test_call_service_raises_when_not_connected(self):
        rc = self._make()
        with pytest.raises(RuntimeError, match='Not connected'):
            rc.call_service('/my_srv', 'std_srvs/srv/Trigger', {})

    def test_call_service_returns_response_on_success(self):
        rc = self._make(connected=True)
        mock_service = MagicMock()

        def fake_call(req, callback, error_callback):
            callback({'result': 'ok'})

        mock_service.call.side_effect = fake_call

        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.Service.return_value = mock_service
            mock_roslibpy.ServiceRequest.return_value = MagicMock()
            result = rc.call_service('/my_srv', 'std_srvs/srv/Trigger', {})

        assert result == {'result': 'ok'}

    def test_call_service_reuses_existing_service(self):
        rc = self._make(connected=True)
        mock_service = MagicMock()

        def fake_call(req, callback, error_callback):
            callback({'result': 'ok'})

        mock_service.call.side_effect = fake_call
        rc._services['/my_srv'] = mock_service

        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.ServiceRequest.return_value = MagicMock()
            mock_roslibpy.Service.return_value = MagicMock()
            rc.call_service('/my_srv', 'std_srvs/srv/Trigger', {})
            mock_roslibpy.Service.assert_not_called()

    def test_call_service_raises_on_error_response(self):
        rc = self._make(connected=True)
        mock_service = MagicMock()

        def fake_call(req, callback, error_callback):
            error_callback('something went wrong')

        mock_service.call.side_effect = fake_call

        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.Service.return_value = mock_service
            mock_roslibpy.ServiceRequest.return_value = MagicMock()
            with pytest.raises(RuntimeError, match='Service call error'):
                rc.call_service('/my_srv', 'std_srvs/srv/Trigger', {})

    def test_call_service_raises_on_timeout(self):
        rc = self._make(connected=True)
        mock_service = MagicMock()
        mock_service.call.return_value = None  # never calls callback

        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.Service.return_value = mock_service
            mock_roslibpy.ServiceRequest.return_value = MagicMock()
            with pytest.raises(TimeoutError, match='did not respond'):
                rc.call_service('/my_srv', 'std_srvs/srv/Trigger', {}, timeout=0.01)

    # ── send_action_goal ──────────────────────────────────────────────────────

    def test_send_action_goal_raises_when_not_connected(self):
        rc = self._make()
        with pytest.raises(RuntimeError, match='Not connected'):
            rc.send_action_goal('/dock', 'irobot_create_msgs/action/Dock', {})

    def test_send_action_goal_sends_goal(self):
        rc = self._make(connected=True)
        mock_action_client = MagicMock()
        mock_action_client.wait_for_server.return_value = True
        mock_goal = MagicMock()

        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.actionlib.ActionClient.return_value = mock_action_client
            mock_roslibpy.actionlib.Goal.return_value = mock_goal
            rc.send_action_goal('/dock', 'irobot_create_msgs/action/Dock', {})

        mock_goal.send.assert_called_once()

    def test_send_action_goal_raises_on_server_timeout(self):
        rc = self._make(connected=True)
        mock_action_client = MagicMock()
        mock_action_client.wait_for_server.return_value = False  # server unavailable

        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.actionlib.ActionClient.return_value = mock_action_client
            with pytest.raises(TimeoutError, match='not available'):
                rc.send_action_goal('/dock', 'irobot_create_msgs/action/Dock', {})

    def test_send_action_goal_reuses_action_client(self):
        rc = self._make(connected=True)
        mock_action_client = MagicMock()
        mock_action_client.wait_for_server.return_value = True
        mock_goal = MagicMock()
        rc._actions['/dock'] = mock_action_client

        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.actionlib.ActionClient.return_value = MagicMock()
            mock_roslibpy.actionlib.Goal.return_value = mock_goal
            rc.send_action_goal('/dock', 'irobot_create_msgs/action/Dock', {})
            mock_roslibpy.actionlib.ActionClient.assert_not_called()

    def test_send_action_goal_registers_result_callback(self):
        rc = self._make(connected=True)
        mock_action_client = MagicMock()
        mock_action_client.wait_for_server.return_value = True
        mock_goal = MagicMock()
        result_cb = MagicMock()

        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.actionlib.ActionClient.return_value = mock_action_client
            mock_roslibpy.actionlib.Goal.return_value = mock_goal
            rc.send_action_goal('/dock', 'irobot_create_msgs/action/Dock', {},
                                result_callback=result_cb)

        on_calls = [c[0][0] for c in mock_goal.on.call_args_list]
        assert 'result' in on_calls

    def test_send_action_goal_registers_feedback_callback(self):
        rc = self._make(connected=True)
        mock_action_client = MagicMock()
        mock_action_client.wait_for_server.return_value = True
        mock_goal = MagicMock()
        feedback_cb = MagicMock()

        with patch('turtlebot4_backend.turtlebot4_controller.RosbridgeConnection.roslibpy') as mock_roslibpy:
            mock_roslibpy.actionlib.ActionClient.return_value = mock_action_client
            mock_roslibpy.actionlib.Goal.return_value = mock_goal
            rc.send_action_goal('/dock', 'irobot_create_msgs/action/Dock', {},
                                feedback_callback=feedback_cb)

        on_calls = [c[0][0] for c in mock_goal.on.call_args_list]
        assert 'feedback' in on_calls

    # ── terminate ─────────────────────────────────────────────────────────────

    def test_terminate_clears_topics_and_services(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        rc._topics['/test'] = mock_topic
        rc._services['/srv'] = MagicMock()
        rc.terminate()
        assert rc._topics == {}
        assert rc._services == {}

    def test_terminate_sets_not_connected(self):
        rc = self._make(connected=True)
        rc.terminate()
        assert rc.isConnected is False
        assert rc.client is None

    def test_terminate_unsubscribes_all_topics(self):
        rc = self._make(connected=True)
        t1, t2 = self._make_topic(), self._make_topic()
        rc._topics['/a'] = t1
        rc._topics['/b'] = t2
        rc.terminate()
        t1.unsubscribe.assert_called_once()
        t2.unsubscribe.assert_called_once()

    def test_terminate_safe_when_unsubscribe_raises(self):
        rc = self._make(connected=True)
        mock_topic = self._make_topic()
        mock_topic.unsubscribe.side_effect = Exception("err")
        rc._topics['/test'] = mock_topic
        rc.terminate()  # should not raise

    def test_terminate_safe_when_client_terminate_raises(self):
        rc = self._make(connected=True)
        rc.client.terminate.side_effect = Exception("err")
        rc.terminate()  # should not raise

    def test_terminate_safe_when_no_client(self):
        rc = self._make()  # client is None
        rc.terminate()  # should not raise
        assert rc.isConnected is False