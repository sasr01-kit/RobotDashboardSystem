import datetime
import pytest

from pixelbot_backend.pixelbot_controller.GlobalMetricsAPI import GlobalMetricsAPI
from pixelbot_backend.pixelbot_model.Session import Session
from pixelbot_backend.pixelbot_model.DrawingData import DrawingData

"""Unit tests for GlobalMetricsAPI.
    Covers send_global_metrics_summary, send_child_recap, getDailySessionHeatmap, get_most_common_objects, get_heatmap_ranges."""

@pytest.fixture
def api():
    return GlobalMetricsAPI()


# ---------------------------------------------------------------------------
# send_global_metrics_summary
# ---------------------------------------------------------------------------
class TestSendGlobalMetricsSummary:

    def test_returns_all_expected_keys(self, api, sample_child):
        result = api.send_global_metrics_summary([sample_child])
        for key in ["totalSessionsThisMonth", "sessionsPerChild",
                    "sessionsPerDay", "sessionsGrowthRate",
                    "dailySessionCounts", "colorScale"]:
            assert key in result

    def test_color_scale_has_data_classes(self, api, sample_child):
        result = api.send_global_metrics_summary([sample_child])
        assert "dataClasses" in result["colorScale"]

    def test_daily_session_counts_has_365_entries(self, api, sample_child):
        result = api.send_global_metrics_summary([sample_child])
        year = datetime.datetime.now().year
        # A non-leap year has 365 days; a leap year has 366
        days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
        assert len(result["dailySessionCounts"]) == days_in_year

    def test_sessions_per_child_non_negative(self, api, sample_child):
        result = api.send_global_metrics_summary([sample_child])
        assert result["sessionsPerChild"] >= 0

    def test_two_children(self, api, sample_child, sample_child_two_sessions):
        result = api.send_global_metrics_summary([sample_child, sample_child_two_sessions])
        assert result["sessionsPerChild"] >= 0


# ---------------------------------------------------------------------------
# send_child_recap
# ---------------------------------------------------------------------------
class TestSendChildRecap:

    def test_returns_all_top_level_keys(self, api, sample_child):
        result = api.send_child_recap("child_001", [sample_child])
        for key in ["name", "engagement", "expressiveness", "opennes", "drawing", "story"]:
            assert key in result

    def test_engagement_keys(self, api, sample_child):
        result = api.send_child_recap("child_001", [sample_child])
        assert "totalSessions" in result["engagement"]
        assert "sessionFrequencyTrend" in result["engagement"]

    def test_expressiveness_keys(self, api, sample_child):
        result = api.send_child_recap("child_001", [sample_child])
        exp = result["expressiveness"]
        for key in ["totalWordCount", "averageWordCount", "wordCountGrowthRate",
                    "averageSpeechTime", "speechTimeGrowthRate"]:
            assert key in exp

    def test_openness_keys(self, api, sample_child):
        result = api.send_child_recap("child_001", [sample_child])
        assert "averageIntimacyScore" in result["opennes"]
        assert "intimacyTrend" in result["opennes"]

    def test_drawing_keys(self, api, sample_child):
        result = api.send_child_recap("child_001", [sample_child])
        for key in ["drawings", "averageStrokeCount", "averageNumberColors", "averageFilledArea"]:
            assert key in result["drawing"]

    def test_story_keys(self, api, sample_child):
        result = api.send_child_recap("child_001", [sample_child])
        for key in ["averageNumberObjects", "mostCommonObjects", "objectDiversity"]:
            assert key in result["story"]

    def test_total_sessions_count(self, api, sample_child):
        result = api.send_child_recap("child_001", [sample_child])
        assert result["engagement"]["totalSessions"] == 1

    def test_child_name_in_recap(self, api, sample_child):
        result = api.send_child_recap("child_001", [sample_child])
        assert result["name"] == "TestChild"

    def test_raises_value_error_for_unknown_child(self, api, sample_child):
        with pytest.raises(ValueError):
            api.send_child_recap("nonexistent_id", [sample_child])

    def test_two_sessions_total_count(self, api, sample_child_two_sessions):
        result = api.send_child_recap("child_002", [sample_child_two_sessions])
        assert result["engagement"]["totalSessions"] == 2


