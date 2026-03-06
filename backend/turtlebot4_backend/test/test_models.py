"""
Unit tests for turtlebot4_backend model classes.

These tests cover pure Python model logic only — no ROS, no rosbridge,
no network connections required. Run with:

    pytest test_models.py -v
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from turtlebot4_backend.turtlebot4_model.Teleoperate import Teleoperate
from turtlebot4_backend.turtlebot4_model.DirectionCommand import DirectionCommand
from turtlebot4_backend.turtlebot4_model.MapData import MapData
from turtlebot4_backend.turtlebot4_model.Human import Human
from turtlebot4_backend.turtlebot4_model.Path import Path
from turtlebot4_backend.turtlebot4_model.PathLogEntry import PathLogEntry
from turtlebot4_backend.turtlebot4_model.FeedbackLogEntry import FeedbackLogEntry
from turtlebot4_backend.turtlebot4_model.RobotState import RobotState
from turtlebot4_backend.turtlebot4_model.Observer import Observer


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def run(coro):
    """Run an async coroutine from a synchronous test."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ─────────────────────────────────────────────
# DirectionCommand
# ─────────────────────────────────────────────

class TestDirectionCommand:
    """Tests for the DirectionCommand enum."""

    def test_forward_has_positive_linear_x(self):
        msg = DirectionCommand.FORWARD.get_message()
        assert msg['linear']['x'] > 0

    def test_backward_has_negative_linear_x(self):
        msg = DirectionCommand.BACKWARD.get_message()
        assert msg['linear']['x'] < 0

    def test_stop_is_all_zeros(self):
        msg = DirectionCommand.STOP.get_message()
        assert msg['linear']['x'] == 0.0
        assert msg['angular']['z'] == 0.0

    def test_left_has_angular_z(self):
        msg = DirectionCommand.LEFT.get_message()
        assert msg['angular']['z'] != 0.0

    def test_right_has_angular_z(self):
        
        msg = DirectionCommand.RIGHT.get_message()
        assert msg['angular']['z'] != 0.0

    def test_get_message_returns_deep_copy(self):
        
        msg1 = DirectionCommand.FORWARD.get_message()
        msg2 = DirectionCommand.FORWARD.get_message()
        msg1['linear']['x'] = 999
        assert msg2['linear']['x'] != 999  # should not be affected

    def test_create_custom_sets_correct_values(self):
        
        msg = DirectionCommand.create_custom(linear_x=1.5, angular_z=-0.5)
        assert msg['linear']['x'] == 1.5
        assert msg['angular']['z'] == -0.5

    def test_create_custom_defaults_to_zero(self):
        
        msg = DirectionCommand.create_custom()
        assert msg['linear']['x'] == 0.0
        assert msg['angular']['z'] == 0.0

    def test_rotate_left_zero_linear(self):
        
        msg = DirectionCommand.ROTATE_LEFT.get_message()
        assert msg['linear']['x'] == 0.0

    def test_rotate_right_zero_linear(self):
        
        msg = DirectionCommand.ROTATE_RIGHT.get_message()
        assert msg['linear']['x'] == 0.0


# ─────────────────────────────────────────────
# MapData
# ─────────────────────────────────────────────

class TestMapData:
    """Tests for the MapData model."""

    def test_default_values(self):
        md = MapData()
        assert md.get_resolution() == 0.0
        assert md.get_width() == 0.0
        assert md.get_height() == 0.0
        assert md.get_occupancyGrid() == []

    def test_constructor_values(self):
        md = MapData(resolution=0.05, width=10.0, height=5.0, occupancyGrid=[0, 1, -1])
        assert md.get_resolution() == 0.05
        assert md.get_width() == 10.0
        assert md.get_height() == 5.0
        assert md.get_occupancyGrid() == [0, 1, -1]

    def test_setters(self):
        md = MapData()
        md.set_resolution(0.1)
        md.set_width(20.0)
        md.set_height(15.0)
        md.set_occupancyGrid([1, 2, 3])
        assert md.get_resolution() == 0.1
        assert md.get_width() == 20.0
        assert md.get_height() == 15.0
        assert md.get_occupancyGrid() == [1, 2, 3]

    def test_toJSON(self):
        md = MapData(resolution=0.05, width=10.0, height=5.0, occupancyGrid=[0])
        j = md.toJSON()
        assert j['resolution'] == 0.05
        assert j['width'] == 10.0
        assert j['height'] == 5.0
        assert j['occupancyGrid'] == [0]

    def test_none_occupancy_grid_becomes_empty_list(self):
        md = MapData(occupancyGrid=None)
        assert md.get_occupancyGrid() == []


