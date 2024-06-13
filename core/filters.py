from typing import List, Any
from config.constants import EVENT_DATETIME
from datetime import datetime


class Filters:
    def event_verification(self, event: Any, filters_list: List['BaseFilter']) -> bool:
        for filter in filters_list:
            if not filter.check(event):
                return False
        return True


class BaseFilter:
    def check(self, event: Any) -> bool:
        raise NotImplementedError(
            "This method should be overridden by subclasses")


class DateFilter(BaseFilter):
    def __init__(self, start_date_entry: str, end_date_entry: str):
        self.__start_date_entry = datetime.strptime(
            start_date_entry, "%Y-%m-%d")
        self.__end_date_entry = datetime.strptime(end_date_entry, "%Y-%m-%d")

    def check(self, event: Any) -> bool:
        event_datetime = event.get_value(EVENT_DATETIME)
        return self.__start_date_entry <= event_datetime <= self.__end_date_entry


class EventFilter(BaseFilter):
    def __init__(self, invert: bool, selected_options: List[str]):
        self.__invert = invert
        self.__selected_options = selected_options

    def check(self, event: Any) -> bool:
        if not self.__selected_options:
            return True

        result = self.__check_event(event.data, self.__selected_options)
        return not result if self.__invert else result

    def __check_event(self, tree: dict, metric_names: List[str]) -> bool:
        if not metric_names:
            return True
        if metric_names[0] in tree:
            if len(metric_names) > 1:
                return self.__check_event(tree[metric_names[0]], metric_names[1:])
            else:
                return isinstance
