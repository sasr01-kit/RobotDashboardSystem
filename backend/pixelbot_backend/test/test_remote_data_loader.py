"""
test_data_loader.py
Unit tests for RemoteDataLoader and DataRepository.

RemoteDataLoader tests use unittest.mock to intercept all HTTP requests
(requests.get / requests.head) so no real robot connection is needed.

DataRepository tests redirect file paths into tmp_path so the real
children_data.json is never touched.
"""
import io
import csv
import json
import datetime
import pytest
from unittest.mock import patch, MagicMock

from pixelbot_backend.pixelbot_storage.RemoteDataLoader import RemoteDataLoader
from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository
from pixelbot_backend.pixelbot_model.Child import Child


BASE_URL = "http://192.168.2.70:8000"

"""Unit tests for RemoteDataLoader and DataRepository. 
    RemoteDataLoader tests use unittest.mock to intercept all HTTP requests (requests.get / requests.head) so no real robot connection is needed. 
    DataRepository tests redirect file paths into tmp_path so the real children_data.json is never touched."""
# ---------------------------------------------------------------------------
# Helpers – build fake HTTP responses
# ---------------------------------------------------------------------------

def make_response(status_code=200, json_data=None, text=""):
    """Return a MagicMock that behaves like a requests.Response."""
    mock = MagicMock()
    mock.status_code = status_code
    mock.text = text
    mock.json.return_value = json_data or {}
    return mock


