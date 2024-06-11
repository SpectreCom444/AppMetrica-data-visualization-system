from enums import GraphType, TypeOfMeasurement, Orientation, HistogramType, SplitTimeMode

from PyQt5.QtWidgets import QMessageBox

from ui.message import error

from collections import OrderedDict


class Plotter:

    def __init__(self, visualization_config):

        self.visualization_config = visualization_config

    def _get_canvas(self):

        return self.visualization_config.canvas

    def _convert_to_percentage(self, events_count):

        total = sum(events_count.values())

        return {k: (v / total) * 100 for k, v in events_count.items()}

    def _convert_to_percentage_split_event(self, events_count):

        total = 0

        for date, events in events_count.items():

            total += sum(events.values())

        for date, events in events_count.items():

            for event in events:

                events[event] = (events[event] / total) * 100
        return events_count

    def _sort_x_axis(self, events_count):

        sorted_items = sorted(events_count.items())

        sorted_keys, sorted_values = zip(*sorted_items)

        return OrderedDict(zip(sorted_keys, sorted_values))

    def _draw_figure(self):

        self._get_canvas().ax.set_title(

            self.visualization_config.selected_data)
        self._get_canvas().figure = self._get_canvas().fig

        self._get_canvas().draw()

    def plot_line_chart(self, events_count):

        events_count = self._sort_x_axis(events_count)

        x = list(events_count.keys())

        y = list(events_count.values())

        self._get_canvas().ax.plot(x, y, marker='o')

        self._draw_figure()

    def plot_bar_chart(self, events_count):

        events_count = self._sort_x_axis(events_count)

        x = list(events_count.keys())

        y = list(events_count.values())

        if self.visualization_config.orientation == Orientation.HORIZONTAL:

            self._get_canvas().ax.bar(x, y)

        elif self.visualization_config.orientation == Orientation.VERTICAL:

            self._get_canvas().ax.barh(x, width=y)

        self._draw_figure()

    def plot_pie_chart(self, events_count):

        events_count = self._sort_x_axis(events_count)

        x = list(events_count.keys())

        y = list(events_count.values())

        self._get_canvas().ax.pie(y, labels=x, autopct='%1.1f%%')

        self._draw_figure()

    def plot_ring_chart(self, events_count):

        events_count = self._sort_x_axis(events_count)

        x = list(events_count.keys())

        y = list(events_count.values())

        self._get_canvas().ax.pie(y, labels=x, autopct='%1.1f%%',

                                  wedgeprops=dict(width=0.65))

        self._draw_figure()

    def plot_scatter_plot(self, events_count):

        events_count = self._sort_x_axis(events_count)

        x = list(events_count.keys())

        y = list(events_count.values())

        self._get_canvas().ax.scatter(x, y)

        self._draw_figure()

    def plot_bubble_chart(self, events_count):

        events_count = self._sort_x_axis(events_count)

        x = list(events_count.keys())

        y = list(events_count.values())

        sizes = y

        self._get_canvas().ax.scatter(x, y, sizes)

        self._draw_figure()

    def plot_area_chart(self, events_count):

        events_count = self._sort_x_axis(events_count)

        x = list(events_count.keys())

        y = list(events_count.values())

        self._get_canvas().ax.fill_between(

            x, y, color="skyblue", alpha=0.4)

        self._get_canvas().ax.plot(

            x, y, color="Slateblue", alpha=0.6)

        self._draw_figure()

    def plot_funnel(self, events_count):

        sorted_events_count = OrderedDict(

            reversed(sorted(events_count.items(), key=lambda item: item[1])))

        x = list(sorted_events_count.keys())

        y = list(sorted_events_count.values())

        self._get_canvas().ax.bar(x, y)

        self._draw_figure()

    def plot_histogram_chart_split(self, element, event_types, data, x_label):

        if self.visualization_config.histogram_type == HistogramType.COMPARISON:

            width = 0.8 / len(event_types)

            positions = range(len(element))

            for i, event in enumerate(event_types):

                if self.visualization_config.orientation == Orientation.HORIZONTAL:

                    self._get_canvas().ax.bar([p + i * width for p in positions],

                                              data[event], width=width, label=event)

                elif self.visualization_config.orientation == Orientation.VERTICAL:

                    self._get_canvas().ax.barh([p + i * width for p in positions],

                                               data[event], height=width, label=event)

            if self.visualization_config.orientation == Orientation.HORIZONTAL:

                self._get_canvas().ax.set_xticks(

                    [p + width * (len(event_types) / 2) - width / 2 for p in positions])

                self._get_canvas().ax.set_xticklabels(element)

            elif self.visualization_config.orientation == Orientation.VERTICAL:

                self._get_canvas().ax.set_yticks(

                    [p + width * (len(event_types) / 2) - width / 2 for p in positions])

                self._get_canvas().ax.set_yticklabels(element)

        elif self.visualization_config.histogram_type == HistogramType.SUMMATION:

            bottom = [0] * len(element)

            for event in event_types:

                if self.visualization_config.orientation == Orientation.HORIZONTAL:

                    self._get_canvas().ax.bar(element, data[event],

                                              bottom=bottom, label=event)

                elif self.visualization_config.orientation == Orientation.VERTICAL:

                    self._get_canvas().ax.barh(element, data[event],

                                               left=bottom, label=event)

                bottom = [i + j for i, j in zip(bottom, data[event])]

        self._get_canvas().ax.set_ylabel('Counts')

        self._get_canvas().ax.set_xlabel(x_label)

        self._get_canvas().ax.legend()

        self._draw_figure()

    def plot_line_chart_split(self, element, event_types, data, x_label):

        for event in event_types:

            self._get_canvas().ax.plot(

                element, data[event], label=event)

        self._get_canvas().ax.set_ylabel('Counts')

        self._get_canvas().ax.set_xlabel(x_label)

        self._get_canvas().ax.legend()

        self._draw_figure()

    def plot_scatter_chart_split(self, element, event_types, data, x_label):

        for event in event_types:

            self._get_canvas().ax.scatter(

                element, data[event], label=event)

        self._get_canvas().ax.set_ylabel('Counts')

        self._get_canvas().ax.set_xlabel(x_label)

        self._get_canvas().ax.legend()

        self._draw_figure()

    def plot_area_chart_split(self, element, event_types, data, x_label):

        bottom = [0] * len(element)

        for event in event_types:

            self._get_canvas().ax.fill_between(element, bottom, [

                i + j for i, j in zip(bottom, data[event])], alpha=0.4, label=event)

            bottom = [i + j for i, j in zip(bottom, data[event])]

        self._get_canvas().ax.set_ylabel('Counts')

        self._get_canvas().ax.set_xlabel(x_label)

        self._get_canvas().ax.legend()

        self._draw_figure()

    def plot_split(self, events_count, x_label, loading):

        try:

            loading("creating a chart")

            self._get_canvas().create_axes()

            if self.visualization_config.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
                events_count = self._convert_to_percentage_split_event(
                    events_count)

            element = list(events_count.keys())

            event_types = list(

                {event for events in events_count.values() for event in events})

            data = {event: [events.get(

                event, 0) for events in events_count.values()] for event in event_types}

            if self.visualization_config.selected_chart_type == GraphType.LINE.value:

                self.plot_line_chart_split(element, event_types, data, x_label)

            elif self.visualization_config.selected_chart_type == GraphType.SCATTER.value:

                self.plot_scatter_chart_split(

                    element, event_types, data, x_label)

            elif self.visualization_config.selected_chart_type == GraphType.HISTOGRAM.value:

                self.plot_histogram_chart_split(

                    element, event_types, data, x_label)

            elif self.visualization_config.selected_chart_type == GraphType.AREA.value:

                self.plot_area_chart_split(element, event_types, data, x_label)

            else:

                raise ValueError(

                    "The data cannot be displayed on this type of histogram.")

        except Exception as e:

            error(f"An error occurred: {e}")

    def plot(self, events_count, loading):

        # try:

        loading("creating a chart")

        self._get_canvas().create_axes()

        if self.visualization_config.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

        if self.visualization_config.selected_chart_type == GraphType.LINE.value:

            self.plot_line_chart(events_count)

        elif self.visualization_config.selected_chart_type == GraphType.HISTOGRAM.value:

            self.plot_bar_chart(events_count)

        elif self.visualization_config.selected_chart_type == GraphType.PIE.value:

            self.plot_pie_chart(events_count)

        elif self.visualization_config.selected_chart_type == GraphType.RING.value:

            self.plot_ring_chart(events_count)

        elif self.visualization_config.selected_chart_type == GraphType.SCATTER.value:
            self.plot_scatter_plot(events_count)

        elif self.visualization_config.selected_chart_type == GraphType.BUBBLE.value:

            self.plot_bubble_chart(events_count)

        elif self.visualization_config.selected_chart_type == GraphType.AREA.value:

            self.plot_area_chart(events_count)

        elif self.visualization_config.selected_chart_type == GraphType.FUNNEL.value:
            self.plot_funnel(events_count)

        #     else:

        #         raise ValueError(

        #             "The data cannot be displayed on this type of histogram.")

        # except Exception as e:

        #     error(f"An error occurred: {e}")
