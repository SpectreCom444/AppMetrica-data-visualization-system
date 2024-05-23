import json
from typing import List, Union, Dict, Any

KEY_JSON_FIELD = "event_json"

class Event:
    def __init__(self, field_names: List[str], values: List[str]):
        if len(field_names) != len(values):
            raise ValueError(f"The data is corrupted!\n"
                             f"The number of field names does not match the number of values.\n"
                             f"{len(field_names)}/{len(values)}\n"
                             f"{field_names}/{values}")

        self.__dict__ = {key: self.convert_JSON_to_dict(value) if key == KEY_JSON_FIELD else value
                         for key, value in zip(field_names, values)}

    def get_value(self, key: str) -> Any:
        return self.__dict__.get(key)

    @staticmethod
    def convert_JSON_to_dict(stringJSON: str) -> Union[str, List[Union[str, tuple]]]:
        def traverse_dict(d: Dict[str, Any], parent: str = None):
            for key, value in d.items():
                if parent is not None:
                    result.append((parent, key))
                if isinstance(value, dict):
                    traverse_dict(value, key)
                else:
                    result.append((key, value))

        if not stringJSON:
            return stringJSON
        data = json.loads(stringJSON)
        result = []
        traverse_dict(data)
        return result


class Session:
    def __init__(self, event: Event):
        self.events = [event]
        self.id_session = event.get_value("session_id")
        self.id_user = event.get_value("appmetrica_device_id")

    def add_event(self, event: Event):
        self.events.append(event)

    def get_events(self) -> List[Event]:
        return self.events

    def get_id_session(self) -> str:
        return self.id_session

    def get_id_user(self) -> str:
        return self.id_user


class User:
    def __init__(self, session: Session):
        self.sessions = [session]
        self.id_user = session.get_id_user()

    def get_events(self) -> List[Event]:
        events = []
        for session in self.sessions:
            events.extend(session.get_events())
        return events

    def get_sessions(self) -> List[Session]:
        return self.sessions

    def add_session(self, session: Session):
        self.sessions.append(session)

    def get_id_user(self) -> str:
        return self.id_user

