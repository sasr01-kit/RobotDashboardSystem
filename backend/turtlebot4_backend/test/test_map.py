"""
Unit tests for Map.py.

Map.py has module-level imports of numpy, matplotlib, and geometry_msgs
which are not available outside a ROS environment. This file mocks all
three before importing anything, which is why Map tests must live in their
own isolated file rather than alongside other tests.

Run with:
    PYTHONPATH=backend pytest backend/turtlebot4_backend/test/test_map.py -v
"""

import sys
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

# ── Must happen before ANY turtlebot4_backend import ──────────────────────────
# Replace ROS, numpy, and matplotlib with mocks so Map.py can be imported
# without a ROS workspace or scientific Python stack.
sys.modules['geometry_msgs'] = MagicMock()
sys.modules['geometry_msgs.msg'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['matplotlib'] = MagicMock()
sys.modules['matplotlib.pyplot'] = MagicMock()
# ──────────────────────────────────────────────────────────────────────────────

# Safe to import turtlebot4_backend now
from turtlebot4_backend.turtlebot4_model.Map import Map
from turtlebot4_backend.turtlebot4_model.MapData import MapData
from turtlebot4_backend.turtlebot4_model.Human import Human
from turtlebot4_backend.turtlebot4_model.Observer import Observer


# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────

def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def make_observer():
    class _Obs(Observer):
        def __init__(self):
            self.received = []
        async def update(self, source, data):
            self.received.append(data)
    return _Obs()


def make_map():
    """Return a Map with _convert_mapdata_to_png patched out."""
    m = Map()
    m._convert_mapdata_to_png = MagicMock()
    m._mapDataPNG = "fakepng"
    return m


# ─────────────────────────────────────────────
# Map — __init__
# ─────────────────────────────────────────────

class TestMapInit:

    def test_default_initial_state(self):
        m = make_map()
        assert m._robotPose is None
        assert m._globalGoal is None
        assert m._intermediateWaypoints == []
        assert m._mapDataPNG == "fakepng"

    def test_mapdata_defaults_to_empty_MapData(self):
        m = make_map()
        assert isinstance(m._mapData, MapData)

    def test_convert_called_when_mapdata_provided(self):
        md = MapData(resolution=0.05, width=10.0, height=5.0, occupancyGrid=[0])
        m = Map(mapData=md)
        # _convert_mapdata_to_png is the real one here — just check mapData was stored
        assert m._mapData is md

    def test_initial_waypoints_empty_list(self):
        m = make_map()
        assert m._intermediateWaypoints == []

    def test_custom_initial_values(self):
        pose = {"position": {"x": 1.0, "y": 0.0, "z": 0.0},
                "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}}
        m = Map(robotPose=pose, globalGoal=pose, intermediateWaypoints=[pose])
        m._convert_mapdata_to_png = MagicMock()
        assert m._robotPose == pose
        assert m._globalGoal == pose
        assert len(m._intermediateWaypoints) == 1


# ─────────────────────────────────────────────
# Map — set_robotPose
# ─────────────────────────────────────────────

class TestMapSetRobotPose:

    def test_stores_new_pose(self):
        m = make_map()
        pose = {"position": {"x": 1.0, "y": 2.0, "z": 0.0},
                "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}}
        run(m.set_robotPose(pose))
        assert m._robotPose == pose

    def test_notifies_with_POSE_DATA(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        run(m.set_robotPose({"position": {"x": 1.0, "y": 0.0, "z": 0.0},
                              "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}}))
        assert any(d.get("type") == "POSE_DATA" for d in obs.received)

    def test_accepts_none(self):
        m = make_map()
        run(m.set_robotPose(None))
        assert m._robotPose is None


# ─────────────────────────────────────────────
# Map — set_globalGoal
# ─────────────────────────────────────────────

class TestMapSetGlobalGoal:

    def test_stores_new_goal(self):
        m = make_map()
        goal = {"position": {"x": 5.0, "y": 3.0, "z": 0.0},
                "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}}
        run(m.set_globalGoal(goal))
        assert m._globalGoal == goal

    def test_notifies_with_POSE_DATA(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        run(m.set_globalGoal({"position": {"x": 1.0, "y": 0.0, "z": 0.0},
                               "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}}))
        assert any(d.get("type") == "POSE_DATA" for d in obs.received)


# ─────────────────────────────────────────────
# Map — set_intermediateWaypoints
# ─────────────────────────────────────────────

class TestMapSetIntermediateWaypoints:

    def test_stores_waypoints(self):
        m = make_map()
        wps = [{"position": {"x": 1, "y": 1, "z": 0},
                "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}}]
        run(m.set_intermediateWaypoints(wps))
        assert m._intermediateWaypoints == wps

    def test_notifies_with_POSE_DATA(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        run(m.set_intermediateWaypoints([]))
        assert any(d.get("type") == "POSE_DATA" for d in obs.received)

    def test_stores_empty_list(self):
        m = make_map()
        run(m.set_intermediateWaypoints([]))
        assert m._intermediateWaypoints == []


# ─────────────────────────────────────────────
# Map — set_detectedHumans
# ─────────────────────────────────────────────

class TestMapSetDetectedHumans:

    def test_stores_humans(self):
        m = make_map()
        humans = [Human(human_id="h1", position={"x": 1.0, "y": 0.0, "z": 0.0})]
        run(m.set_detectedHumans(humans))
        assert m._detectedHumans == humans

    def test_notifies_with_POSE_DATA(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        run(m.set_detectedHumans([]))
        assert any(d.get("type") == "POSE_DATA" for d in obs.received)

    def test_humans_serialized_in_notification(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        humans = [Human(human_id="h1", position={"x": 1.0, "y": 0.0, "z": 0.0})]
        run(m.set_detectedHumans(humans))
        pose_events = [d for d in obs.received if d.get("type") == "POSE_DATA"]
        assert len(pose_events[0]["humans"]) == 1
        assert pose_events[0]["humans"][0]["id"] == "h1"


# ─────────────────────────────────────────────
# Map — _send_pose_update payload structure
# ─────────────────────────────────────────────

class TestMapSendPoseUpdate:

    def test_payload_contains_all_keys(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        run(m.set_robotPose(None))
        event = [d for d in obs.received if d.get("type") == "POSE_DATA"][0]
        assert "robotPose" in event
        assert "globalGoal" in event
        assert "intermediateWaypoints" in event
        assert "humans" in event

    def test_intermediateWaypoints_is_list(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        run(m.set_robotPose(None))
        event = [d for d in obs.received if d.get("type") == "POSE_DATA"][0]
        assert isinstance(event["intermediateWaypoints"], list)

    def test_humans_is_list(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        run(m.set_robotPose(None))
        event = [d for d in obs.received if d.get("type") == "POSE_DATA"][0]
        assert isinstance(event["humans"], list)


# ─────────────────────────────────────────────
# Map — _pose_to_dict
# ─────────────────────────────────────────────

class TestMapPoseToDict:

    def test_none_returns_none(self):
        assert make_map()._pose_to_dict(None) is None

    def test_dict_pose_extracts_position(self):
        m = make_map()
        pose = {"position": {"x": 1.0, "y": 2.0, "z": 3.0},
                "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}}
        result = m._pose_to_dict(pose)
        assert result["position"]["x"] == 1.0
        assert result["position"]["y"] == 2.0
        assert result["position"]["z"] == 3.0

    def test_dict_pose_extracts_orientation(self):
        m = make_map()
        pose = {"position": {"x": 0.0, "y": 0.0, "z": 0.0},
                "orientation": {"x": 0.1, "y": 0.2, "z": 0.3, "w": 0.9}}
        result = m._pose_to_dict(pose)
        assert result["orientation"]["w"] == 0.9

    def test_dict_pose_missing_keys_use_defaults(self):
        m = make_map()
        result = m._pose_to_dict({"position": {}, "orientation": {}})
        assert result["position"]["x"] == 0.0
        assert result["position"]["y"] == 0.0
        assert result["position"]["z"] == 0.0
        assert result["orientation"]["w"] == 1.0  # default w is 1.0

    def test_empty_dict_uses_all_defaults(self):
        m = make_map()
        result = m._pose_to_dict({})
        assert result["position"]["x"] == 0.0
        assert result["orientation"]["w"] == 1.0

    def test_posestamped_object_uses_attribute_access(self):
        # Simulate a PoseStamped object (non-dict) using a MagicMock
        m = make_map()
        mock_pose = MagicMock()
        mock_pose.pose.position.x = 4.0
        mock_pose.pose.position.y = 5.0
        mock_pose.pose.position.z = 0.0
        mock_pose.pose.orientation.x = 0.0
        mock_pose.pose.orientation.y = 0.0
        mock_pose.pose.orientation.z = 0.0
        mock_pose.pose.orientation.w = 1.0
        result = m._pose_to_dict(mock_pose)
        assert result["position"]["x"] == 4.0
        assert result["orientation"]["w"] == 1.0


# ─────────────────────────────────────────────
# Map — set_mapData
# ─────────────────────────────────────────────

class TestMapSetMapData:

    def test_stores_new_mapdata(self):
        m = make_map()
        md = MapData(resolution=0.05, width=10.0, height=5.0, occupancyGrid=[0])
        run(m.set_mapData(md))
        assert m._mapData is md

    def test_notifies_with_MAP_DATA(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        md = MapData(resolution=0.05, width=10.0, height=5.0, occupancyGrid=[0])
        run(m.set_mapData(md))
        map_events = [d for d in obs.received if d.get("type") == "MAP_DATA"]
        assert len(map_events) == 1

    def test_MAP_DATA_payload_contains_resolution(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        md = MapData(resolution=0.05, width=10.0, height=5.0, occupancyGrid=[0])
        run(m.set_mapData(md))
        event = [d for d in obs.received if d.get("type") == "MAP_DATA"][0]
        assert event["mapData"]["resolution"] == 0.05

    def test_MAP_DATA_payload_contains_png(self):
        m = make_map()
        obs = make_observer()
        m.attach(obs)
        md = MapData(resolution=0.05, width=10.0, height=5.0, occupancyGrid=[0])
        run(m.set_mapData(md))
        event = [d for d in obs.received if d.get("type") == "MAP_DATA"][0]
        assert event["mapData"]["occupancyGridPNG"] == "fakepng"

    def test_calls_convert_mapdata_to_png(self):
        m = make_map()
        md = MapData(resolution=0.05, width=10.0, height=5.0, occupancyGrid=[0])
        run(m.set_mapData(md))
        m._convert_mapdata_to_png.assert_called_once()