import datetime
from collections import defaultdict

class Utils:
    JANUARY = 1
    DECEMBER = 12

    @staticmethod
    def calculate_average(values: list):
        if not values:
            return 0.0  
        return sum(values) / len(values) 

    @staticmethod
    def count_sessions_this_month(sessions: list, month: int, year: int):
        total_sessions_this_month = 0

        for session in sessions:
            session_date = session.session_date
            if session_date.month == month and session_date.year == year:
                total_sessions_this_month += 1

        return total_sessions_this_month
    
    @staticmethod
    def get_session_frequency_monthly(sessions: list, year: int):
        monthlyCount = defaultdict(int)

        for session in sessions:
            if session.session_date.year == year:
                month = session.session_date.strftime("%m-%Y")
                monthlyCount[month] += 1
        
        sorted_months = sorted(
        monthlyCount.keys(), key=lambda month: datetime.datetime.strptime(month, "%m-%Y"))

        return [
            {"month": month, "count": monthlyCount[month]}
            for month in sorted_months
        ]        
    
    @staticmethod
    def get_session_streak(self, sessions: list):
        pass

    @staticmethod
    def get_total_word_count(sessions):
        return sum(session.getTotalWordCount() for session in sessions)
    
    @staticmethod
    def get_avg_intervention_count_per_session(sessions):
        return sum(session.getInterventionCount() for session in sessions) / len(sessions)
    
    @staticmethod
    def get_avg_word_count_growth_rate(sessions, this_year):
        word_growth_rate = [
        {
            "sessionId": session.getSessionId(),
            "wordCount": session.getTotalWordCount()
        }
        for session in sessions if session.session_date.year == this_year]
        return word_growth_rate
    
    
    @staticmethod
    def word_count_for_month(sessions, month, year):
        return sum(session.getTotalWordCount() for session in sessions
               if session.session_date.month == month and session.session_date.year == year)
    
    @staticmethod
    def avg_word_count(sessions):
        return sum(session.getTotalWordCount() for session in sessions) / len(sessions)

    @staticmethod
    def get_speech_time_growth_rate(sessions, this_year):
        speech_time_growth_rate = [
        {
            "sessionId": session.getSessionId(),
            "speechTime": session.getTotalSpeechTime()
        }
        for session in sessions if session.session_date.year == this_year]
        return speech_time_growth_rate
    
    @staticmethod
    def speech_time_for_month(sessions, month, year):
        return sum(session.getTotalSpeechTime() for session in sessions
               if session.session_date.month == month and session.session_date.year == year)

    # red line on the chart for intimacy score
    @staticmethod
    def get_avg_intimacy_score(sessions):
        return sum(session.getAvgIntimacyScore() for session in sessions) / len(sessions)

    # bar/line chart for intimacy score
    @staticmethod
    def get_intimacy_trend(sessions, year):

        intimacy_trend = [
        {
            "sessionId": session.getSessionId(),
            "intimacy": session.getAvgIntimacyScore()
        }
        for session in sessions if session.session_date.year == year]

        return intimacy_trend
    
    #Right below the drawing carrousel this metric can be shown
    @staticmethod
    def get_avg_stroke_count(sessions):
        return sum(session.getStrokeCountDrawing() for session in sessions) / len(sessions)
    
    #Right below the drawing carrousel this metric can be shown
    @staticmethod
    def get_avg_filled_area(sessions):
        return sum(session.getFilledAreaDrawing() for session in sessions) / len(sessions)
    
    #Right below the drawing carrousel this metric can be shown
    @staticmethod 
    def get_avg_colors_used(sessions):
        return sum(session.getColorsUsedCountDrawing() for session in sessions) / len(sessions)
    
    @staticmethod
    def get_avg_number_objects(sessions):
        return sum(len(session.story_summary) for session in sessions) / len(sessions)
    
    @staticmethod
    def get_object_diversity(sessions):
        objects = set()
        for session in sessions:
            for item in session.story_summary:
                name = item.get("name")
                if name:
                    objects.add(name)
        return len(objects)


    @staticmethod
    def calculate_avg_sessions_per_day(sessions: list, year: int, now: datetime.datetime):
        # Count sessions in the current year
        sessions_this_year = 0
        for session in sessions:
            if session.getSessionDate().year == year:
                sessions_this_year += 1

        # Days passed this year including today
        start_of_year = datetime.datetime(year, 1, 1)
        days_passed = (now - start_of_year).days + 1  # +1 so Jan 1 counts as 1

        # Compute average
        if days_passed > 0:
            return round (sessions_this_year / days_passed, 1)
        else:
            return 0

    
    @staticmethod
    def calculate_avg_sessions_per_child_so_far(children: list, sessions: list, now: datetime.datetime):
        total_sessions = 0
        for session in sessions:
            # only count sessions up to today considerating the last years.
            if session.session_date <= now: 
                total_sessions += 1

        total_children = len(children)
        return round(total_sessions / total_children, 1) if total_children > 0 else 0
    
    @staticmethod
    def calculate_sessions_growth_rate(sessions: list, month: int, year: int):
        current_month_sessions = Utils.count_sessions_this_month(sessions, month, year)
        previous_month = month - 1 if month > 1 else 12
        previous_year = year if month > 1 else year - 1
        previous_month_sessions = Utils.count_sessions_this_month(sessions, previous_month, previous_year)

        if previous_month_sessions == 0:
            return float('inf') if current_month_sessions > 0 else 0.0  

        growth_rate = (current_month_sessions - previous_month_sessions) / previous_month_sessions * 100
        return round(growth_rate)
    
    @staticmethod
    def calculate_difference(current, previous):
        return (current - previous)
    
    @staticmethod
    def calculate_growth(current, previous):
        if previous == 0:
            return float('inf') if current > 0 else 0
        return ((current - previous) / previous) * 100

        
