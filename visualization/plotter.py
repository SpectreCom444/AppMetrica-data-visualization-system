from enums.enums import GraphType, TypeOfMeasurement,Orientation,HistogramType,DisplayMode
import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, visualization_config, x_label="X-axis", y_label="Y-axis"):
        print(visualization_config.selected_chart_type)
        self.canvas = visualization_config.canvas
        self.selected_data = visualization_config.selected_data
        self.type_of_measurement = visualization_config.type_of_measurement
        self.selected_chart_type=visualization_config.selected_chart_type
        self.orientation = visualization_config.orientation
        self.x_label = x_label
        self.y_label = y_label
        self.fig, self.ax = plt.subplots()
        
    def _setup_plot(self, x, y):
        self.ax.set_title(self.selected_data)
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)

    def _convert_to_percentage(self, events_count):
        total = sum(events_count.values())
        return {k: (v / total) * 100 for k, v in events_count.items()}
    
    def _sort_x_axis(self, events_count):
        sorted_items = sorted(events_count.items())
        sorted_keys, sorted_values = zip(*sorted_items)
        return dict(zip(sorted_keys, sorted_values))

    def plot_line_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)
        
        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.plot(x, y, marker='o')
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_bar_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        if self.orientation == Orientation.HORIZONTAL:
            self.ax.bar(x, y)
        elif self.orientation == Orientation.VERTICAL:
            self.ax.barh(x, width=y)
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_pie_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.pie(y, labels=x, autopct='%1.1f%%')
        self.ax.set_title(self.selected_data)

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_ring_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.pie(y, labels=x, autopct='%1.1f%%', wedgeprops=dict(width=0.65))
        self.ax.set_title(self.selected_data)

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_scatter_plot(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.scatter(x, y)

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_histogram(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        if self.orientation == Orientation.HORIZONTAL:
            self.ax.bar(x, y, edgecolor="black")
        elif self.orientation == Orientation.VERTICAL:
            self.ax.barh(x, width=y, edgecolor="black")

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_bubble_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        sizes = y
        self.ax.scatter(x, y, sizes)
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_area_chart(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.fill_between(x, y, color="skyblue", alpha=0.4)
        self.ax.plot(x, y, color="Slateblue", alpha=0.6)
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_funnel(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        if self.orientation == Orientation.HORIZONTAL:
            self.ax.bar(x, y)
        elif self.orientation == Orientation.VERTICAL:
            self.ax.barh(x, width=y)
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot(self, events_count):
        if self.selected_chart_type == GraphType.LINE.value:
            self.plot_line_chart(events_count)
        elif self.selected_chart_type == GraphType.BAR.value:
            self.plot_bar_chart(events_count)
        elif self.selected_chart_type == GraphType.PIE.value:
            self.plot_pie_chart(events_count)
        elif self.selected_chart_type == GraphType.RING.value:
            self.plot_ring_chart(events_count)
        elif self.selected_chart_type == GraphType.SCATTER.value:
            self.plot_scatter_plot(events_count)
        elif self.selected_chart_type == GraphType.HISTOGRAM.value:
            self.plot_histogram(events_count)
        elif self.selected_chart_type == GraphType.BUBBLE.value:
            self.plot_bubble_chart(events_count)
        elif self.selected_chart_type == GraphType.AREA.value:
            self.plot_area_chart(events_count)
        elif self.selected_chart_type == GraphType.FUNNEL.value:
            self.plot_funnel(events_count)