def make_csv_text(headers: list, row: list) -> str:
    """Build a CSV string from a header list and a single data row."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(headers)
    writer.writerow(row)
    return buf.getvalue()


# Reusable CSV payloads
SPEECH_WIDTH_CSV = make_csv_text(
    ["intervention_count", "total_word_count",
     "average_word_count_per_intervention", "std_word_count_per_intervention",
     "total_speech_time", "average_speech_time_per_intervention",
     "std_speech_time_per_intervention"],
    ["3", "50", "16.7", "2.1", "30.0", "10.0", "1.5"]
)

SPEECH_DEPTH_CSV = make_csv_text(
    ["average_intimacy_score", "std_intimacy_score"],
    ["2.5", "0.3"]
)

DRAWING_WIDTH_CSV = make_csv_text(
    ["stroke_count", "total_stroke_length", "average_stroke_length",
     "std_stroke_length", "color_used_count", "pen_size_used_count",
     "amount_filled_area"],
    ["8", "400.0", "50.0", "4.0", "3", "2", "0.28"]
)

TRANSCRIPT_TEXT = "Child: I drew a house\nRobot: That looks great!"
STORY_SUMMARY_TEXT = json.dumps({"house": "a big red house", "tree": "a tall green tree"})
DRAWING_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQ=="


def side_effect_full_session(url, **kwargs):
    """
    Single side_effect that returns the correct mock response
    for every URL a full load_session call makes.
    """
    if url.endswith("/children"):
        return make_response(json_data={"children": ["Alice"]})
    if url.endswith("/sessions"):
        return make_response(json_data={"sessions": ["session_1"]})
    if "/file/" in url and url.endswith("/session_1"):
        return make_response(json_data={"files": ["drawing_01-03-2026.png"]})
    if url.endswith("drawing_01-03-2026.png"):
        return make_response(json_data={"base64": DRAWING_B64})
    if url.endswith("transcript.txt"):
        return make_response(text=TRANSCRIPT_TEXT)
    if url.endswith("drawing_description.txt"):
        return make_response(text=STORY_SUMMARY_TEXT)
    if url.endswith("speech_self_disclosure_width_data.csv"):
        return make_response(text=SPEECH_WIDTH_CSV)
    if url.endswith("speech_self_disclosure_depth_data.csv"):
        return make_response(text=SPEECH_DEPTH_CSV)
    if url.endswith("drawing_self_disclosure_width_data.csv"):
        return make_response(text=DRAWING_WIDTH_CSV)
    return make_response(status_code=404)


# ---------------------------------------------------------------------------
# RemoteDataLoader – constructor
# ---------------------------------------------------------------------------
class TestRemoteDataLoaderInit:

    def test_trailing_slash_is_removed(self):
        loader = RemoteDataLoader("http://192.168.2.70:8000/")
        assert not loader.pixelbot_url.endswith("/")

    def test_url_without_slash_unchanged(self):
        loader = RemoteDataLoader(BASE_URL)
        assert loader.pixelbot_url == BASE_URL


# ---------------------------------------------------------------------------
# RemoteDataLoader – get_file_url
# ---------------------------------------------------------------------------
class TestGetFileUrl:

    def test_builds_correct_url(self):
        loader = RemoteDataLoader(BASE_URL)
        url = loader.get_file_url("Alice", "session_1", "transcript.txt")
        assert url == f"{BASE_URL}/file/Alice/session_1/transcript.txt"

    def test_no_double_slash(self):
        loader = RemoteDataLoader(BASE_URL)
        url = loader.get_file_url("Alice", "session_1", "drawing.png")
        assert "//" not in url.replace("http://", "")


# ---------------------------------------------------------------------------
# RemoteDataLoader – extract_day_from_file_url
# ---------------------------------------------------------------------------
class TestExtractDayFromFileUrl:

    def test_extracts_valid_date(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.extract_day_from_file_url(
            f"{BASE_URL}/file/Alice/session_1/drawing_01-03-2026.png"
        )
        assert result == datetime.datetime(2026, 3, 1)

    def test_returns_none_when_no_date_in_url(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.extract_day_from_file_url(
            f"{BASE_URL}/file/Alice/session_1/nodatehere.png"
        )
        assert result is None

    def test_different_valid_date(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.extract_day_from_file_url(
            f"{BASE_URL}/file/Bob/session_2/drawing_15-02-2025.png"
        )
        assert result == datetime.datetime(2025, 2, 15)


# ---------------------------------------------------------------------------
# RemoteDataLoader – parse_transcript
# ---------------------------------------------------------------------------
class TestParseTranscript:

    def test_two_lines_parsed(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.parse_transcript("Child: Hello\nRobot: Hi there")
        assert len(result) == 2

    def test_keys_are_name_and_description(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.parse_transcript("Child: Hello")
        assert "name" in result[0] and "description" in result[0]

    def test_speaker_and_message_split_correctly(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.parse_transcript("Child: I drew a cat")
        assert result[0]["name"] == "Child"
        assert result[0]["description"] == "I drew a cat"

    def test_line_without_colon_is_skipped(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.parse_transcript("no colon here\nChild: hello")
        assert len(result) == 1

    def test_empty_string_returns_empty_list(self):
        loader = RemoteDataLoader(BASE_URL)
        assert loader.parse_transcript("") == []

    def test_message_with_colon_inside_is_preserved(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.parse_transcript("Child: time is 12:30")
        assert result[0]["description"] == "time is 12:30"


# ---------------------------------------------------------------------------
# RemoteDataLoader – parse_story_summary
# ---------------------------------------------------------------------------
class TestParseStorySummary:

    def test_valid_json_parsed(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.parse_story_summary('{"cat": "a cat", "dog": "a dog"}')
        assert len(result) == 2

    def test_returns_name_and_description_keys(self):
        loader = RemoteDataLoader(BASE_URL)
        result = loader.parse_story_summary('{"cat": "fluffy"}')
        assert result[0]["name"] == "cat"
        assert result[0]["description"] == "fluffy"

    def test_invalid_json_returns_empty_list(self):
        loader = RemoteDataLoader(BASE_URL)
        assert loader.parse_story_summary("not valid json") == []

    def test_empty_string_returns_empty_list(self):
        loader = RemoteDataLoader(BASE_URL)
        assert loader.parse_story_summary("") == []

    def test_empty_json_object_returns_empty_list(self):
        loader = RemoteDataLoader(BASE_URL)
        assert loader.parse_story_summary("{}") == []


# ---------------------------------------------------------------------------
# RemoteDataLoader – load_csv
# ---------------------------------------------------------------------------
class TestLoadCsv:

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_returns_dict_on_200(self, mock_get):
        mock_get.return_value = make_response(status_code=200, text=SPEECH_DEPTH_CSV)
        loader = RemoteDataLoader(BASE_URL)
        result = loader.load_csv(f"{BASE_URL}/file/Alice/session_1/speech_self_disclosure_depth_data.csv")
        assert result["average_intimacy_score"] == "2.5"

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_returns_empty_dict_on_404(self, mock_get):
        mock_get.return_value = make_response(status_code=404)
        loader = RemoteDataLoader(BASE_URL)
        result = loader.load_csv(f"{BASE_URL}/file/missing.csv")
        assert result == {}

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_all_speech_width_keys_present(self, mock_get):
        mock_get.return_value = make_response(status_code=200, text=SPEECH_WIDTH_CSV)
        loader = RemoteDataLoader(BASE_URL)
        result = loader.load_csv(f"{BASE_URL}/file/Alice/session_1/speech_self_disclosure_width_data.csv")
        for key in ["intervention_count", "total_word_count", "total_speech_time"]:
            assert key in result


# ---------------------------------------------------------------------------
# RemoteDataLoader – load_txt
# ---------------------------------------------------------------------------
class TestLoadTxt:

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_returns_text_on_200(self, mock_get):
        mock_get.return_value = make_response(status_code=200, text=TRANSCRIPT_TEXT)
        loader = RemoteDataLoader(BASE_URL)
        result = loader.load_txt("Alice", "session_1", "transcript.txt")
        assert result == TRANSCRIPT_TEXT

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_returns_empty_string_on_404(self, mock_get):
        mock_get.return_value = make_response(status_code=404)
        loader = RemoteDataLoader(BASE_URL)
        result = loader.load_txt("Alice", "session_1", "missing.txt")
        assert result == ""


# ---------------------------------------------------------------------------
# RemoteDataLoader – get_drawing_file
# ---------------------------------------------------------------------------
class TestGetDrawingFile:

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_returns_png_url(self, mock_get):
        mock_get.return_value = make_response(
            status_code=200,
            json_data={"files": ["drawing_01-03-2026.png", "transcript.txt"]}
        )
        loader = RemoteDataLoader(BASE_URL)
        result = loader.get_drawing_file("Alice", "session_1")
        assert result.endswith("drawing_01-03-2026.png")

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_returns_none_when_no_png(self, mock_get):
        mock_get.return_value = make_response(
            status_code=200,
            json_data={"files": ["transcript.txt"]}
        )
        loader = RemoteDataLoader(BASE_URL)
        result = loader.get_drawing_file("Alice", "session_1")
        assert result is None

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_returns_none_on_404(self, mock_get):
        mock_get.return_value = make_response(status_code=404)
        loader = RemoteDataLoader(BASE_URL)
        result = loader.get_drawing_file("Alice", "session_1")
        assert result is None


# ---------------------------------------------------------------------------
# RemoteDataLoader – load_child
# ---------------------------------------------------------------------------
class TestLoadChild:

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_returns_child_object(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        child = loader.load_child("Alice")
        assert child.name == "Alice"

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_child_id_is_none(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        child = loader.load_child("Alice")
        assert child.child_id is None

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_child_has_one_session(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        child = loader.load_child("Alice")
        assert len(child.sessions) == 1


# ---------------------------------------------------------------------------
# RemoteDataLoader – load_session
# ---------------------------------------------------------------------------
class TestLoadSession:

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_session_id_is_set(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        session = loader.load_session("Alice", "session_1")
        assert session.session_id == "session_1"

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_session_date_parsed(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        session = loader.load_session("Alice", "session_1")
        assert session.session_date == datetime.datetime(2026, 3, 1)

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_drawing_base64_loaded(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        session = loader.load_session("Alice", "session_1")
        assert session.drawing.base64 == DRAWING_B64

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_transcript_parsed(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        session = loader.load_session("Alice", "session_1")
        assert len(session.transcript) == 2

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_story_summary_parsed(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        session = loader.load_session("Alice", "session_1")
        names = {item["name"] for item in session.story_summary}
        assert "house" in names and "tree" in names

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_total_word_count(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        session = loader.load_session("Alice", "session_1")
        assert session.get_total_word_count() == 50

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_intimacy_score(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        session = loader.load_session("Alice", "session_1")
        assert session.get_avg_intimacy_score() == pytest.approx(2.5)

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_stroke_count(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        session = loader.load_session("Alice", "session_1")
        assert session.get_stroke_count_drawing() == 8

    # Test load sessions with missing CSV files to ensure defaults are used and no exceptions are raised

    def setup_method(self):
        self.api = RemoteDataLoader("http://192.168.2.70:8000")

    def test_uses_default_speech_width_when_csv_missing(self):
        with patch.object(self.api, "load_csv", return_value={}):
            with patch.object(self.api, "get_drawing_file", return_value=None):
                with patch.object(self.api, "extract_day_from_file_url", return_value=None):
                    with patch.object(self.api, "load_txt", return_value=""):
                        session = self.api.load_session("child_1", "session_0")
                        assert session.speech_width.get_total_word_count() == 0

    def test_uses_default_speech_depth_when_csv_missing(self):
        with patch.object(self.api, "load_csv", return_value={}):
            with patch.object(self.api, "get_drawing_file", return_value=None):
                with patch.object(self.api, "extract_day_from_file_url", return_value=None):
                    with patch.object(self.api, "load_txt", return_value=""):
                        session = self.api.load_session("child_1", "session_0")
                        assert session.speech_depth.get_avg_intimacy_score() == 0.0

    def test_uses_default_drawing_width_when_csv_missing(self):
        with patch.object(self.api, "load_csv", return_value={}):
            with patch.object(self.api, "get_drawing_file", return_value=None):
                with patch.object(self.api, "extract_day_from_file_url", return_value=None):
                    with patch.object(self.api, "load_txt", return_value=""):
                        session = self.api.load_session("child_1", "session_0")
                        assert session.drawing_width.get_stroke_count() == 0

    def test_uses_empty_drawing_when_request_fails(self):
        """Falls back to empty DrawingData when drawing request fails."""
        with patch.object(self.api, "load_csv", return_value={}):
            with patch.object(self.api, "get_drawing_file", return_value="http://bad-url"):
                with patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get",
                           side_effect=Exception("network error")):
                    with patch.object(self.api, "load_txt", return_value=""):
                        session = self.api.load_session("child_1", "session_0")
                        assert session.drawing.base64 == ""


# ---------------------------------------------------------------------------
# RemoteDataLoader – load_all_children
# ---------------------------------------------------------------------------
class TestLoadAllChildren:

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_returns_one_child(self, mock_get):
        mock_get.side_effect = side_effect_full_session
        loader = RemoteDataLoader(BASE_URL)
        children = loader.load_all_children()
        assert len(children) == 1
        assert children[0].name == "Alice"

    @patch("pixelbot_backend.pixelbot_storage.RemoteDataLoader.requests.get")
    def test_two_children_returned(self, mock_get):
        def two_children_side_effect(url, **kwargs):
            if url.endswith("/children"):
                return make_response(json_data={"children": ["Alice", "Bob"]})
            return side_effect_full_session(url, **kwargs)

        mock_get.side_effect = two_children_side_effect
        loader = RemoteDataLoader(BASE_URL)
        children = loader.load_all_children()
        assert len(children) == 2


# ---------------------------------------------------------------------------
# DataRepository tests
# ---------------------------------------------------------------------------
class TestDataRepository:

    @pytest.fixture
    def repo(self, tmp_path, monkeypatch):
        """DataRepository whose JSON files land in tmp_path."""
        r = DataRepository()
        monkeypatch.setattr(r, "DATA_FILE", str(tmp_path / "children_data.json"))
        monkeypatch.setattr(r, "META_FILE", str(tmp_path / "children_meta.json"))
        return r

    def test_load_children_returns_empty_when_no_file(self, repo):
        assert repo.load_children() == []

    def test_save_and_load_roundtrip(self, repo, sample_child):
        repo.save_children([sample_child])
        loaded = repo.load_children()
        assert len(loaded) == 1
        assert loaded[0].child_id == "child_001"
        assert loaded[0].name == "TestChild"

    def test_save_preserves_session_count(self, repo, sample_child):
        repo.save_children([sample_child])
        assert len(repo.load_children()[0].sessions) == 1

    def test_save_creates_data_file(self, repo, sample_child):
        import os
        repo.save_children([sample_child])
        assert os.path.exists(repo.DATA_FILE)

    def test_save_creates_meta_file(self, repo, sample_child):
        import os
        repo.save_children([sample_child])
        assert os.path.exists(repo.META_FILE)

    def test_get_last_updated_none_when_no_meta_file(self, repo):
        assert repo.get_last_updated() is None

    def test_get_last_updated_none_for_missing_key(self, repo, tmp_path, monkeypatch):
        meta_path = tmp_path / "children_meta.json"
        meta_path.write_text("{}")
        monkeypatch.setattr(repo, "META_FILE", str(meta_path))
        assert repo.get_last_updated() is None

    def test_update_assigns_new_id_when_none(self, repo, sample_child):
        sample_child.child_id = None
        updated = repo.update_children([sample_child])
        assert updated[0].child_id is not None

    def test_update_reuses_existing_id(self, repo, sample_child):
        repo.save_children([sample_child])
        original_id = sample_child.child_id
        fresh = Child(child_id=None, name="TestChild", sessions=sample_child.sessions)
        updated = repo.update_children([fresh])
        assert updated[0].child_id == original_id

    def test_update_returns_correct_count(self, repo, sample_child):
        assert len(repo.update_children([sample_child])) == 1

    def test_update_saves_to_disk(self, repo, sample_child):
        import os
        repo.update_children([sample_child])
        assert os.path.exists(repo.DATA_FILE)
