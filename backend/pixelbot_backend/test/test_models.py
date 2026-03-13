import datetime


from pixelbot_backend.pixelbot_model.DrawingData import DrawingData
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureWidth import SpeechSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureDepth import SpeechSelfDisclosureDepth
from pixelbot_backend.pixelbot_model.DrawingSelfDisclosureWidth import DrawingSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.Session import Session
from pixelbot_backend.pixelbot_model.Child import Child

"""
Unit tests for all model classes: DrawingData, SpeechSelfDisclosureWidth, SpeechSelfDisclosureDepth, DrawingSelfDisclosureWidth, Session and Child
"""
# ---------------------------------------------------------------------------
# DrawingData
# ---------------------------------------------------------------------------
class TestDrawingData:

    def test_to_dict_adds_prefix(self):
        drawing = DrawingData("abc123")
        assert drawing.to_dict() == ["data:image/png;base64,abc123"]

    def test_from_dict_strips_prefix(self):
        drawing = DrawingData.from_dict(["data:image/png;base64,abc123"])
        assert drawing.base64 == "abc123"

    def test_from_dict_empty_list_gives_empty_base64(self):
        drawing = DrawingData.from_dict([])
        assert drawing.base64 == ""

    def test_roundtrip(self):
        original = DrawingData("mydata")
        restored = DrawingData.from_dict(original.to_dict())
        assert restored.base64 == "mydata"


# ---------------------------------------------------------------------------
# SpeechSelfDisclosureWidth
# ---------------------------------------------------------------------------
class TestSpeechSelfDisclosureWidth:

    def test_getters(self, sample_speech_width):
        assert sample_speech_width.get_intervention_count() == 5
        assert sample_speech_width.get_total_word_count() == 120
        assert sample_speech_width.get_avg_word_count_per_intervention() == 24.0
        assert sample_speech_width.get_std_word_count_per_intervention() == 3.0
        assert sample_speech_width.get_total_speech_time() == 60.0
        assert sample_speech_width.get_avg_speech_time_per_intervention() == 12.0
        assert sample_speech_width.get_std_speech_time_per_intervention() == 2.0

    def test_to_dict_has_all_keys(self, sample_speech_width):
        d = sample_speech_width.to_dict()
        expected_keys = [
            "intervention_count", "total_word_count",
            "average_word_count_per_intervention", "std_word_count_per_intervention",
            "total_speech_time", "average_speech_time_per_intervention",
            "std_speech_time_per_intervention"
        ]
        for key in expected_keys:
            assert key in d

    def test_from_dict_roundtrip(self, sample_speech_width):
        d = sample_speech_width.to_dict()
        restored = SpeechSelfDisclosureWidth.from_dict(d)
        assert restored.total_word_count == 120
        assert restored.intervention_count == 5


# ---------------------------------------------------------------------------
# SpeechSelfDisclosureDepth
# ---------------------------------------------------------------------------
class TestSpeechSelfDisclosureDepth:

    def test_getters(self, sample_speech_depth):
        assert sample_speech_depth.get_avg_intimacy_score() == 3.5
        assert sample_speech_depth.get_std_intimacy_score() == 0.5

    def test_to_dict(self, sample_speech_depth):
        d = sample_speech_depth.to_dict()
        assert d["average_intimacy_score"] == 3.5
        assert d["std_intimacy_score"] == 0.5

    def test_from_dict_roundtrip(self, sample_speech_depth):
        restored = SpeechSelfDisclosureDepth.from_dict(sample_speech_depth.to_dict())
        assert restored.average_intimacy_score == 3.5


# ---------------------------------------------------------------------------
# DrawingSelfDisclosureWidth
# ---------------------------------------------------------------------------
class TestDrawingSelfDisclosureWidth:

    def test_getters(self, sample_drawing_width):
        assert sample_drawing_width.get_stroke_count() == 10
        assert sample_drawing_width.get_total_stroke_length() == 500.0
        assert sample_drawing_width.get_avg_stroke_length() == 50.0
        assert sample_drawing_width.get_std_stroke_length() == 5.0
        assert sample_drawing_width.get_color_used_count() == 4
        assert sample_drawing_width.get_pen_size_used_count() == 2
        assert sample_drawing_width.get_amount_filled_area() == 0.35

    def test_to_dict_has_all_keys(self, sample_drawing_width):
        d = sample_drawing_width.to_dict()
        for key in ["stroke_count", "total_stroke_length", "average_stroke_length",
                    "std_stroke_length", "color_used_count", "pen_size_used_count", "amount_filled_area"]:
            assert key in d

    def test_from_dict_roundtrip(self, sample_drawing_width):
        restored = DrawingSelfDisclosureWidth.from_dict(sample_drawing_width.to_dict())
        assert restored.stroke_count == 10
        assert restored.amount_filled_area == 0.35


# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------
class TestSession:

    def test_to_dict_contains_required_keys(self, sample_session):
        d = sample_session.to_dict()
        for key in ["sessionId", "sessionDate", "drawing", "storySummary",
                    "transcript", "speechWidth", "speechDepth", "drawingWidth"]:
            assert key in d

    def test_to_dict_date_format(self, sample_session):
        d = sample_session.to_dict()
        assert d["sessionDate"] == "01-03-2026"

    def test_from_dict_roundtrip(self, sample_session):
        d = sample_session.to_dict()
        restored = Session.from_dict(d)
        assert restored.session_id == "session_1"
        assert restored.session_date == datetime.datetime(2026, 3, 1)
        assert restored.get_total_word_count() == 120

    def test_get_total_word_count(self, sample_session):
        assert sample_session.get_total_word_count() == 120

    def test_get_avg_intimacy_score(self, sample_session):
        assert sample_session.get_avg_intimacy_score() == 3.5

    def test_get_total_speech_time(self, sample_session):
        assert sample_session.get_total_speech_time() == 60.0

    def test_get_stroke_count_drawing(self, sample_session):
        assert sample_session.get_stroke_count_drawing() == 10

    def test_get_colors_used_count_drawing(self, sample_session):
        assert sample_session.get_colors_used_count_drawing() == 4

    def test_get_filled_area_drawing(self, sample_session):
        assert sample_session.get_filled_area_drawing() == 0.35

    def test_getters(self, sample_session):
        assert sample_session.get_session_id() == "session_1"
        assert sample_session.get_session_date() == datetime.datetime(2026, 3, 1)
        assert sample_session.get_story_summary() == [{"name": "cat", "description": "a fluffy cat"}]
        assert len(sample_session.get_transcript()) == 1

    def test_get_drawing_is_drawing_data(self, sample_session):
        assert isinstance(sample_session.get_drawing(), DrawingData)

    def test_get_speech_and_drawing_width_objects(self, sample_session):
        assert isinstance(sample_session.get_speech_width(), SpeechSelfDisclosureWidth)
        assert isinstance(sample_session.get_speech_depth(), SpeechSelfDisclosureDepth)
        assert isinstance(sample_session.get_drawing_width(), DrawingSelfDisclosureWidth)


# ---------------------------------------------------------------------------
# Child
# ---------------------------------------------------------------------------
class TestChild:

    def test_to_dict_has_required_keys(self, sample_child):
        d = sample_child.to_dict()
        assert d["child_id"] == "child_001"
        assert d["name"] == "TestChild"
        assert len(d["sessions"]) == 1

    def test_get_id(self, sample_child):
        assert sample_child.get_id() == "child_001"

    def test_get_name(self, sample_child):
        assert sample_child.get_name() == "TestChild"

    def test_get_sessions(self, sample_child):
        assert len(sample_child.get_sessions()) == 1

    def test_get_drawings_returns_drawing_objects(self, sample_child):
        drawings = sample_child.get_drawings()
        assert len(drawings) == 1
        assert isinstance(drawings[0], DrawingData)

    def test_get_session_by_id_found(self, sample_child, sample_session):
        result = sample_child.get_session_by_id("session_1")
        assert result is sample_session

    def test_get_session_by_id_not_found(self, sample_child):
        assert sample_child.get_session_by_id("nonexistent") is None

    def test_get_session_ids(self, sample_child):
        assert sample_child.get_session_ids() == ["session_1"]

    def test_get_number_of_sessions(self, sample_child):
        assert sample_child.get_number_of_sessions() == 1

    def test_get_total_word_count(self, sample_child):
        assert sample_child.get_total_word_count() == 120

    def test_get_avg_intimacy_score(self, sample_child):
        assert sample_child.get_avg_intimacy_score() == 3.5

    def test_sessions_are_ordered_by_id(self, sample_child_two_sessions):
        ids = sample_child_two_sessions.get_session_ids()
        # session_1 should come before session_2
        assert ids == ["session_1", "session_2"]

    def test_from_dict_roundtrip(self, sample_child):
        d = sample_child.to_dict()
        restored = Child.from_dict(d)
        assert restored.child_id == "child_001"
        assert restored.name == "TestChild"
        assert len(restored.sessions) == 1
