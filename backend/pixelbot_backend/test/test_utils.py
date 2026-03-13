"""
test_utils.py
Unit tests for the Utils helper class.
Covers all static methods including edge cases (January roll-over,
empty previous month, zero children, etc.).
"""
import datetime
import pytest

from pixelbot_backend.pixelbot_utils.Utils import Utils


class TestCountSessionsThisMonth:

    def test_counts_matching_session(self, sample_session):
        # sample_session is dated 2026-03-01
        assert Utils.count_sessions_this_month([sample_session], 3, 2026) == 1

    def test_returns_zero_for_wrong_month(self, sample_session):
        assert Utils.count_sessions_this_month([sample_session], 2, 2026) == 0

    def test_returns_zero_for_wrong_year(self, sample_session):
        assert Utils.count_sessions_this_month([sample_session], 3, 2025) == 0

    def test_empty_session_list(self):
        assert Utils.count_sessions_this_month([], 3, 2026) == 0

    def test_multiple_sessions_same_month(self, sample_session, sample_session_2):
        # sample_session → March 2026, sample_session_2 → Feb 2026
        assert Utils.count_sessions_this_month([sample_session, sample_session_2], 3, 2026) == 1
        assert Utils.count_sessions_this_month([sample_session, sample_session_2], 2, 2026) == 1


class TestOrderMapByDate:

    def test_orders_ascending(self):
        entries = [
            {"sessionDate": datetime.datetime(2026, 3, 5), "value": "B"},
            {"sessionDate": datetime.datetime(2026, 1, 1), "value": "A"},
        ]
        result = Utils.order_map_by_date(entries)
        assert result[0]["value"] == "A"
        assert result[1]["value"] == "B"

    def test_single_entry(self):
        entries = [{"sessionDate": datetime.datetime(2026, 1, 1), "value": "only"}]
        assert Utils.order_map_by_date(entries)[0]["value"] == "only"


class TestGetSessionFrequencyMonthly:

    def test_single_session(self, sample_session):
        result = Utils.get_session_frequency_monthly([sample_session], 2026)
        assert len(result) == 1
        assert result[0]["month"] == "03-2026"
        assert result[0]["count"] == 1

    def test_two_sessions_different_months(self, sample_session, sample_session_2):
        result = Utils.get_session_frequency_monthly([sample_session, sample_session_2], 2026)
        months = [r["month"] for r in result]
        assert "02-2026" in months
        assert "03-2026" in months

    def test_filters_by_year(self, sample_session):
        result = Utils.get_session_frequency_monthly([sample_session], 2025)
        assert result == []

    def test_result_is_sorted_chronologically(self, sample_session, sample_session_2):
        result = Utils.get_session_frequency_monthly([sample_session, sample_session_2], 2026)
        assert result[0]["month"] == "02-2026"
        assert result[1]["month"] == "03-2026"


class TestWordCountHelpers:

    def test_get_total_word_count(self, sample_session):
        assert Utils.get_total_word_count([sample_session]) == 120

    def test_avg_word_count(self, sample_session, sample_session_2):
        result = Utils.avg_word_count([sample_session, sample_session_2], 2026)
        assert result == (120 + 80) / 2

    def test_get_avg_word_count_growth_rate_current_year(self, sample_session):
        result = Utils.get_avg_word_count_growth_rate([sample_session], 2026)
        assert len(result) == 1
        assert result[0]["wordCount"] == 120

    def test_get_avg_word_count_growth_rate_filters_year(self, sample_session):
        result = Utils.get_avg_word_count_growth_rate([sample_session], 2025)
        assert result == []


class TestSpeechTimeHelpers:

    def test_get_avg_speech_time(self, sample_session):
        assert Utils.get_avg_speech_time([sample_session], 2026) == 60.0

    def test_get_speech_time_growth_rate(self, sample_session):
        result = Utils.get_speech_time_growth_rate([sample_session], 2026)
        assert len(result) == 1
        assert result[0]["speechTime"] == 60.0

    def test_get_speech_time_growth_rate_filters_year(self, sample_session):
        result = Utils.get_speech_time_growth_rate([sample_session], 2020)
        assert result == []


