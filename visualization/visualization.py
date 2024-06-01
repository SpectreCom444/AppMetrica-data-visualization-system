import matplotlib.pyplot as plt
from core.shared import shared_state
from enums.enums import TypeOfData, GraphType, TypeOfMeasurement,Orientation,HistogramType,DisplayMode
from filters.filters import Filters
import config.constants as constants


def counter(elements, metric_name, visualization_params, filters):
    count = {}
    if visualization_params.type_data == constants.EVENTS:
        counter_events(elements, metric_name, visualization_params, count, filters)
    elif visualization_params.type_data == constants.SESSIONS:
        counter_sessions(elements, metric_name, visualization_params, count, filters)
    elif visualization_params.type_data == constants.USERS:
        counter_users(elements, metric_name, visualization_params, count, filters)
    return count


def counter_sessions(elements, metric_name, visualization_params, count, filters):
    for sessions in elements:
        sessions_count = {}
        counter_events(sessions.get_events(), metric_name, visualization_params, sessions_count, filters)
        for key in sessions_count.keys():
            if key in count:
                count[key] += 1
            else:
                count[key] = 1


def counter_users(elements, metric_name, visualization_params, count, filters):
    for user in elements:
        user_count = {}
        counter_sessions(user.get_sessions(), metric_name, visualization_params, user_count, filters)
        for key in user_count.keys():
            if key in count:
                count[key] += 1
            else:
                count[key] = 1


def counter_events(elements, metric_name, visualization_params, count, filters):
    for event in elements:
        if filters.event_verification(event):
            if TypeOfData.FIELD_NAME == visualization_params.type_of_data:
                value = event.get_value(metric_name)
                if value in count:
                    count[value] += 1
                else:
                    count[value] = 1
            elif TypeOfData.TREE == visualization_params.type_of_data:
                value = counter_events_list(event, metric_name)
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
    names = check_event(event.__dict__[constants.EVENT_JSON], metric_names)
    if names is not None:
        return names

    return events_count


def counting_other(data, other_threshold):
    total = sum(data.values())
    other_sum = 0

    keys_to_remove = [key for key, value in data.items() if (value / total) * 100 < other_threshold]

    for key in keys_to_remove:
        other_sum += data.pop(key)

    if other_sum > 0:
        if 'other' in data:
            data['other'] += other_sum
        else:
            data['other'] = other_sum

    return data


def create_chart(visualization_params):
    if visualization_params.type_data == constants.EVENTS:
        data = shared_state.events_result
    elif visualization_params.type_data == constants.SESSIONS:
        data = shared_state.sessions_result
    elif visualization_params.type_data == constants.USERS:
        data = shared_state.users_result

    filters = Filters(visualization_params)

    if visualization_params.get_time_limits:
        filters.add_filter(filters.data_filter)

    events_count = counter(data, visualization_params.selected_data, visualization_params, filters)

    events_count = counting_other(events_count, visualization_params.other_reference)

    plotter = Plotter(visualization_params.canvas, visualization_params.selected_data, visualization_params.type_of_measurement,visualization_params.orientation)
    plotter.plot(visualization_params.selected_chart_type, events_count)


class Plotter:
    def __init__(self, canvas, metric_name, type_of_measurement,orientation, x_label="X-axis", y_label="Y-axis"):
        self.canvas = canvas
        self.metric_name = metric_name
        self.type_of_measurement = type_of_measurement
        self.orientation = orientation
        self.x_label = x_label
        self.y_label = y_label

    def _setup_plot(self, x, y):
        fig, ax = plt.subplots()
        ax.set_title(self.metric_name)
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        return fig, ax

    def _convert_to_percentage(self, events_count):
        total = sum(events_count.values())
        return {k: (v / total) * 100 for k, v in events_count.items()}

    def plot_line_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        fig, ax = self._setup_plot(x, y)
        ax.plot(x, y, marker='o')
        self.canvas.figure = fig
        self.canvas.draw()

    def plot_bar_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        fig, ax = self._setup_plot(x, y)
        if self.orientation == Orientation.HORIZONTAL:
            ax.bar(x, y)
        elif self.orientation == Orientation.VERTICAL:
            ax.barh(x, width=y)
        self.canvas.figure = fig
        self.canvas.draw()

    def plot_pie_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        fig, ax = plt.subplots()
        ax.pie(y, labels=x, autopct='%1.1f%%')
        ax.set_title(self.metric_name)
        self.canvas.figure = fig
        self.canvas.draw()

    def plot_ring_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        fig, ax = plt.subplots()
        ax.pie(y, labels=x, autopct='%1.1f%%', wedgeprops=dict(width=0.7))
        ax.set_title(self.metric_name)
        self.canvas.figure = fig
        self.canvas.draw()

    def plot_scatter_plot(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        fig, ax = self._setup_plot(x, y)
        ax.scatter(x, y)
        self.canvas.figure = fig
        self.canvas.draw()

    def plot_histogram(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        fig, ax = self._setup_plot(x, y)
        if self.orientation == Orientation.HORIZONTAL:
            ax.bar(x, y, edgecolor="black")
        elif self.orientation == Orientation.VERTICAL:
            ax.barh(x, width=y, edgecolor="black")

        self.canvas.figure = fig
        self.canvas.draw()

    def plot_bubble_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        sizes = y
        fig, ax = self._setup_plot(x, y)
        ax.scatter(x, y, sizes)
        self.canvas.figure = fig
        self.canvas.draw()

    def plot_area_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        fig, ax = self._setup_plot(x, y)
        ax.fill_between(x, y, color="skyblue", alpha=0.4)
        ax.plot(x, y, color="Slateblue", alpha=0.6)
        self.canvas.figure = fig
        self.canvas.draw()

    def plot_funnel(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        fig, ax = self._setup_plot(x, y)
        if self.orientation == Orientation.HORIZONTAL:
            ax.bar(x, y)
        elif self.orientation == Orientation.VERTICAL:
            ax.barh(x, width=y)
        self.canvas.figure = fig
        self.canvas.draw()

    def plot(self, chart_type, events_count):
        if chart_type == GraphType.LINE.value:
            self.plot_line_chart(events_count)
        elif chart_type == GraphType.BAR.value:
            self.plot_bar_chart(events_count)
        elif chart_type == GraphType.PIE.value:
            self.plot_pie_chart(events_count)
        elif chart_type == GraphType.RING.value:
            self.plot_ring_chart(events_count)
        elif chart_type == GraphType.SCATTER.value:
            self.plot_scatter_plot(events_count)
        elif chart_type == GraphType.HISTOGRAM.value:
            self.plot_histogram(events_count)
        elif chart_type == GraphType.BUBBLE.value:
            self.plot_bubble_chart(events_count)
        elif chart_type == GraphType.AREA.value:
            self.plot_area_chart(events_count)
        elif chart_type == GraphType.FUNNEL.value:
            self.plot_funnel(events_count)