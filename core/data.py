import time
import csv
from core.models import Event, Session, User
import config.constants as constants
from ui.messege import error
from config.constants import HIDDEN_ITEMS


class DataStorage:
    def __init__(self):
        self.data_result = None
        self.events_result = None
        self.sessions_result = None
        self.users_result = None
        self.names = None
        self.json_tree = {}
        self.ui_names = None

    def is_session_create(self):
        return self.sessions_result != None

    def add_to_json_tree(self, json_data):
        def update_tree(tree, data):
            for key, value in data.items():
                if key not in HIDDEN_ITEMS:
                    if isinstance(value, dict):
                        if key not in tree:
                            tree[key] = {}
                        update_tree(tree[key], value)
                    else:
                        if key not in tree:
                            tree[key] = {}
                        tree[key][value] = {}

        update_tree(self.json_tree, json_data)


class DataLoader:
    def __init__(self, path):
        self.path = path

    def load_data(self, load_data_done, data_storage):
        try:
            start_time = time.time()
            with open(self.path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data_storage.names = next(reader)
                data_storage.data_result = [
                    list(map(str.strip, line)) for line in reader][:15000]

            data_storage.ui_names = list(
                filter(lambda x: x not in constants.HIDDEN_ITEMS, data_storage.names))
            print(f"> Data loaded in {time.time() - start_time:.2f} seconds")
            load_data_done()
        except (UnicodeDecodeError, FileNotFoundError) as te:
            error(te)
        except Exception as e:
            error(e)


class DataProcessor:

    def processing_data(self, create_events_done, data_storage):
        start_time = time.time()
        data_storage.events_result = self.create_events(
            data_storage.data_result, data_storage.names)
        for event in data_storage.events_result:
            data_storage.add_to_json_tree(event.json_dict)
        print(f"> Events {len(data_storage.events_result)} created in {
              time.time() - start_time:.2f} seconds")
        create_events_done()

    def processing_session(self, create_session_done, data_storage):
        start_time = time.time()
        data_storage.sessions_result = self.create_sessions(
            data_storage.events_result)
        print(f"> Sessions {len(data_storage.sessions_result)} created in {
              time.time() - start_time:.2f} seconds")
        create_session_done()

    def processing_users(self, create_user_done, data_storage):
        start_time = time.time()
        data_storage.users_result = self.create_users(
            data_storage.sessions_result)
        print(f"> Users {len(data_storage.users_result)} created in {
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