# ─────────────────────────────────────────────
# Human
# ─────────────────────────────────────────────

class TestHuman:
    """Tests for the Human model."""

    def test_default_values(self):
        h = Human()
        assert h.get_id() == ""
        assert h.get_position() == {"x": 0.0, "y": 0.0, "z": 0.0}

    def test_constructor_values(self):
        h = Human(human_id="h1", position={"x": 1.0, "y": 2.0, "z": 0.0})
        assert h.get_id() == "h1"
        assert h.get_position()["x"] == 1.0

    def test_default_proxemic_distances(self):
        h = Human()
        d = h.get_proxemic_distances()
        assert "intimate" in d
        assert "personal" in d
        assert "social" in d
        assert "public" in d

    def test_custom_proxemic_distances(self):
        custom = {"intimate": 0.3, "personal": 1.0, "social": 3.0, "public": 7.0}
        h = Human(proxemic_distances=custom)
        assert h.get_proxemic_distances()["intimate"] == 0.3

    def test_setters(self):
        h = Human()
        h.set_id("h2")
        h.set_position({"x": 5.0, "y": 6.0, "z": 0.0})
        assert h.get_id() == "h2"
        assert h.get_position()["x"] == 5.0

    def test_toJSON(self):
        h = Human(human_id="h3", position={"x": 1.0, "y": 2.0, "z": 0.0})
        j = h.toJSON()
        assert j["id"] == "h3"
        assert j["position"]["x"] == 1.0
        assert "proxemicDistances" in j

    def test_none_position_uses_default(self):
        h = Human(position=None)
        assert h.get_position() == {"x": 0.0, "y": 0.0, "z": 0.0}


# ─────────────────────────────────────────────
# PathLogEntry
# ─────────────────────────────────────────────

class TestPathLogEntry:
    """Tests for the PathLogEntry model."""

    def test_default_values(self):
        e = PathLogEntry()
        assert e.get_label() == ""
        assert e.get_id() == ""
        assert e.get_goal_type() == ""
        assert e.get_timestamp() is None
        assert e.get_fuzzy_output() == ""
        assert e.get_user_feedback() == ""

    def test_constructor_values(self):
        ts = datetime(2024, 1, 1)
        e = PathLogEntry(label="Test", id="goal_1", goal_type="global", timestamp=ts,
                         fuzzy_output="rule1", user_feedback="good")
        assert e.get_label() == "Test"
        assert e.get_id() == "goal_1"
        assert e.get_goal_type() == "global"
        assert e.get_timestamp() == ts
        assert e.get_fuzzy_output() == "rule1"
        assert e.get_user_feedback() == "good"

    def test_setters(self):
        e = PathLogEntry()
        e.set_label("NewLabel")
        e.set_id("goal_99")
        e.set_goal_type("intermediate")
        e.set_fuzzy_output("rule_x")
        e.set_user_feedback("bad")
        assert e.get_label() == "NewLabel"
        assert e.get_id() == "goal_99"
        assert e.get_goal_type() == "intermediate"
        assert e.get_fuzzy_output() == "rule_x"
        assert e.get_user_feedback() == "bad"

    def test_set_timestamp(self):
        e = PathLogEntry()
        ts = datetime(2025, 6, 15)
        e.set_timestamp(ts)
        assert e.get_timestamp() == ts

    def test_set_timestamp_none(self):
        e = PathLogEntry(timestamp=datetime.now())
        e.set_timestamp(None)
        assert e.get_timestamp() is None


# ─────────────────────────────────────────────
# FeedbackLogEntry
# ─────────────────────────────────────────────