# ---------------------------------------------------------------------------
# getDailySessionHeatmap
# ---------------------------------------------------------------------------
class TestGetDailySessionHeatmap:

    def test_session_date_is_counted(self, api, sample_session):
        result = api.getDailySessionHeatmap([sample_session], 2026)
        assert result.get("01-03-2026") == 1

    def test_all_days_filled(self, api, sample_session):
        result = api.getDailySessionHeatmap([sample_session], 2026)
        # 2026 is not a leap year → 365 days
        assert len(result) == 365

    def test_days_without_sessions_are_zero(self, api, sample_session):
        result = api.getDailySessionHeatmap([sample_session], 2026)
        assert result.get("02-03-2026") == 0

    def test_session_from_different_year_not_counted(self, api, sample_session):
        result = api.getDailySessionHeatmap([sample_session], 2025)
        assert result.get("01-03-2025") == 0

    def test_multiple_sessions_same_day(self, api, sample_session, sample_session_2,
                                        sample_speech_width, sample_speech_depth, sample_drawing_width):
        # Create a third session on the same day as sample_session
        extra = Session(
            session_id="session_3",
            session_date=datetime.datetime(2026, 3, 1),
            drawing=DrawingData(""),
            story_summary=[],
            transcript=[],
            speech_width=sample_speech_width,
            speech_depth=sample_speech_depth,
            drawing_width=sample_drawing_width
        )
        result = api.getDailySessionHeatmap([sample_session, extra], 2026)
        assert result.get("01-03-2026") == 2


# ---------------------------------------------------------------------------
# get_most_common_objects
# ---------------------------------------------------------------------------
class TestGetMostCommonObjects:

    def test_returns_most_common(self, api, sample_session):
        result = api.get_most_common_objects([sample_session], top_n=5)
        assert result[0][0] == "cat"
        assert result[0][1] == 1

    def test_counts_across_sessions(self, api, sample_session, sample_session_2):
        # "cat" appears in both sessions → count 2; "house" appears once
        result = api.get_most_common_objects([sample_session, sample_session_2], top_n=5)
        result_dict = dict(result)
        assert result_dict["cat"] == 2
        assert result_dict["house"] == 1

    def test_top_n_limits_result(self, api, sample_session, sample_session_2):
        result = api.get_most_common_objects([sample_session, sample_session_2], top_n=1)
        assert len(result) == 1

    def test_empty_sessions(self, api):
        result = api.get_most_common_objects([], top_n=5)
        assert result == []


# ---------------------------------------------------------------------------
# get_heatmap_ranges
# ---------------------------------------------------------------------------
class TestGetHeatmapRanges:

    def test_max_zero_or_one_returns_two_buckets(self, api):
        counts = {"01-01-2026": 1, "02-01-2026": 0}
        result = api.get_heatmap_ranges(counts)
        assert len(result) == 2

    def test_max_zero_returns_two_buckets(self, api):
        counts = {"01-01-2026": 0}
        result = api.get_heatmap_ranges(counts)
        assert len(result) == 2

    def test_normal_max_returns_five_buckets(self, api):
        counts = {"01-01-2026": 8, "02-01-2026": 4, "03-01-2026": 2}
        result = api.get_heatmap_ranges(counts)
        assert len(result) == 5

    def test_first_bucket_always_zero_to_zero(self, api):
        counts = {"01-01-2026": 10}
        result = api.get_heatmap_ranges(counts)
        assert result[0] == {"from": 0, "to": 0}

    def test_buckets_are_non_overlapping(self, api):
        counts = {"01-01-2026": 20, "02-01-2026": 5}
        result = api.get_heatmap_ranges(counts)
        # Each bucket's "from" should be previous "to" + 1 (except the first)
        for i in range(1, len(result) - 1):
            assert result[i + 1]["from"] == result[i]["to"] + 1


# ---------------------------------------------------------------------------
# get_child_obj (helper)
# ---------------------------------------------------------------------------
class TestGetChildObj:

    def test_finds_existing_child(self, api, sample_child):
        result = api.get_child_obj("child_001", [sample_child])
        assert result is sample_child

    def test_returns_none_for_missing_child(self, api, sample_child):
        result = api.get_child_obj("does_not_exist", [sample_child])
        assert result is None
