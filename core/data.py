import time
from core.shared import shared_state
from core.models import Event, Session, User
import config.constants as constants
import csv

def load_data(path,load_data_done):
    start_time = time.time()

    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        shared_state.names = next(reader)
        shared_state.data_result = [list(map(str.strip, line)) for line in reader][0:10000]
    print(f"> data is loaded in {time.time() - start_time:.2f} seconds")
    load_data_done()
  

def data_processing(create_events_done):
    start_time = time.time()
    shared_state.events_result = create_events(shared_state.data_result, shared_state.names)
    print(f"> events {len( shared_state.events_result)} created in {time.time() - start_time:.2f} seconds")
    create_events_done()
       
def create_session(create_session_done):
    start_time = time.time()
    shared_state.sessions_result = crate_sessions( shared_state.events_result)
    print(f"> sessions {len( shared_state.sessions_result)} created in {time.time() - start_time:.2f} seconds")
    create_session_done()

def create_users(create_user_done):
    if not shared_state.is_session_create():
        create_session()
    
    start_time = time.time()
    shared_state.users_result = crate_users( shared_state.sessions_result)
    print(f"> users {len( shared_state.users_result)} created in {time.time() - start_time:.2f} seconds")
    create_user_done()

def create_events(data, names):
    return [Event(names, row) for row in data]

def crate_sessions(events):
    sessions = []
    session_dict = {}

    for event in events:
        session_id = event.get_value(constants.SESSION_ID)
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
    
