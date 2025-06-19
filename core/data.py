import time
import csv
from core.models import Event, Session, User
from config.constants import SESSION_ID, HIDDEN_ITEMS
from ui.message import error
from typing import Callable, List, Dict, Union, Optional
from typing import Any


class DataStorage:
    def __init__(self):
        self._raw_data: Optional[List[List[str]]] = None
        self._events: Optional[List[Event]] = None
        self._sessions: Optional[List[Session]] = None
        self._users: Optional[List[User]] = None
        self._headers: Optional[List[str]] = None
        self._json_structure: Dict = {}

    @property
    def events(self) -> Optional[List[Event]]:
        return self._events

    @property
    def sessions(self) -> Optional[List[Session]]:
        return self._sessions

    @property
    def users(self) -> Optional[List[User]]:
        return self._users

    @property
    def headers(self) -> Optional[List[str]]:
        return self._headers

    @property
    def json_structure(self) -> Dict:
        return self._json_structure

    def load_data(self, file_path: str, on_data_loaded: Callable[[], None]) -> None:
        data_loader = self._DataLoader(file_path, self)
        data_loader.load_data(on_data_loaded)

    def process_events(self, on_events_processed: Callable[[], None]) -> None:
        event_processor = self._EventProcessor(self)
        event_processor.process(on_events_processed)

    def process_sessions(self, on_sessions_processed: Callable[[], None]) -> None:
        session_processor = self._SessionProcessor(self)
        session_processor.process(on_sessions_processed)

    def process_users(self, on_users_processed: Callable[[], None]) -> None:
        user_processor = self._UserProcessor(self)
        user_processor.process(on_users_processed)

    class _Timer:
        def __init__(self):
            self.start_time: Optional[float] = None

        def start(self) -> None:
            self.start_time = time.time()

        def stop(self) -> float:
            return time.time() - self.start_time if self.start_time else 0.0

    class _JSONTreeBuilder:
        def __init__(self, data_storage: 'DataStorage'):
            self.json_structure: Dict = data_storage.json_structure

        def add_to_json_structure(self, json_data: Dict) -> None:
            def update_structure(structure: Dict, data: Dict) -> None:
                for key, value in data.items():
                    if key not in HIDDEN_ITEMS:
                        if isinstance(value, dict):
                            structure.setdefault(key, {})
                            update_structure(structure[key], value)
                        else:
                            structure.setdefault(key, {})
                            structure[key][value] = {}

            update_structure(self.json_structure, json_data)

    class _SessionProcessor:
        def __init__(self, data_storage: 'DataStorage'):
            self.data_storage: DataStorage = data_storage

        def process(self, on_sessions_processed: Callable[[], None]) -> None:
            try:
                timer = self.data_storage._Timer()
                timer.start()
                self.data_storage._sessions = self.create_sessions(
                    self.data_storage.events)
                print(f"{len(self.data_storage.sessions)} sessions created in {timer.stop():.2f} seconds.")

                on_sessions_processed()
            except Exception as err:
                error(f"An error occurred during session processing: {err}")

        @staticmethod
        def create_sessions(events: List[Event]) -> List[Session]:
            sessions: List[Session] = []
            session_dict: Dict[str, Session] = {}

            for event in events:
                session_id = event.get_value(SESSION_ID)
                if session_id not in session_dict:
                    new_session = Session(event)
                    sessions.append(new_session)
                    session_dict[session_id] = new_session
                else:
                    session_dict[session_id].events.append(event)

            return sessions

    class _UserProcessor:
        def __init__(self, data_storage: 'DataStorage'):
            self.data_storage: DataStorage = data_storage

        def process(self, on_users_processed: Callable[[], None]) -> None:
            try:
                timer = self.data_storage._Timer()
                timer.start()
                self.data_storage._users = self.create_users(
                    self.data_storage.sessions)
                print(f"{len(self.data_storage.users)} users created in {
                      timer.stop():.2f} seconds")
                on_users_processed()
            except Exception as err:
                error(f"An error occurred during user processing: {err}")

        @staticmethod
        def create_users(sessions: List[Session]) -> List[User]:
            users: List[User] = []
            user_dict: Dict[str, User] = {}

            for session in sessions:
                user_id = session.user_id
                if user_id not in user_dict:
                    new_user = User(session)
                    users.append(new_user)
                    user_dict[user_id] = new_user
                else:
                    user_dict[user_id].sessions.append(session)

            return users

    class _DataLoader:
        def __init__(self, file_path: str, data_storage: 'DataStorage'):
            self.file_path: str = file_path
            self.data_storage: DataStorage = data_storage

        def load_data(self, on_data_loaded: Callable[[], None]) -> None:
            try:
                if not self.file_path.lower().endswith('.csv'):
                    raise ValueError("File is not a CSV file")

                timer = self.data_storage._Timer()
                timer.start()
                with open(self.file_path, mode='r', encoding='utf-8-sig') as file:
                    reader = csv.reader(file)
                    self.data_storage._headers = next(reader)
                    self.data_storage._raw_data = [
                        list(map(str.strip, line)) for line in reader]

                print(f"Data loaded in {timer.stop():.2f} seconds")
                on_data_loaded()
            except (UnicodeDecodeError, FileNotFoundError) as err:
                error(f"File error: {err}")
            except Exception as err:
                error(f"An error occurred: {err}")

    class _EventProcessor:
        def __init__(self, data_storage: 'DataStorage'):
            self.data_storage: DataStorage = data_storage
            self._json_builder: DataStorage._JSONTreeBuilder = self.data_storage._JSONTreeBuilder(
                self.data_storage)

        def process(self, on_events_processed: Callable[[], None]) -> None:
            try:
                timer = self.data_storage._Timer()
                timer.start()
                self.data_storage._events = self.create_events(
                    self.data_storage._raw_data, self.data_storage._headers)
                del self.data_storage._raw_data
                for event in self.data_storage._events:
                    self._json_builder.add_to_json_structure(event.data)
                print(f"{len(self.data_storage._events)} events created in {
                      timer.stop():.2f} seconds")
                on_events_processed()
            except Exception as err:
                error(f"An error occurred during event processing: {err}")

        @staticmethod
        def create_events(data: List[List[str]], headers: List[str]) -> List[Event]:
            return [Event(dict(zip(headers, row))) for row in data]
