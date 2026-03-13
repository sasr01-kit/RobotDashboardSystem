from unittest.mock import MagicMock, patch
from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI
from pixelbot_backend.pixelbot_controller.SessionAPI import SessionAPI
from pixelbot_backend.pixelbot_model.Child import Child
from pixelbot_backend.pixelbot_model.Session import Session
from pixelbot_backend.pixelbot_model.DrawingData import DrawingData
from pixelbot_backend.pixelbot_model.DrawingSelfDisclosureWidth import DrawingSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureWidth import SpeechSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureDepth import SpeechSelfDisclosureDepth
from pixelbot_backend.pixelbot_storage.RemoteDataLoader import RemoteDataLoader
import datetime
import pytest

'''This test_apis.py file contains unit tests for the ChildAPI and SessionAPI classes in the Pixelbot backend. 
    It uses pytest and unittest.mock to test the behavior of these APIs, including their interactions with the data'''
# ──────────────────────────────────────────────
# Shared fixtures
# ──────────────────────────────────────────────

def make_session(session_id="session_0"):
    return Session(
        session_id=session_id,
        session_date=datetime.datetime(2024, 3, 15),
        drawing=DrawingData("abc123"),
        story_summary=[{"name": "cat", "description": "a cat"}],
        transcript=[{"name": "Child", "description": "Hello"}],
        speech_width=SpeechSelfDisclosureWidth(
            intervention_count=3,
            total_word_count=100,
            average_word_count_per_intervention=33.3,
            std_word_count_per_intervention=5.0,
            total_speech_time=60.0,
            average_speech_time_per_intervention=20.0,
            std_speech_time_per_intervention=2.0,
        ),
        speech_depth=SpeechSelfDisclosureDepth(
            average_intimacy_score=0.7,
            std_intimacy_score=0.1,
        ),
        drawing_width=DrawingSelfDisclosureWidth(
            stroke_count=10,
            total_stroke_length=500.0,
            average_stroke_length=50.0,
            std_stroke_length=5.0,
            color_used_count=3,
            pen_size_used_count=2,
            amount_filled_area=0.4,
        ),
    )


def make_child(child_id="child_abc", name="Alice", num_sessions=2):
    sessions = [make_session(f"session_{i}") for i in range(num_sessions)]
    return Child(child_id=child_id, name=name, sessions=sessions)


# ──────────────────────────────────────────────
# ChildAPI tests
# ──────────────────────────────────────────────

