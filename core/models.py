import json
from typing import List, Union, Dict, Any
from datetime import datetime
from config.constants import EVENT_JSON, EVENT_DATETIME, SESSION_ID, DEVICE_ID
from ui.message import error


class Event:
    def __init__(self, data: List[tuple]):
        self._data: Dict[str, Any] = {key: self._process_value(
            key, value) for key, value in data.items()}

    @staticmethod
    def _process_value(key: str, value: str) -> Any:
        if key == EVENT_JSON:
            return Event._convert_json_to_dict(value)
        elif key == EVENT_DATETIME:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value

    @staticmethod
    def _convert_json_to_dict(json_string: str) -> Union[str, Dict[str, Any]]:
        if not json_string:
            return json_string
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            error(f"Error decoding the json string: {json_string}")

    def get_value(self, key: str) -> Any:
        return self.data.get(key)

    @property
    def data(self) -> dict:
        return self._data


class Session:
    def __init__(self, event: Event):
        self.events: List[Event] = [event]
        self._session_id: str = event.get_value(SESSION_ID)
        self._user_id: str = event.get_value(DEVICE_ID)

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def user_id(self) -> str:
        return self._user_id


class User:
    def __init__(self, session: Session):
        self.sessions: List[Session] = [session]
        self._user_id: str = session.user_id

    @property
    def events(self) -> List[Event]:
        return [event for session in self._sessions for event in session.events]

    @property
    def user_id(self) -> str:
        return self._user_id
