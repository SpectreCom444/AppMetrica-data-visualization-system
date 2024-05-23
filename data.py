import time
from data_loader import create_events,crate_sessions,crate_users,load_data

data_result = None
events_result = None
sessions_result = None
users_result = None
names = None

def load_data_wrapper():
    start_time = time.time()
    global data_result
    global names
    names,data_result = load_data("E://AppMetrica-data//test.csv")
    print(f"> data is loaded in {time.time() - start_time:.2f} seconds")
    data_processing()

def data_processing():
    start_time = time.time()
    global events_result
    events_result = create_events(data_result, names)
    print(f"> events {len(events_result)} created in {time.time() - start_time:.2f} seconds")

    if "session_id" in names:
        start_time = time.time()
        global sessions_result
        sessions_result = crate_sessions(events_result)
        print(f"> sessions {len(sessions_result)} created in {time.time() - start_time:.2f} seconds")

        if "appmetrica_device_id" in names:
            start_time = time.time()
            global users_result
            users_result = crate_users(sessions_result)
            print(f"> users {len(users_result)} created in {time.time() - start_time:.2f} seconds")

