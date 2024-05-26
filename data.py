import time
from data_loader import create_events,crate_sessions,crate_users,load_data

data_result = None
events_result = None
sessions_result = None
users_result = None
names = None

def is_session_create():
    return sessions_result!=None

def is_users_create():
    return users_result!=None

def is_events_create():
    return events_result!=None

def load_data_wrapper(load_data_done,):
    start_time = time.time()
    global data_result
    global names
    names,data_result = load_data("E://AppMetrica-data//test.csv")
    print(f"> data is loaded in {time.time() - start_time:.2f} seconds")
    load_data_done()

def data_processing(create_ui_session, create_ui_user):
    start_time = time.time()
    global events_result
    events_result = create_events(data_result, names)
    print(f"> events {len(events_result)} created in {time.time() - start_time:.2f} seconds")

    if "session_id" in names:
        create_ui_session()

        if "appmetrica_device_id" in names:
            create_ui_user()
            

def create_session(create_session_done):
    start_time = time.time()
    global sessions_result
    sessions_result = crate_sessions(events_result)
    print(f"> sessions {len(sessions_result)} created in {time.time() - start_time:.2f} seconds")
    create_session_done()

def create_users(create_user_done):
    if not is_session_create():
        create_session()
    
    start_time = time.time()
    global users_result
    users_result = crate_users(sessions_result)
    print(f"> users {len(users_result)} created in {time.time() - start_time:.2f} seconds")
    create_user_done()