import time
from data_loader import create_events,crate_sessions,crate_users,load_data
from shared import shared_state


def load_data_wrapper(load_data_done,):
    start_time = time.time()
    shared_state.names,shared_state.data_result = load_data("E://AppMetrica-data//test.csv")
    print(*shared_state.names)
    print(f"> data is loaded in {time.time() - start_time:.2f} seconds")
    load_data_done()
  

def data_processing(create_ui_session, create_ui_user):
    start_time = time.time()
    shared_state.events_result = create_events(shared_state.data_result, shared_state.names)
    print(f"> events {len( shared_state.events_result)} created in {time.time() - start_time:.2f} seconds")

    if "session_id" in  shared_state.names:
        create_ui_session()

        if "appmetrica_device_id" in  shared_state.names:
            create_ui_user()
            

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