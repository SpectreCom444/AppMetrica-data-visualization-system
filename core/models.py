import json
from typing import List, Union, Dict, Any
from datetime import datetime
import config.constants as constants


class Event:
    def __init__(self, data):
        self.json_dict = {}
        for key, value in data:
            if key == constants.EVENT_JSON:
                self.json_dict[key] = self.convert_JSON_to_dict(value)
            elif key == constants.EVENT_DATATIME:
                self.json_dict[key] = datetime.strptime(
                    value, '%Y-%m-%d %H:%M:%S')
            else:
                self.json_dict[key] = value

    def get_value(self, key: str) -> Any:
        return self.json_dict.get(key)

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
        self._sessions = [session]
        self._id_user = session.get_id_user()

    def get_events(self) -> List[Event]:
        events = []
        for session in self.sessions:
            events.extend(session.get_events())
        return events

    @property
    def sessions(self) -> List[Session]:
        return self._sessions.copy()

    def add_session(self, session: Session):
        self.sessions.append(session)

    def get_id_user(self) -> str:
        return self._id_user
