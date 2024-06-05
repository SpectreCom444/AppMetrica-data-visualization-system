from enums import DisplayMode, GraphType
from core.filters import Filters
from config.constants import EVENTS, SESSIONS, USERS, EVENT_JSON, DISPLAY_MODE, END_LOADING
from visualization.plotter import Plotter
from core.data_classes_visualization import VisualizationConfig
from ui.messege import warning_dialog, warning
from config.graph_parameters import graph_parameters


class Counter:
    pass


class DataVisualizer:

    def __init__(self):
        self.visualization_config = VisualizationConfig()
        self.plotter = Plotter(self.visualization_config)

    def counter(self, elements, filters):
        count = {}
        if self.visualization_config.type_data == EVENTS:
            self.counter_events(elements, count, filters)
        elif self.visualization_config.type_data == SESSIONS:
            self.counter_sessions(elements, count, filters)
        elif self.visualization_config.type_data == USERS:
            self.counter_users(elements, count, filters)
        return count

    def counter_split_time(self, elements, filters, time_division_format):
        count = {}
        if self.visualization_config.type_data == EVENTS:
            self.counter_events_split_time(
                elements, count, filters, time_division_format)
        elif self.visualization_config.type_data == SESSIONS:
            self.counter_sessions_split_time(
                elements, count, filters, time_division_format)
        elif self.visualization_config.type_data == USERS:
            self.counter_users_split_time(
                elements, count, filters, time_division_format)
        return count

    def counter_sessions(self, elements, count, filters):
        for sessions in elements:
            sessions_count = {}
            self.counter_events(sessions.get_events(), sessions_count, filters)
            for key in sessions_count.keys():
                if key in count:
                    count[key] += 1
                else:
                    count[key] = 1

    def counter_sessions_split_time(self, elements, count, filters, time_division_format):
        for sessions in elements:
            sessions_count = {}
            self.counter_events_split_time(
                sessions.get_events(), sessions_count, filters, time_division_format)
            for event_time in sessions_count.keys():
                if event_time not in count:
                    count[event_time] = {}
                for key in sessions_count[event_time].keys():
                    if key in count[event_time]:
                        count[event_time][key] += 1
                    else:
                        count[event_time][key] = 1

    def counter_users(self, elements, count, filters):
        for user in elements:
            user_count = {}
            self.counter_sessions(user.get_sessions(), user_count, filters)
            for key in user_count.keys():
                if key in count:
                    count[key] += 1
                else:
                    count[key] = 1

    def counter_users_split_time(self, elements, count, filters, time_division_format):
        for user in elements:
            user_count = {}
            self.counter_sessions_split_time(
                user.get_sessions(), user_count, filters, time_division_format)
            for event_time in user_count.keys():
                if event_time not in count:
                    count[event_time] = {}
                for key in user_count[event_time].keys():
                    if key in count[event_time]:
                        count[event_time][key] += 1
                    else:
                        count[event_time][key] = 1

    def counter_events(self, elements, count, filters):
        for event in elements:
            if filters.event_verification(event):
                value = self.counter_events_list(
                    event, self.visualization_config.selected_data)
                if isinstance(value, str):
                    if value in count:
                        count[value] += 1
                    else:
                        count[value] = 1
                else:
                    for name in value:
                        if name in count:
                            count[name] += 1
                        else:
                            count[name] = 1
        return count

    def counter_events_split_time(self, elements, count, filters, time_division_format):
        for event in elements:
            if filters.event_verification(event):
                event_time = event.get_value(
                    "event_datetime").strftime(time_division_format)

                if event_time not in count:
                    count[event_time] = {}
                value = self.counter_events_list(
                    event, self.visualization_config.selected_data)
                if isinstance(value, str):
                    if value in count[event_time]:
                        count[event_time][value] += 1
                    else:
                        count[event_time][value] = 1
                else:
                    for name in value:
                        if name in count[event_time]:
                            count[event_time][name] += 1
                        else:
                            count[event_time][name] = 1
        return count

    @staticmethod
    def counter_events_list(event, metric_names):
        def check_event(tree, metric_names):
            if metric_names[0] in tree:
                if len(metric_names) > 1:
                    return check_event(tree[metric_names[0]], metric_names[1:])
                else:
                    if isinstance(tree, dict):
                        return tree[metric_names[0]]
                    else:
                        return None
            else:
                return None

        events_count = {}
        names = check_event(event.json_dict, metric_names)
        if names is not None:
            return names

        return events_count

    @staticmethod
    def counting_other(data, other_threshold):
        total = sum(data.values())
        other_sum = 0

        keys_to_remove = [key for key, value in data.items() if (
            value / total) * 100 < other_threshold]

        for key in keys_to_remove:
            other_sum += data.pop(key)

        if other_sum > 0:
            if 'other' in data:
                data['other'] += other_sum
            else:
                data['other'] = other_sum

        return data

    @staticmethod
    def counting_other_split_time(data, other_threshold):
        total = 0
        event_sums = {}

        for date, events in data.items():
            for event, count in events.items():
                total += count
                if event in event_sums:
                    event_sums[event] += count
                else:
                    event_sums[event] = count

        keys_to_remove = [key for key, value in event_sums.items() if (
            value / total) * 100 < other_threshold]

        for date, events in data.items():
            other_sum = 0
            for key in keys_to_remove:
                if key in events:
                    other_sum += events.pop(key)
            if other_sum > 0:
                if 'other' in events:
                    events['other'] += other_sum
                else:
                    events['other'] = other_sum

        return data

    def plot_copy_chart(self, visualization_config, loading):
        self.visualization_config.copy(visualization_config)
        self.plotter_set_visualization_config()
        self.add_chart(loading)

    def add_chart(self, loading, data):
        loading("data preparation")
        filters = Filters(self.visualization_config)
        filters.add_filter(filters.data_filter)

        if self.visualization_config.display_mode == DisplayMode.TOTAL or DISPLAY_MODE not in graph_parameters[GraphType(self.visualization_config.selected_chart_type)]:
            events_count = self.counter(data, filters)
            if not events_count:
                warning(
                    "Elements that would satisfy the selected filters are 0. It is impossible to build a chart.")
                return
            events_count = self.counting_other(
                events_count, self.visualization_config.other_reference)
            self.visualization_config.canvas.set_visualization_parameters(
                self.visualization_config)
            if len(events_count.keys()) > 15:
                if warning_dialog(f"There will be more than 15 labels on this visualization. Increase the value of the other parameter to improve readability."):
                    return
            self.plotter.plot(events_count, loading)

        elif self.visualization_config.display_mode == DisplayMode.DAY:
            events_count = self.counter_split_time(data, filters, "%Y-%m-%d")
            if not events_count:
                warning(
                    "Elements that would satisfy the selected filters are 0. It is impossible to build a chart.")
                return

            events_count = self.counting_other_split_time(
                events_count, self.visualization_config.other_reference)
            self.visualization_config.canvas.set_visualization_parameters(
                self.visualization_config)
            self.plotter.plot_split(events_count, 'Date', loading)

        elif self.visualization_config.display_mode == DisplayMode.HOURSE:
            events_count = self.counter_split_time(
                data, filters, "%Y-%m-%d %H")

            if not events_count:
                warning(
                    "Elements that would satisfy the selected filters are 0. It is impossible to build a chart.")
                return

            events_count = self.counting_other_split_time(
                events_count, self.visualization_config.other_reference)
            self.visualization_config.canvas.set_visualization_parameters(
                self.visualization_config)
            self.plotter.plot_split(events_count, 'Hours', loading)

        self.visualization_config.canvas.draw()
        loading(END_LOADING)

    def plotter_set_visualization_config(self):
        self.plotter.visualization_config = self.visualization_config

    def set_orientation(self, orientation):
        self.visualization_config.orientation = orientation

    def set_other_reference(self, other_reference):
        self.visualization_config.other_reference = other_reference

    def set_selected_data(self, selected_data):
        self.visualization_config.selected_data = selected_data

    def set_canvas(self, canvas):
        self.visualization_config.canvas = canvas

    def set_chart_type(self, selected_chart_type):
        self.visualization_config.selected_chart_type = selected_chart_type

    def set_display_mode(self, display_mode):
        self.visualization_config.display_mode = display_mode

    def set_histogram_type(self, histogram_type):
        self.visualization_config.histogram_type = histogram_type

    def set_type_of_measurement(self, type_of_measurement):
        self.visualization_config.type_of_measurement = type_of_measurement

    def set_data_time(self, start_date_entry, end_date_entry):
        if isinstance(start_date_entry, str) and len(start_date_entry) == 10:
            start_date_entry += ' 00:00:00'
        if isinstance(end_date_entry, str) and len(end_date_entry) == 10:
            end_date_entry += ' 23:59:59'

        self.visualization_config.start_date_entry = start_date_entry
        self.visualization_config.end_date_entry = end_date_entry

    def set_type_data(self, type_data):
        self.visualization_config.type_data = type_data
