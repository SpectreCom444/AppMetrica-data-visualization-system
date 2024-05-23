import time
from data_loader import load_data, create_events, crate_sessions, crate_users
from visualization import plot_data
from interface import create_ui

def main():
    start_time = time.time() 
    names, data = load_data('E://AppMetrica-data//test.csv')
    print(f"> data is loaded in {time.time() - start_time:.2f} seconds")
    
    start_time = time.time()
    events = create_events(data, names)
    print(f"> events {len(events)} created in {time.time() - start_time:.2f} seconds")
    
    if "session_id" in names:
        start_time = time.time()
        sessions = crate_sessions(events)
        print(f"> sessions {len(sessions)} created in {time.time() - start_time:.2f} seconds")
        
        if "appmetrica_device_id" in names:
            start_time = time.time()
            users = crate_users(sessions)
            print(f"> users {len(users)} created in {time.time() - start_time:.2f} seconds")
    
    print(names)
    print()
    print(data[0])

if __name__ == "__main__":
    main()