class TestFeedbackLogEntry:
    """Tests for the FeedbackLogEntry model."""

    def test_default_values(self):
        f = FeedbackLogEntry()
        assert f.get_duration() == ""
        assert f.get_start_point() == ""
        assert f.get_end_point() == ""
        assert f.get_feedback() == ""

    def test_constructor_values(self):
        f = FeedbackLogEntry(duration="5s", start_point="A", end_point="B", feedback="good")
        assert f.get_duration() == "5s"
        assert f.get_start_point() == "A"
        assert f.get_end_point() == "B"
        assert f.get_feedback() == "good"

    def test_setters(self):
        f = FeedbackLogEntry()
        f.set_duration("10s")
        f.set_start_point("C")
        f.set_end_point("D")
        f.set_feedback("bad")
        assert f.get_duration() == "10s"
        assert f.get_start_point() == "C"
        assert f.get_end_point() == "D"
        assert f.get_feedback() == "bad"


# ─────────────────────────────────────────────
# Teleoperate
# ─────────────────────────────────────────────

class TestTeleoperate:
    """Tests for the Teleoperate model."""

    def test_initial_empty_queue(self):
        ""
        t = Teleoperate()
        assert t.get_command() is None

    def test_add_command_queues_it(self):
        
        t = Teleoperate()
        t.add_command("FORWARD")
        assert t.get_command() == "FORWARD"

    def test_commands_are_fifo(self):
        
        t = Teleoperate()
        t.add_command("FORWARD")
        t.add_command("LEFT")
        assert t.get_command() == "FORWARD"
        assert t.get_command() == "LEFT"

    def test_stop_clears_queue(self):
        
        t = Teleoperate()
        t.add_command("FORWARD")
        t.add_command("LEFT")
        t.add_command("STOP")
        # Only STOP should remain after the clear
        assert t.get_command() == "STOP"
        assert t.get_command() is None

    def test_get_command_returns_none_when_empty(self):
        t = Teleoperate()
        assert t.get_command() is None
        assert t.get_command() is None  # still None on repeat

    def test_attach_and_notify(self):
        
        t = Teleoperate()
        calls = []
        t.attach(lambda src, data: calls.append("called"))
        t.add_command("FORWARD")
        assert len(calls) == 1

    def test_detach_stops_notifications(self):
        
        t = Teleoperate()
        calls = []
        cb = lambda src, data: calls.append("called")
        t.attach(cb)
        t.detach(cb)
        t.add_command("FORWARD")
        assert len(calls) == 0

    def test_fromJSON_adds_command(self):
        
        t = Teleoperate()
        t.fromJSON({"command": "BACKWARD"})
        assert t.get_command() == "BACKWARD"

    def test_fromJSON_ignores_missing_command(self):
        
        t = Teleoperate()
        t.fromJSON({"other_key": "value"})
        assert t.get_command() is None

    def test_duplicate_attach_ignored(self):
        
        t = Teleoperate()
        calls = []
        cb = lambda src, data: calls.append("called")
        t.attach(cb)
        t.attach(cb)  # attaching same callback twice
        t.add_command("FORWARD")
        assert len(calls) == 1  # only called once


# ─────────────────────────────────────────────
# Path model
# ─────────────────────────────────────────────

