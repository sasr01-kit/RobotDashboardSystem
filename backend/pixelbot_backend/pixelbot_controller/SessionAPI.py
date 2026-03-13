'''SessionAPI provides methods to retrieve session data for a specific child or all sessions across children, 
    returning the data as dictionaries suitable for JSON responses.'''
class SessionAPI:

    def __init__(self):
        pass

    '''Retrieve a specific session for a given child ID and session ID, returning the session data as a dictionary.'''    
    def send_session(self, child_id, session_id, children):
        for child in children:
            if child.child_id == child_id:
                for session in child.sessions:
                    
        # Return the session data as a dictionary (for JSON response)
                    if session.get_session_id() == session_id:
                        return session.to_dict()

        return None
    
    '''Retrieve all sessions across all children, returning a list of session data dictionaries, each including the child ID.'''
    def send_all_sessions(self, children):
        all_sessions = []

        for child in children:
            for session in child.sessions:
                session_dict = session.to_dict()
                # add child ID to session data
                session_dict["childId"] = child.child_id
            
        # Returns a list of all session dictionaries, each with its childId
                all_sessions.append(session_dict)

        return all_sessions
