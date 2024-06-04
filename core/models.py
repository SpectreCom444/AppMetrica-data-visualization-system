import json
from typing import List, Union, Dict, Any
from core.shared import shared_state
from datetime import datetime
import config.constants as constants


class Event:
    def __init__(self, field_names: List[str], values: List[str]):
        if len(field_names) != len(values):
            raise ValueError(f"The data is corrupted!\n"
                             f"The number of field names does not match the number of values.\n"
                             f"{len(field_names)}/{len(values)}\n"
                             f"{field_names}/{values}")

        self.__dict__ = {}
        for key, value in zip(field_names, values):
            if key == constants.EVENT_JSON:
                json_dict = self.convert_JSON_to_dict(value)
                self.__dict__[key] = json_dict
                shared_state.add_to_json_tree(json_dict)
            elif key == constants.EVENT_DATATIME:
                self.__dict__[key] = datetime.strptime(
                    value, '%Y-%m-%d %H:%M:%S')
            else:
                self.__dict__[key] = value

    def get_value(self, key: str) -> Any:
        return self.__dict__.get(key)

    @staticmethod
    def convert_JSON_to_dict(stringJSON: str) -> Union[str, Dict[str, Any]]:
        if not stringJSON:
            return stringJSON
        return json.loads(stringJSON)


class Session:
    def __init__(self, event: Event):
        self.events = [event]
        self.id_session = event.get_value(constants.SESSION_ID)
        self.id_user = event.get_value(constants.DEVICE_ID)

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
