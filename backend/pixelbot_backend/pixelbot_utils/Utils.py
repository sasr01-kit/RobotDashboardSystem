import datetime
from collections import defaultdict

''' Utility functions for processing session data, calculating metrics, and growth rates. '''
class Utils:
    
    '''' Order a list of session dictionaries by their session date. Assumes each dictionary has a "sessionDate" key with a datetime value. '''
    @staticmethod
    def order_map_by_date(session_map):
        # session_map is {sessionId: Session}
        return sorted(session_map, key=lambda x: x["sessionDate"])

    ''' Calculate the growth rate of the total sessions per month. Used for the line chart Total Sessions in recap.'''
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

    ''' Calculate the total word count accros all sessions.'''
    @staticmethod
    def get_total_word_count(sessions):
        return sum(session.get_total_word_count() for session in sessions)
    
    ''' Calculate the total word count for each month. Used for the bar chart Word Count in recap. Only data for this year is considered,
        but can be easily adapted to show data for previous years as well.'''
    @staticmethod
    def get_avg_word_count_growth_rate(sessions, this_year):
        word_growth_rate = [
        {
            "sessionId": session.get_session_id(),
            "sessionDate": session.session_date,
            "wordCount": session.get_total_word_count()
        }
        # Only consider sessions from this year, since we want to show the trend for the current year in the recap.
        for session in sessions if session.session_date.year == this_year]

        ordered_list_word_growth_rate = Utils.order_map_by_date(word_growth_rate)

        return ordered_list_word_growth_rate
    
    ''' Calculate the average word count for all the sessions. Used for the average line in Word Count in recap.
        Only data for this year is considered.'''
    @staticmethod
    def avg_word_count(sessions, this_year):
        return sum(session.get_total_word_count() for session in sessions if session.session_date.year == this_year) / len(sessions)

    ''' Calculate the growth rate of the total speech time for each month. Used for the line chart Speech Time in recap. 
        Only data for this year is considered.'''
    @staticmethod
    def get_speech_time_growth_rate(sessions, this_year):
        speech_time_growth_rate = [
        {
            "sessionId": session.get_session_id(),
            "sessionDate": session.session_date,
            "speechTime": session.get_total_speech_time()
        }
        for session in sessions if session.session_date.year == this_year]

        ordered_list_speech_time_growth_rate = Utils.order_map_by_date(speech_time_growth_rate)

        return ordered_list_speech_time_growth_rate
    
    ''' Calculate the average speech time for all the sessions. Used for the average line in Speech Time in recap.'''
    @staticmethod
    def get_avg_speech_time(sessions, this_year):
        return sum(session.get_total_speech_time() for session in sessions if session.session_date.year == this_year) / len(sessions)

    ''' Calculate the average intimacy score across all sessions. Used for the average line in Intimacy Score in recap.'''
    @staticmethod
    def get_avg_intimacy_score(sessions, this_year):
        return sum(session.get_avg_intimacy_score() for session in sessions if session.session_date.year == this_year) / len(sessions)

    ''' Calculate the intimacy score for each session. Used for the line chart Intimacy Score in recap. 
        Only data for this year is considered.'''
    @staticmethod
    def get_intimacy_trend(sessions, year):

        intimacy_trend = [
        {
            "sessionId": session.get_session_id(),
            "sessionDate": session.session_date,
            "intimacy": session.get_avg_intimacy_score()
        }
        for session in sessions if session.session_date.year == year]

        ordered_list_intimacy_trend = Utils.order_map_by_date(intimacy_trend)

        return ordered_list_intimacy_trend
    
    '''Calculate the average stroke count. Used below the drawing carrousel in the recap page.'''
    @staticmethod
    def get_avg_stroke_count(sessions):
        return sum(session.get_stroke_count_drawing() for session in sessions) / len(sessions)
    
    '''Calculate the average filled area. Used below the drawing carrousel in the recap page.'''
    @staticmethod
    def get_avg_filled_area(sessions):
        return sum(session.get_filled_area_drawing() for session in sessions) / len(sessions)
    
    '''Calculate the average number of colors used in the drawings. Used below the drawing carrousel in the recap page.'''
    @staticmethod 
    def get_avg_colors_used(sessions):
        return sum(session.get_colors_used_count_drawing() for session in sessions) / len(sessions)
    
    '''Calculate the average number of objects in the story. Used for the story metrics in recap page'''
    @staticmethod
    def get_avg_number_objects(sessions):
        return sum(len(session.get_story_summary()) for session in sessions) / len(sessions)
    
    '''Calculate the object diversity in the story. Used for the story metrics in recap page'''
    @staticmethod
    def get_object_diversity(sessions):
        objects = set()
        for session in sessions:
            for item in session.get_story_summary():
                name = item.get("name")
                if name:
                    objects.add(name)
        return len(objects)

    '''Calculate the average number of sessions per day for the current year. Used for the heatmap in the summary page.'''
    @staticmethod
    def calculate_avg_sessions_per_day(sessions: list, year: int, now: datetime.datetime):
        # Count sessions in the current year
        sessions_this_year = 0
        for session in sessions:
            if session.get_session_date().year == year:
                sessions_this_year += 1

        # Days passed this year including today
        start_of_year = datetime.datetime(year, 1, 1)
        days_passed = (now - start_of_year).days + 1  # +1 so Jan 1 counts as 1

        # Compute average
        if days_passed > 0:
            return round (sessions_this_year / days_passed, 1)
        else:
            return 0
        
    ''' Count the number of sessions that occurred in a specific month and year. Used for the summary page. '''
    @staticmethod
    def count_sessions_this_month(sessions: list, month: int, year: int):
        total_sessions_this_month = 0

        for session in sessions:
            session_date = session.session_date
            if session_date.month == month and session_date.year == year:
                total_sessions_this_month += 1

        return total_sessions_this_month    

    '''Calculate the average sessions per child so far for the current year. Used for the summary page'''
    @staticmethod
    def calculate_avg_sessions_per_child_so_far(children: list, sessions: list, now: datetime.datetime):
        total_sessions = 0
        for session in sessions:
            # only count sessions up to today considerating the last years.
            if session.get_session_date() <= now: 
                total_sessions += 1

        total_children = len(children)
        return round(total_sessions / total_children, 1) if total_children > 0 else 0
    
    '''Calculate the difference in sessions count between this month and the previous month. Used for the summary page'''
    @staticmethod
    def calculate_sessions_growth_rate(sessions: list, month: int, year: int):
        JANUARY = 1
        DECEMBER = 12

        current_month_sessions = Utils.count_sessions_this_month(sessions, month, year)
        previous_month = month - 1 if month > JANUARY else DECEMBER
        previous_year = year if month > JANUARY else year - 1
        previous_month_sessions = Utils.count_sessions_this_month(sessions, previous_month, previous_year)

        if previous_month_sessions == 0:
            return float('inf') if current_month_sessions > 0 else 0.0  

        growth_rate = (current_month_sessions - previous_month_sessions) / previous_month_sessions * 100
        return round(growth_rate)

        
