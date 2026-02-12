from pixelbot_backend.pixelbot_utils.Utils import Utils   
import datetime
from collections import defaultdict
from collections import Counter
import os

class GlobalMetricsAPI:

    def __init__(self, child_api):
        self.child_api = child_api 
        self.children = self.child_api.load_children_objects()  

    def send_global_metrics_summary(self):
        now = datetime.datetime.now()
        month = now.month
        year = now.year
        sessions = []

        for child in self.children:
            sessions.extend(child.sessions)

        sessions_per_day = Utils.calculate_avg_sessions_per_day(sessions, month, year, now)
        sessions_growth_rate = Utils.calculate_sessions_growth_rate(sessions, month, year)
        sessions_this_month = Utils.count_sessions_this_month(sessions, month, year)
        sessions_per_child_so_far = Utils.calculate_avg_sessions_per_child_so_far(self.children, sessions, now)
        daily_session_counts = self.getDailySessionHeatmap(sessions, year)

        return {
            # total sessions for this month
            "totalSessionsThisMonth": sessions_this_month,
            # sessions per child for this month
            "sessionsPerChild": sessions_per_child_so_far, 
            # sessions per child per day for this month
            "sessionsPerDay": sessions_per_day,    
            # growth rate of sessions compared to last month
            "sessionsGrowthRate": sessions_growth_rate,
            # list of daily session counts for heatmap
            "dailySessionCounts": daily_session_counts
        }
    
    def send_child_recap(self, child_id):
        child = self.child_api.get_child_obj(child_id)
        sessions = child.sessions

        now = datetime.datetime.now()
        year = now.year

        recap = {
            "engagement": {
                # Can be visualised as a box
                "totalSessions": len(sessions),
                # Can be visualised as a line chart. It's a map for every month and the count of sessions taken each month
                "sessionFrequencyTrend": Utils.get_session_frequency_monthly(sessions, year),
                # "sessionStreakWeeks": Utils.get_session_streak(sessions),
            },
            "expressiveness": {
                # It can be written under or above the chart
                "totalWordCount": Utils.get_total_word_count(sessions),
                # red line which shows the average for the bar chart
                "averageWordCount": Utils.avg_word_count(sessions),
                # a map of the word count for every session. Can be visualized as a bbar chart
                "wordCountGrowthRate": Utils.get_avg_word_count_growth_rate(sessions, year),
                # a map of the speech time for every session.
                "speechTimeGrowthRate": Utils.get_speech_time_growth_rate(sessions, year),
            },
            "opennes": {
                # red line which shows the average for the line chart
                "averageIntimacyScore": Utils.get_avg_intimacy_score(sessions),
                # a map for every session and its intimacy value. Can be visualized as a line chart.
                "intimacyTrend": Utils.get_intimacy_trend(sessions, year),
            },
            "drawing": {
                # all these three metrics can be put under the drawing section in the same box
                "averageStrokeCount": Utils.get_avg_stroke_count(sessions),
                "averageNumberColors": Utils.get_avg_colors_used(sessions),
                "averageFilledArea": Utils.get_avg_filled_area(sessions),
            },
            "story": {
                "averageNumberObjects": Utils.get_avg_number_objects(sessions),
                # top 5 objects, ranking
                "mostCommonObjects": self.get_most_common_objects(sessions, 5),
                "objectDiversity": Utils.get_object_diversity(sessions),
            }
        }
        return recap



    def getDailySessionHeatmap(self, sessions, year):
        """
        Converts a list of session objects into:
        { "02-01-2026": count, "03-01-2026": count }
        and formats dates as d-m-y for frontend."""

        date_map = defaultdict(int)
        for session in sessions:
            if session.session_date.year == year:
                session_date = session.session_date.strftime("%d-%m-%Y")
                date_map[session_date] += 1

        start = datetime.date(year, 1, 1)
        end = datetime.date(year, 12, 31)
        delta = datetime.timedelta(days=1)

        current_date = start
        while current_date <= end:
            date_str = current_date.strftime("%d-%m-%Y")
            if date_str not in date_map:
                date_map[date_str] = 0
            current_date += delta        
        return dict(date_map)

    def get_most_common_objects(self, sessions, top_n=5):
        counter = Counter()

        for session in sessions:
            for item in session.story_summary:
                # item is a dict like {"name": "...", "description": "..."}
                name = item.get("name")
                if name:
                    counter[name] += 1

        return counter.most_common(top_n)
    
    def get_recap_data(self, child_id):
        now = datetime.datetime.now()
        month = now.month
        year = now.year

        child = self.child_api.get_child_obj(child_id)
        sessions = child.sessions

        recap = child.get_recap()

        # current month
        sessions_this_month = Utils.count_sessions_this_month(sessions, month, year)
        currentWordCount = self.word_count_for_month(sessions, month, year)
        currentIntimacy = self.avg_intimacy_for_month(sessions, month, year)

        # previous month
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1

        prev_sessions = self.count_sessions_for_month(sessions, prev_month, prev_year)
        prev_word_count = self.word_count_for_month(sessions, prev_month, prev_year)
        prev_intimacy = self.avg_intimacy_for_month(sessions, prev_month, prev_year)
        
        recap["sessionGrowthRate"] = Utils.calculate_difference(sessions_this_month, prev_sessions)
        recap["wordCountGrowthRate"] = Utils.calculate_difference(currentWordCount, prev_word_count)
        recap["intimacyScoreGrowthRate"] = Utils.calculate_growth(currentIntimacy, prev_intimacy)
        
        return recap
    
    def count_sessions_for_month(self, sessions, month, year):
        count_session = 0
        for session in sessions:
            if session.session_date.month == month and session.session_date.year == year:
                count_session += 1

        return count_session
    
    def word_count_for_month(self, sessions, month, year):
        return sum(session.getTotalWordCount() for session in sessions
               if session.session_date.month == month and session.session_date.year == year)
    
    def avg_intimacy_for_month(self, sessions, month, year):
        scores = []
        for session in sessions:
            if session.session_date.month == month and session.session_date.year == year:
                scores.append(session.getAvgIntimacyScore())

        return (float)(sum(scores))

