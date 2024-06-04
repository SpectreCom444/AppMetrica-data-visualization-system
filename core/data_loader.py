import time
import csv
from core.shared import shared_state
from core.models import Event, Session, User
import config.constants as constants
from ui.messege import error


class DataProcessor:
    def __init__(self, path):
        self.path = path

    def load_data(self, load_data_done):
        try:
            start_time = time.time()
            with open(self.path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                shared_state.names = next(reader)
                shared_state.data_result = [
                    list(map(str.strip, line)) for line in reader][:15000]

            shared_state.ui_names = list(
                filter(lambda x: x not in constants.HIDDEN_ITEMS, shared_state.names))
            print(f"> Data loaded in {time.time() - start_time:.2f} seconds")
            load_data_done()
        except (UnicodeDecodeError, FileNotFoundError) as te:
            error(te)
        except Exception as e:
            error(e)

    def processing_data(self, create_events_done):
        start_time = time.time()
        shared_state.events_result = self.create_events(
            shared_state.data_result, shared_state.names)
        print(f"> Events {len(shared_state.events_result)} created in {
              time.time() - start_time:.2f} seconds")
        create_events_done()

    def processing_session(self, create_session_done):
        start_time = time.time()
        shared_state.sessions_result = self.create_sessions(
            shared_state.events_result)
        print(f"> Sessions {len(shared_state.sessions_result)} created in {
              time.time() - start_time:.2f} seconds")
        create_session_done()

    def processing_users(self, create_user_done):
        start_time = time.time()
        shared_state.users_result = self.create_users(
            shared_state.sessions_result)
        print(f"> Users {len(shared_state.users_result)} created in {
              time.time() - start_time:.2f} seconds")
        create_user_done()

    def create_events(self, data, names):
        return [Event(zip(names, row)) for row in data]

    def create_sessions(self, events):
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

    def create_users(self, sessions):
        users = []
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