class TestChildAPI:

    def setup_method(self):
        self.mock_repository = MagicMock()

    def test_load_children_objects_returns_from_repository(self):
        """load_children_objects always reads from repository JSON."""
        children = [make_child()]
        self.mock_repository.load_children.return_value = children

        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        result = api.load_children_objects()

        self.mock_repository.load_children.assert_called_once()
        assert result == children

    def test_load_children_objects_returns_empty_list_when_no_data(self):
        """Returns [] when repository has no data."""
        self.mock_repository.load_children.return_value = []

        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        result = api.load_children_objects()

        assert result == []

     # --- background_refresh ---
    def setup_method(self):
        self.mock_repository = MagicMock()

    @patch("pixelbot_backend.pixelbot_controller.ChildAPI.time.sleep")
    def test_syncs_once_when_robot_comes_online(self, mock_sleep):
        """Syncs only when robot transitions from offline to online."""
        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        
        # Robot is offline first, then comes online
        availability = [False, True, True]
        call_count = 0

        def fake_is_robot_available(url):
            nonlocal call_count
            result = availability[min(call_count, len(availability) - 1)]
            call_count += 1
            if call_count >= len(availability):
                raise StopIteration  # stop the loop
            return result

        with patch.object(api, "is_robot_available", side_effect=fake_is_robot_available):
            with patch.object(api, "refresh_from_source") as mock_refresh:
                with pytest.raises(StopIteration):
                    api.background_refresh()
                # Should only sync once (when transitioning False → True)
                assert mock_refresh.call_count == 1

    @patch("pixelbot_backend.pixelbot_controller.ChildAPI.time.sleep")
    def test_does_not_sync_when_robot_stays_offline(self, mock_sleep):
        """Does not sync when robot never comes online."""
        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        call_count = 0

        def fake_is_robot_available(url):
            nonlocal call_count
            call_count += 1
            if call_count >= 3:
                raise StopIteration
            return False

        with patch.object(api, "is_robot_available", side_effect=fake_is_robot_available):
            with patch.object(api, "refresh_from_source") as mock_refresh:
                with pytest.raises(StopIteration):
                    api.background_refresh()
                mock_refresh.assert_not_called()

    @patch("pixelbot_backend.pixelbot_controller.ChildAPI.time.sleep")
    def test_end_of_day_sync_triggers_at_20(self, mock_sleep):
        """End of day sync triggers at 20:00 when robot is available."""
        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        call_count = 0

        def fake_is_robot_available(url):
            nonlocal call_count
            call_count += 1
            if call_count >= 2:
                raise StopIteration
            return True

        fake_time = datetime.datetime(2024, 1, 1, 20, 0, 0)  # exactly 20:00

        with patch.object(api, "is_robot_available", side_effect=fake_is_robot_available):
            with patch.object(api, "refresh_from_source") as mock_refresh:
                with patch("pixelbot_backend.pixelbot_controller.ChildAPI.datetime") as mock_dt:
                    mock_dt.datetime.now.return_value = fake_time
                    with pytest.raises(StopIteration):
                        api.background_refresh()
                    mock_refresh.assert_called_once()
    

    # --- refresh_from_source ---

    @patch("pixelbot_backend.pixelbot_controller.ChildAPI.RemoteDataLoader")
    def test_refresh_from_source_loads_from_robot_when_available(self, MockRemoteLoader):
        """refresh_from_source fetches from robot and updates repository."""
        raw_children = [make_child()]
        MockRemoteLoader.return_value.load_all_children.return_value = raw_children

        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        with patch.object(api, "is_robot_available", return_value=True):
            api.refresh_from_source()

        MockRemoteLoader.assert_called_once_with("http://192.168.2.70:8000")
        self.mock_repository.update_children.assert_called_once_with(raw_children)                

    @patch("pixelbot_backend.pixelbot_controller.ChildAPI.RemoteDataLoader")
    def test_refresh_from_source_skips_when_robot_unavailable(self, MockRemoteLoader):
        """refresh_from_source does nothing when robot is not reachable."""
        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        with patch.object(api, "is_robot_available", return_value=False):
            api.refresh_from_source()

        MockRemoteLoader.assert_not_called()
        self.mock_repository.update_children.assert_not_called()

    @patch("pixelbot_backend.pixelbot_controller.ChildAPI.RemoteDataLoader")
    def test_refresh_from_source_handles_exception_gracefully(self, MockRemoteLoader):
        """refresh_from_source catches exceptions and does not crash."""
        MockRemoteLoader.return_value.load_all_children.side_effect = Exception("network error")

        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        with patch.object(api, "is_robot_available", return_value=True):
            api.refresh_from_source()  # should not raise

    # --- is_robot_available ---

    @patch("pixelbot_backend.pixelbot_controller.ChildAPI.requests.head")
    def test_is_robot_available_returns_true(self, mock_head):
        mock_head.return_value = MagicMock(status_code=200)
        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        assert api.is_robot_available("http://192.168.2.70:8000") is True

    @patch("pixelbot_backend.pixelbot_controller.ChildAPI.requests.head", side_effect=Exception("timeout"))
    def test_is_robot_available_returns_false_on_error(self, mock_head):
        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        assert api.is_robot_available("http://192.168.2.70:8000") is False

    # --- send_children ---

    def test_send_children_returns_list_of_dicts(self):
        children = [make_child()]
        self.mock_repository.load_children.return_value = children

        api = ChildAPI("http://192.168.2.70:8000", self.mock_repository)
        result = api.send_children()

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert "child_id" in result[0]

# ──────────────────────────────────────────────
# SessionAPI tests
# ──────────────────────────────────────────────

class TestSessionAPI:

    def setup_method(self):
        self.api = SessionAPI()
        self.children = [
            make_child(child_id="child_001", name="Alice", num_sessions=2),
            make_child(child_id="child_002", name="Bob", num_sessions=1),
        ]

    # --- send_session ---

    def test_send_session_returns_correct_session(self):
        """Returns the correct session dict for a valid child_id and session_id."""
        result = self.api.send_session("child_001", "session_0", self.children)

        assert result is not None
        assert result["sessionId"] == "session_0"

    def test_send_session_returns_none_for_wrong_child(self):
        """Returns None when child_id does not exist."""
        result = self.api.send_session("nonexistent_child", "session_0", self.children)
        assert result is None

    def test_send_session_returns_none_for_wrong_session(self):
        """Returns None when session_id does not exist for the given child."""
        result = self.api.send_session("child_001", "session_999", self.children)
        assert result is None

    def test_send_session_returns_dict(self):
        """Returned session is a dictionary (JSON-serializable)."""
        result = self.api.send_session("child_002", "session_0", self.children)
        assert isinstance(result, dict)

    # --- send_all_sessions ---

    def test_send_all_sessions_returns_all_sessions(self):
        """Returns all sessions from all children combined."""
        result = self.api.send_all_sessions(self.children)
        # child_001 has 2 sessions, child_002 has 1 → total 3
        assert len(result) == 3

    def test_send_all_sessions_includes_child_id(self):
        """Each session dict contains a childId field."""
        result = self.api.send_all_sessions(self.children)
        for session in result:
            assert "childId" in session

    def test_send_all_sessions_child_id_matches(self):
        """childId in each session matches the correct parent child."""
        result = self.api.send_all_sessions(self.children)
        child_ids_in_result = {s["childId"] for s in result}
        assert "child_001" in child_ids_in_result
        assert "child_002" in child_ids_in_result

    def test_send_all_sessions_empty_children(self):
        """Returns empty list when no children are given."""
        result = self.api.send_all_sessions([])
        assert result == []

    def test_send_all_sessions_each_item_is_dict(self):
        """Every item in the result is a dictionary."""
        result = self.api.send_all_sessions(self.children)
        for session in result:
            assert isinstance(session, dict)