class TestIntimacyHelpers:

    def test_get_avg_intimacy_score(self, sample_session):
        assert Utils.get_avg_intimacy_score([sample_session], 2026) == 3.5

    def test_get_avg_intimacy_score_multiple(self, sample_session, sample_session_2):
        result = Utils.get_avg_intimacy_score([sample_session, sample_session_2], 2026)
        assert result == (3.5 + 2.0) / 2

    def test_get_intimacy_trend(self, sample_session):
        result = Utils.get_intimacy_trend([sample_session], 2026)
        assert len(result) == 1
        assert result[0]["intimacy"] == 3.5

    def test_get_intimacy_trend_filters_year(self, sample_session):
        result = Utils.get_intimacy_trend([sample_session], 2025)
        assert result == []


class TestDrawingHelpers:

    def test_get_avg_stroke_count(self, sample_session):
        assert Utils.get_avg_stroke_count([sample_session]) == 10.0

    def test_get_avg_filled_area(self, sample_session):
        assert Utils.get_avg_filled_area([sample_session]) == 0.35

    def test_get_avg_colors_used(self, sample_session):
        assert Utils.get_avg_colors_used([sample_session]) == 4.0


class TestStoryHelpers:

    def test_get_avg_number_objects(self, sample_session):
        # sample_session has 1 object in story_summary
        assert Utils.get_avg_number_objects([sample_session]) == 1.0

    def test_get_avg_number_objects_multiple(self, sample_session, sample_session_2):
        # session_1: 1 object, session_2: 2 objects → avg = 1.5
        result = Utils.get_avg_number_objects([sample_session, sample_session_2])
        assert result == 1.5

    def test_get_object_diversity_unique_names(self, sample_session, sample_session_2):
        # session_1 has "cat", session_2 has "house" and "cat" → 2 unique
        result = Utils.get_object_diversity([sample_session, sample_session_2])
        assert result == 2

    def test_get_object_diversity_single_session(self, sample_session):
        assert Utils.get_object_diversity([sample_session]) == 1


class TestSessionRateHelpers:

    def test_calculate_avg_sessions_per_day_normal(self, sample_session):
        now = datetime.datetime(2026, 3, 10)
        result = Utils.calculate_avg_sessions_per_day([sample_session], 2026, now)
        assert result >= 0

    def test_calculate_avg_sessions_per_day_no_sessions_this_year(self, sample_session):
        now = datetime.datetime(2025, 6, 1)
        # sample_session is in 2026, so none match 2025
        result = Utils.calculate_avg_sessions_per_day([sample_session], 2025, now)
        assert result == 0.0

    def test_calculate_avg_sessions_per_child_so_far(self, sample_session, sample_child):
        now = datetime.datetime(2026, 12, 31)
        result = Utils.calculate_avg_sessions_per_child_so_far([sample_child], [sample_session], now)
        assert result == 1.0

    def test_calculate_avg_sessions_per_child_zero_children(self, sample_session):
        now = datetime.datetime(2026, 12, 31)
        result = Utils.calculate_avg_sessions_per_child_so_far([], [sample_session], now)
        assert result == 0

    def test_calculate_sessions_growth_rate_no_previous(self, sample_session):
        # March 2026 has 1 session, February 2026 has 0 → inf
        result = Utils.calculate_sessions_growth_rate([sample_session], 3, 2026)
        assert result == float("inf")

    def test_calculate_sessions_growth_rate_with_previous(self, sample_session, sample_session_2):
        # March: 1, Feb: 1 → 0% growth
        result = Utils.calculate_sessions_growth_rate([sample_session, sample_session_2], 3, 2026)
        assert result == 0

    def test_calculate_sessions_growth_rate_january_rolls_to_december(self, sample_session):
        # January month roll-over: previous month should be December of previous year
        result = Utils.calculate_sessions_growth_rate([sample_session], 1, 2026)
        # sample_session is in March so both Jan 2026 and Dec 2025 have 0 sessions
        assert result == 0.0

    def test_calculate_sessions_growth_rate_positive_growth(self, sample_session, sample_session_2):
        # Add a second March session to get growth from Feb (1) to March (2) → +100%
        from pixelbot_backend.pixelbot_model.Session import Session
        from pixelbot_backend.pixelbot_model.DrawingData import DrawingData
        extra_march = Session(
            session_id="session_3",
            session_date=datetime.datetime(2026, 3, 20),
            drawing=DrawingData(""),
            story_summary=[],
            transcript=[],
            speech_width=sample_session.speech_width,
            speech_depth=sample_session.speech_depth,
            drawing_width=sample_session.drawing_width
        )
        result = Utils.calculate_sessions_growth_rate(
            [sample_session, sample_session_2, extra_march], 3, 2026
        )
        assert result == 100
