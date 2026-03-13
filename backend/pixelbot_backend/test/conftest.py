import pytest
import datetime
from pixelbot_backend.pixelbot_model.Child import Child
from pixelbot_backend.pixelbot_model.Session import Session
from pixelbot_backend.pixelbot_model.DrawingData import DrawingData
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureWidth import SpeechSelfDisclosureWidth
from pixelbot_backend.pixelbot_model.SpeechSelfDisclosureDepth import SpeechSelfDisclosureDepth
from pixelbot_backend.pixelbot_model.DrawingSelfDisclosureWidth import DrawingSelfDisclosureWidth

'''This conftest.py file defines pytest fixtures that create sample data objects for testing the Pixelbot backend.'''

@pytest.fixture
def sample_speech_width():
    return SpeechSelfDisclosureWidth(
        intervention_count=5,
        total_word_count=120,
        average_word_count_per_intervention=24.0,
        std_word_count_per_intervention=3.0,
        total_speech_time=60.0,
        average_speech_time_per_intervention=12.0,
        std_speech_time_per_intervention=2.0
    )


@pytest.fixture
def sample_speech_depth():
    return SpeechSelfDisclosureDepth(
        average_intimacy_score=3.5,
        std_intimacy_score=0.5
    )


@pytest.fixture
def sample_drawing_width():
    return DrawingSelfDisclosureWidth(
        stroke_count=10,
        total_stroke_length=500.0,
        average_stroke_length=50.0,
        std_stroke_length=5.0,
        color_used_count=4,
        pen_size_used_count=2,
        amount_filled_area=0.35
    )


@pytest.fixture
def sample_session(sample_speech_width, sample_speech_depth, sample_drawing_width):
    # session_id must follow the format "session_N" because Child.order_sessions_by_id splits on "_"
    return Session(
        session_id="session_1",
        session_date=datetime.datetime(2026, 3, 1),
        drawing=DrawingData("abc123"),
        story_summary=[{"name": "cat", "description": "a fluffy cat"}],
        transcript=[{"name": "Child", "description": "I drew a cat"}],
        speech_width=sample_speech_width,
        speech_depth=sample_speech_depth,
        drawing_width=sample_drawing_width
    )


@pytest.fixture
def sample_session_2(sample_speech_width, sample_speech_depth, sample_drawing_width):
    """A second session in a different month for growth-rate tests."""
    return Session(
        session_id="session_2",
        session_date=datetime.datetime(2026, 2, 15),
        drawing=DrawingData("xyz789"),
        story_summary=[{"name": "house", "description": "a big house"}, {"name": "cat", "description": "same cat"}],
        transcript=[{"name": "Child", "description": "I drew a house"}],
        speech_width=SpeechSelfDisclosureWidth(
            intervention_count=3,
            total_word_count=80,
            average_word_count_per_intervention=26.0,
            std_word_count_per_intervention=2.0,
            total_speech_time=40.0,
            average_speech_time_per_intervention=13.0,
            std_speech_time_per_intervention=1.5
        ),
        speech_depth=SpeechSelfDisclosureDepth(average_intimacy_score=2.0, std_intimacy_score=0.3),
        drawing_width=sample_drawing_width
    )


@pytest.fixture
def sample_child(sample_session):
    return Child(
        child_id="child_001",
        name="TestChild",
        sessions=[sample_session]
    )


@pytest.fixture
def sample_child_two_sessions(sample_session, sample_session_2):
    return Child(
        child_id="child_002",
        name="TwoSessionChild",
        sessions=[sample_session, sample_session_2]
    )
