from typing import List, Dict, Any, Union
from enums import SplitTimeMode, GraphType, DateType
from config.constants import SPLIT_TIME_MODE, END_LOADING
from visualization.plotter import Plotter
from core.data_classes_visualization import VisualizationConfig
from ui.message import warning_dialog, warning, error
from config.graph_parameters import graph_parameters
from core.filters import DateFilter, EventFilter, Filters


class Counter:
    @staticmethod
    def count(elements: List[Any], visualization_config: VisualizationConfig, filters: Filters) -> Dict[str, int]:
        counter_map = {
            DateType.EVENTS: Counter._count_events,
            DateType.SESSIONS: Counter._count_sessions,
            DateType.USERS: Counter._count_users
        }
        return counter_map[visualization_config.type_data](elements, visualization_config, filters)

    @staticmethod
    def count_split_time(elements: List[Any], visualization_config: VisualizationConfig, filters: Filters, time_division_format: str) -> Dict[str, Dict[str, int]]:
        counter_map = {
            DateType.EVENTS: Counter._count_events_split_time,
            DateType.SESSIONS: Counter._count_sessions_split_time,
            DateType.USERS: Counter._count_users_split_time
        }
        return counter_map[visualization_config.type_data](elements, visualization_config, filters, time_division_format)

    @staticmethod
    def _count_sessions(elements: List[Any], visualization_config: VisualizationConfig, filters: Filters) -> Dict[str, int]:
        count = {}
        for sessions in elements:
            sessions_count = Counter._count_events(
                sessions.events, visualization_config, filters)
            for key in sessions_count:
                count[key] = count.get(key, 0) + 1
        return count

    @staticmethod
    def _count_sessions_split_time(elements: List[Any], count: Dict[str, Dict[str, int]], visualization_config: VisualizationConfig, filters: Filters, time_division_format: str) -> Dict[str, Dict[str, int]]:
        for sessions in elements:
            sessions_count = Counter._count_events_split_time(
                sessions.get_events(), count, visualization_config, filters, time_division_format)
            for event_time, events in sessions_count.items():
                if event_time not in count:
                    count[event_time] = {}
                for key, value in events.items():
                    count[event_time][key] = count[event_time].get(
                        key, 0) + value
        return count

    @staticmethod
    def _count_users(elements: List[Any], visualization_config: VisualizationConfig, filters: Filters) -> Dict[str, int]:
        count = {}
        for user in elements:
            user_count = Counter._count_sessions(
                user.sessions, visualization_config, filters)
            for key in user_count:
                count[key] = count.get(key, 0) + 1
        return count

    @staticmethod
    def _count_users_split_time(elements: List[Any], visualization_config: VisualizationConfig, filters: Filters, time_division_format: str) -> Dict[str, Dict[str, int]]:
        count = {}
        for user in elements:
            user_count = Counter._count_sessions_split_time(
                user.get_sessions(), count, visualization_config, filters, time_division_format)
            for event_time, events in user_count.items():
                if event_time not in count:
                    count[event_time] = {}
                for key, value in events.items():
                    count[event_time][key] = count[event_time].get(
                        key, 0) + value
        return count

    @staticmethod
    def _count_events(elements: List[Any], visualization_config: VisualizationConfig, filters: Filters) -> Dict[str, int]:
        count = {}
        for event in elements:
            if filters.event_verification(event, visualization_config.filters_list):
                value = Counter._get_event_value(
                    event, visualization_config.selected_data)
                if isinstance(value, str):
                    count[value] = count.get(value, 0) + 1
                else:
                    for name in value:
                        count[name] = count.get(name, 0) + 1
        return count

    @staticmethod
    def _count_events_split_time(elements: List[Any], count: Dict[str, Dict[str, int]], visualization_config: VisualizationConfig, filters: Filters, time_division_format: str) -> Dict[str, Dict[str, int]]:
        for event in elements:
            if filters.event_verification(event, visualization_config.filters_list):
                event_time = event.get_value(
                    "event_datetime").strftime(time_division_format)
                if event_time not in count:
                    count[event_time] = {}
                value = Counter._get_event_value(
                    event, visualization_config.selected_data)
                if isinstance(value, str):
                    count[event_time][value] = count[event_time].get(
                        value, 0) + 1
                else:
                    for name in value:
                        count[event_time][name] = count[event_time].get(
                            name, 0) + 1
        return count

    @staticmethod
    def _get_event_value(event: Any, metric_names: List[str]) -> Union[str, Dict[str, Any]]:
        def check_event(tree: Any, metric_names: List[str]) -> Union[str, Dict[str, Any]]:
            if metric_names[0] in tree:
                if len(metric_names) > 1:
                    return check_event(tree[metric_names[0]], metric_names[1:])
                else:
                    return tree.get(metric_names[0], {})
            else:
                return {}

        return check_event(event.data, metric_names)

    @staticmethod
    def apply_other_threshold(data: Dict[str, int], other_threshold: float) -> Dict[str, int]:
        total = sum(data.values())
        other_sum = 0
        keys_to_remove = [key for key, value in data.items() if (
            value / total) * 100 < other_threshold]

        for key in keys_to_remove:
            other_sum += data.pop(key)

        if other_sum > 0:
            data['other'] = data.get('other', 0) + other_sum

        return data

    @staticmethod
    def apply_other_threshold_split_time(data: Dict[str, Dict[str, int]], other_threshold: float) -> Dict[str, Dict[str, int]]:
        total = 0
        event_sums = {}

        for date, events in data.items():
            for event, count in events.items():
                total += count
                event_sums[event] = event_sums.get(event, 0) + count

        keys_to_remove = [key for key, value in event_sums.items() if (
            value / total) * 100 < other_threshold]

        for date, events in data.items():
            other_sum = 0
            for key in keys_to_remove:
                if key in events:
                    other_sum += events.pop(key)
            if other_sum > 0:
                events['other'] = events.get('other', 0) + other_sum

        return data


