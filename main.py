from data_loader import load_data, crate_events, crate_sessions, crate_users
from visualization import plot_data
from interface import create_ui

def main():
    names, data = load_data('E://AppMetrica-data//test.csv')
    print(f"> data is load")
    events = crate_events(data,names)
    print(f"> events {len(events)}")
    if "session_id" in names:
        sessions = crate_sessions(events)
        print(f"> sessions {len(sessions)}")
        if "appmetrica_device_id" in names:  
            users = crate_users(sessions)
            print(f"> users {len(users)}")
    
    print(names)
    print()
    print(data[0:1])

if __name__ == "__main__":
    main()