class TestPath:
    """Tests for the Path model."""

    def test_default_values(self):
        p = Path()
        assert p.get_path_history() == []
        assert p.get_is_path_module_active() is False
        assert p.get_is_docked() is False

    def test_constructor_values(self):
        entry = PathLogEntry(id="goal_1")
        p = Path(path_history=[entry], is_path_module_active=True, is_docked=True)
        assert len(p.get_path_history()) == 1
        assert p.get_is_path_module_active() is True
        assert p.get_is_docked() is True

    def test_set_is_path_module_active_notifies(self):
        p = Path()
        received = []

        async def observer_fn(source, data):
            received.append(data)

        from turtlebot4_backend.turtlebot4_model.Observer import Observer

        class MockObserver(Observer):
            async def update(self, source, data):
                received.append(data)

        p.attach(MockObserver())
        run(p.set_is_path_module_active(True))
        assert any(d.get("type") == "PATH_UPDATE" for d in received)

    def test_set_is_path_module_active_no_notify_if_same(self):
        p = Path(is_path_module_active=True)
        received = []

        class MockObserver(Observer):
            async def update(self, source, data):
                received.append(data)

        p.attach(MockObserver())
        run(p.set_is_path_module_active(True))  # no change
        assert len(received) == 0

    def test_set_is_docked_notifies(self):

        p = Path()
        received = []

        class MockObserver(Observer):
            async def update(self, source, data):
                received.append(data)

        p.attach(MockObserver())
        run(p.set_is_docked(True))
        assert any(d.get("type") == "PATH_UPDATE" for d in received)

    def test_set_is_docked_no_notify_if_same(self):

        p = Path(is_docked=False)
        received = []

        class MockObserver(Observer):
            async def update(self, source, data):
                received.append(data)

        p.attach(MockObserver())
        run(p.set_is_docked(False))  # no change
        assert len(received) == 0

    def test_set_path_history_notifies(self):

        p = Path()
        received = []

        class MockObserver(Observer):
            async def update(self, source, data):
                received.append(data)

        p.attach(MockObserver())
        run(p.set_path_history([PathLogEntry(id="g1")]))
        assert any(d.get("type") == "PATH_UPDATE" for d in received)

    def test_set_path_controller(self):
        p = Path()
        mock_ctrl = MagicMock()
        p.set_path_controller(mock_ctrl)
        assert p._path_controller is mock_ctrl


# ─────────────────────────────────────────────
# RobotState model
# ─────────────────────────────────────────────

class TestRobotState:
    """Tests for the RobotState model."""

    def _make_state(self):
        path = Path()
        return RobotState(path_model=path)

    def test_default_values(self):
        state = self._make_state()
        assert state.get_is_on() is False
        assert state.get_battery_percentage() is None
        assert state.get_is_wifi_connected() is None
        assert state.get_is_comms_connected() is None
        assert state.get_is_raspberry_pi_connected() is None

    def test_set_is_on_notifies(self):
        state = self._make_state()
        received = []

        class MockObserver(Observer):
            async def update(self, source, data):
                received.append(data)

        state.attach(MockObserver())
        run(state.set_is_on(True))
        assert state.get_is_on() is True
        assert any(d.get("type") == "STATUS_UPDATE" for d in received)

    def test_set_is_on_no_notify_if_same(self):
        state = self._make_state()
        received = []

        class MockObserver(Observer):
            async def update(self, source, data):
                received.append(data)

        state.attach(MockObserver())
        run(state.set_is_on(False))  # already False
        assert len(received) == 0

    def test_set_battery_percentage_clamped_above_100(self):
        state = self._make_state()
        run(state.set_battery_percentage(150.0))
        assert state.get_battery_percentage() == 100.0

    def test_set_battery_percentage_clamped_below_0(self):
        state = self._make_state()
        run(state.set_battery_percentage(-10.0))
        assert state.get_battery_percentage() == 0.0

    def test_set_battery_percentage_valid(self):
        state = self._make_state()
        run(state.set_battery_percentage(75.0))
        assert state.get_battery_percentage() == 75.0

    def test_set_wifi_connected(self):
        state = self._make_state()
        run(state.set_is_wifi_connected(True))
        assert state.get_is_wifi_connected() is True

    def test_set_comms_connected(self):
        state = self._make_state()
        run(state.set_is_comms_connected(True))
        assert state.get_is_comms_connected() is True

    def test_set_raspberry_pi_connected(self):
        state = self._make_state()
        run(state.set_is_raspberry_pi_connected(False))
        assert state.get_is_raspberry_pi_connected() is False

    def test_toJSON_contains_expected_keys(self):
        state = self._make_state()
        j = state.toJSON()
        for key in ["isOn", "batteryPercentage", "isWifiConnected",
                    "isCommsConnected", "isRaspberryPiConnected", "mode", "isDocked"]:
            assert key in j

    def test_toJSON_mode_teleoperating_when_path_inactive(self):
        state = self._make_state()
        j = state.toJSON()
        assert j["mode"] == "Teleoperating"

    def test_toJSON_mode_path_module_when_active(self):

        path = Path(is_path_module_active=True)
        state = RobotState(path_model=path)
        j = state.toJSON()
        assert j["mode"] == "Running Path Module"


