from enums import GraphType, TypeOfMeasurement, Orientation, HistogramType
from PyQt5.QtWidgets import QMessageBox
from ui.message import error
from collections import OrderedDict
from typing import Callable, Dict, List, Any
import matplotlib.colors as mcolors


class Plotter:
    def __init__(self, visualization_config: Any) -> None:
        self.visualization_config = visualization_config

    def _get_canvas(self) -> Any:
        return self.visualization_config.canvas

    def _convert_to_percentage(self, events_count: Dict[Any, int]) -> Dict[Any, float]:
        total = sum(events_count.values())
        return {k: (v / total) * 100 for k, v in events_count.items()}

    def _convert_to_percentage_split_event(self, events_count: Dict[str, Any]) -> Dict[str, Any]:
        total = sum(sum(events.values()) for events in events_count.values())
        for date, events in events_count.items():
            for event in events:
                events[event] = (events[event] / total) * 100
        return events_count

    def _sort_x_axis(self, events_count: Dict[Any, int]) -> OrderedDict:
        def is_number(s: Any) -> bool:
            try:
                float(s)
                return True
            except (ValueError, TypeError):
                return False
        numeric_items = []
        string_items = []
        for key, value in events_count.items():
            if is_number(key):
                numeric_items.append((float(key), key, value))  
            else:
                string_items.append((str(key), value))

        numeric_items.sort(key=lambda x: x[0])
        string_items.sort(key=lambda x: x[0])
        result = OrderedDict()
        for _, key, value in numeric_items:
            result[key] = value
        for key, value in string_items:
            result[key] = value
        return result

    def _draw_figure(self) -> None:
        self._get_canvas().ax.set_title(" → ".join(
            self.visualization_config.selected_options))
        self._get_canvas().figure = self._get_canvas().fig
        self._get_canvas().draw()

    def _plot_chart(self, x: List[Any], y: List[int], plot_func: Callable[[List[Any], List[int]], None]) -> None:
        plot_func(x, y)
        self._draw_figure()

    def plot_line_chart(self, events_count: Dict[Any, int]) -> None:
        self._plot_chart(
            *zip(*self._sort_x_axis(events_count).items()),
            self._get_canvas().ax.plot
        )

    def plot_bar_chart(self, events_count: Dict[Any, int]) -> None:
        x, y = zip(*self._sort_x_axis(events_count).items())
        plot_func = self._get_canvas(
        ).ax.bar if self.visualization_config.orientation == Orientation.HORIZONTAL else self._get_canvas().ax.barh
        self._plot_chart(x, y, plot_func)

    def get_pastel_colors(self, num_colors):
        base_colors = list(mcolors.TABLEAU_COLORS.values())
        pastel_colors = []
        for base in base_colors:
            rgb = mcolors.hex2color(base)
            pastel_rgb = [(x + 1) / 2.0 for x in rgb]
            pastel_colors.append(pastel_rgb)
        return pastel_colors[:num_colors]

    def plot_pie_chart(self, events_count: Dict[Any, int]) -> None:
        x, y = zip(*self._sort_x_axis(events_count).items())
        pastel_colors = self.get_pastel_colors(len(x))
        self._get_canvas().ax.pie(y, labels=x, autopct='%1.1f%%', colors=pastel_colors)
        self._draw_figure()

    def plot_ring_chart(self, events_count: Dict[Any, int]) -> None:
        x, y = zip(*self._sort_x_axis(events_count).items())
        pastel_colors = self.get_pastel_colors(len(x))
        self._get_canvas().ax.pie(y, labels=x, autopct='%1.1f%%',
                                  wedgeprops=dict(width=0.65), colors=pastel_colors)
        self._draw_figure()

    def plot_scatter_plot(self, events_count: Dict[Any, int]) -> None:
        self._plot_chart(
            *zip(*self._sort_x_axis(events_count).items()),
            self._get_canvas().ax.scatter
        )

    def plot_bubble_chart(self, events_count: Dict[Any, int]) -> None:
        x, y = zip(*self._sort_x_axis(events_count).items())
        self._get_canvas().ax.scatter(x, y, sizes=y)
        self._draw_figure()

    def plot_area_chart(self, events_count: Dict[Any, int]) -> None:
        x, y = zip(*self._sort_x_axis(events_count).items())
        self._get_canvas().ax.fill_between(x, y, color="skyblue", alpha=0.4)
        self._get_canvas().ax.plot(x, y, color="Slateblue", alpha=0.6)
        self._draw_figure()

    def plot_funnel(self, events_count: Dict[Any, int]) -> None:
        sorted_events_count = OrderedDict(
            reversed(sorted(events_count.items(), key=lambda item: item[1])))
        x, y = zip(*sorted_events_count.items())
        self._get_canvas().ax.bar(x, y)
        self._draw_figure()

    def plot_histogram_chart_split(self, element: List[Any], event_types: List[str], data: Dict[str, List[int]], x_label: str) -> None:
        if self.visualization_config.histogram_type == HistogramType.CLUSTERED:
            positions = range(len(element))

            if self.visualization_config.orientation == Orientation.HORIZONTAL:
                height = 0.8 / len(event_types)
                for i, event in enumerate(event_types):
                    self._get_canvas().ax.barh([p + i * height for p in positions],
                                               data[event], height=height, label=event)
                self._get_canvas().ax.set_yticks(
                    [p + height * (len(event_types) / 2) - height / 2 for p in positions])
                self._get_canvas().ax.set_yticklabels(element)
            else:
                width = 0.8 / len(event_types)
                for i, event in enumerate(event_types):
                    self._get_canvas().ax.bar([p + i * width for p in positions],
                                              data[event], width=width, label=event)
                self._get_canvas().ax.set_xticks(
                    [p + width * (len(event_types) / 2) - width / 2 for p in positions])
                self._get_canvas().ax.set_xticklabels(element)

        elif self.visualization_config.histogram_type == HistogramType.STACKET:
            for event in event_types:
                if self.visualization_config.orientation == Orientation.HORIZONTAL:
                    plot_func = self._get_canvas().ax.bar
                    plot_func(element, data[event], label=event)
                else:
                    plot_func = self._get_canvas().ax.barh
                    plot_func(element, data[event], label=event)
        self._get_canvas().ax.set_ylabel('Counts')
        self._get_canvas().ax.set_xlabel(x_label)
        self._get_canvas().ax.legend()
        self._draw_figure()

    def plot_chart_split(self, plot_func: Callable[[List[Any], List[int]], None], element: List[Any], event_types: List[str], data: Dict[str, List[int]], x_label: str) -> None:
        for event in event_types:
            plot_func(element, data[event], label=event)
        self._get_canvas().ax.set_ylabel('Counts')
        self._get_canvas().ax.set_xlabel(x_label)
        self._get_canvas().ax.legend()
        self._draw_figure()

    def plot_line_chart_split(self, element: List[Any], event_types: List[str], data: Dict[str, List[int]], x_label: str) -> None:
        self.plot_chart_split(self._get_canvas().ax.plot,
                              element, event_types, data, x_label)

    def plot_scatter_chart_split(self, element: List[Any], event_types: List[str], data: Dict[str, List[int]], x_label: str) -> None:
        self.plot_chart_split(self._get_canvas().ax.scatter,
                              element, event_types, data, x_label)

    def plot_area_chart_split(self, element: List[Any], event_types: List[str], data: Dict[str, List[int]], x_label: str) -> None:
        bottom = [0] * len(element)
        for event in event_types:
            self._get_canvas().ax.fill_between(element, bottom, [
                i + j for i, j in zip(bottom, data[event])], alpha=0.4, label=event)
            bottom = [i + j for i, j in zip(bottom, data[event])]
        self._get_canvas().ax.set_ylabel('Counts')
        self._get_canvas().ax.set_xlabel(x_label)
        self._get_canvas().ax.legend()
        self._draw_figure()

    def plot_split(self, events_count: Dict[str, Dict[str, int]], x_label: str, loading: Callable[[str], None]) -> None:
        try:
            loading("creating a chart")
            self._get_canvas().create_axes()
            if self.visualization_config.type_of_measurement == TypeOfMeasurement.PERCENTED:
                events_count = self._convert_to_percentage_split_event(
                    events_count)
            element = list(events_count.keys())
            event_types = list(
                {event for events in events_count.values() for event in events})
            data = {event: [events.get(
                event, 0) for events in events_count.values()] for event in event_types}
            chart_type = self.visualization_config.chart_type
            if chart_type == GraphType.LINE.value:
                self.plot_line_chart_split(element, event_types, data, x_label)
            elif chart_type == GraphType.SCATTER.value:
                self.plot_scatter_chart_split(
                    element, event_types, data, x_label)
            elif chart_type == GraphType.HISTOGRAM.value:
                self.plot_histogram_chart_split(
                    element, event_types, data, x_label)
            elif chart_type == GraphType.AREA.value:
                self.plot_area_chart_split(element, event_types, data, x_label)
            else:
                raise ValueError(
                    "The data cannot be displayed on this type of histogram.")
        except Exception as e:
            error(f"An error occurred: {e}")

    def plot(self, events_count: Dict[Any, int], loading: Callable[[str], None]) -> None:
        try:
            loading("creating a chart")
            self._get_canvas().create_axes()
            if self.visualization_config.type_of_measurement == TypeOfMeasurement.PERCENTED:
                events_count = self._convert_to_percentage(events_count)
            chart_type = self.visualization_config.chart_type
            if chart_type == GraphType.LINE.value:
                self.plot_line_chart(events_count)
            elif chart_type == GraphType.HISTOGRAM.value:
                self.plot_bar_chart(events_count)
            elif chart_type == GraphType.PIE.value:
                self.plot_pie_chart(events_count)
            elif chart_type == GraphType.RING.value:
                self.plot_ring_chart(events_count)
            elif chart_type == GraphType.SCATTER.value:
                self.plot_scatter_plot(events_count)
            elif chart_type == GraphType.BUBBLE.value:
                self.plot_bubble_chart(events_count)
            elif chart_type == GraphType.AREA.value:
                self.plot_area_chart(events_count)
            elif chart_type == GraphType.FUNNEL.value:
                self.plot_funnel(events_count)
            else:
                raise ValueError(
                    "The data cannot be displayed on this type of histogram.")
        except Exception as e:
            error(f"An error occurred: {e}")
