import csv
import json
from models import Event, Session, User

def load_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        events = [list(map(str.strip, line)) for line in reader]
    return headers, events

def create_events(data, names):
    return [Event(names, row) for row in data]

def crate_sessions(events):
    sessions = []
    session_dict = {}

    for event in events:
        session_id = event.get_value('session_id')
        if session_id not in session_dict:
            new_session = Session(event)
            sessions.append(new_session)
            session_dict[session_id] = new_session
        else:
            session_dict[session_id].add_event(event)

    return sessions

def crate_users(sessions):
    users=[]
    users_dict = {}
    for session in sessions:
        user_id = session.get_id_user()
        if user_id not in users_dict:
            new_user = User(session)
            users.append(new_user)
            users_dict[user_id] = new_user
        else:
            users_dict[user_id].add_session(session)
    return users