class DataVisualizer:

    def __init__(self, data_storage: Any, filter_panel: Any):
        self._visualization_config = VisualizationConfig()
        self._plotter = Plotter(self._visualization_config)
        self._data_storage = data_storage
        self._filter_panel = filter_panel
        self._filters = Filters()

    def plot_copy_chart(self, visualization_config: VisualizationConfig, loading: Any) -> None:
        self._visualization_config.copy(visualization_config)
        self._plotter.visualization_config = self._visualization_config
        self.add_chart(loading)

    def add_chart(self, loading: Any) -> None:
        loading("data processed...")
        if not self._visualization_config.selected_data:
            error("The metric for visualization is not selected.")
            return

        data = self._get_data()
        self._set_filters()

        if self._visualization_config.display_mode == SplitTimeMode.NOSPLIT or SPLIT_TIME_MODE not in graph_parameters[GraphType(self._visualization_config.selected_chart_type)]:
            events_count = Counter.count(
                data, self._visualization_config, self._filters)
            if not events_count:
                warning(
                    "Elements that would satisfy the selected filters are 0. It is impossible to build a chart.")
                return
            events_count = Counter.apply_other_threshold(
                events_count, self._visualization_config.other_reference)
            self._visualization_config.canvas.set_visualization_parameters(
                self._visualization_config)
            self._check_parameter_count(events_count)
            self._plotter.plot(events_count, loading)
        else:
            time_format = self._get_time_format()
            events_count = Counter.count_split_time(
                data, self._visualization_config, self._filters, time_format)
            if not events_count:
                warning(
                    "Elements that would satisfy the selected filters are 0. It is impossible to build a chart.")
                return
            events_count = Counter.apply_other_threshold_split_time(
                events_count, self._visualization_config.other_reference)
            self._visualization_config.canvas.set_visualization_parameters(
                self._visualization_config)
            self._plotter.plot_split(
                events_count, 'Date' if time_format == "%Y-%m-%d" else 'Hours', loading)

        self._visualization_config.canvas.draw()
        loading(END_LOADING)

    def _get_data(self) -> Any:
        data_map = {
            DateType.EVENTS: self._data_storage.events,
            DateType.SESSIONS: self._data_storage.sessions,
            DateType.USERS: self._data_storage.users
        }
        return data_map[self._visualization_config.type_data]

    def _set_filters(self) -> None:
        self._visualization_config.filters_list.clear()
        self._visualization_config.filters_list.append(DateFilter(
            self._visualization_config.start_date_entry, self._visualization_config.end_date_entry))

        for filter in self._filter_panel.filters:
            self._visualization_config.filters_list.append(
                EventFilter(filter.invert, filter.selected_options))

    def _check_parameter_count(self, events_count: Dict[str, int]) -> None:
        if len(events_count.keys()) > 15:
            if warning_dialog('There are too many parameters in this visualization. The names can be superimposed on each other. Increase the value of the "other" parameter to improve readability.'):
                return

    def _get_time_format(self) -> str:
        return "%Y-%m-%d" if self._visualization_config.display_mode == SplitTimeMode.SPLITBYDAY else "%Y-%m-%d %H"

    def set_orientation(self, orientation: str) -> None:
        self._visualization_config.orientation = orientation

    def set_other_reference(self, other_reference: float) -> None:
        self._visualization_config.other_reference = other_reference

    def set_selected_data(self, selected_data: List[str]) -> None:
        self._visualization_config.selected_data = selected_data

    def set_canvas(self, canvas: Any) -> None:
        self._visualization_config.canvas = canvas

    def set_chart_type(self, selected_chart_type: str) -> None:
        self._visualization_config.selected_chart_type = selected_chart_type

    def set_display_mode(self, display_mode: SplitTimeMode) -> None:
        self._visualization_config.display_mode = display_mode

    def set_histogram_type(self, histogram_type: str) -> None:
        self._visualization_config.histogram_type = histogram_type

    def set_type_of_measurement(self, type_of_measurement: str) -> None:
        self._visualization_config.type_of_measurement = type_of_measurement

    def set_data_time(self, start_date_entry: str, end_date_entry: str) -> None:
        start_date_entry = start_date_entry.toString('yyyy-MM-dd')
        end_date_entry = end_date_entry.toString('yyyy-MM-dd')

        self._visualization_config.start_date_entry = start_date_entry
        self._visualization_config.end_date_entry = end_date_entry

    def set_type_data(self, type_data: DateType) -> None:
        self._visualization_config.type_data = type_data
