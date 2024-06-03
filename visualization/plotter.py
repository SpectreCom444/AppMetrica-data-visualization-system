from enums.enums import GraphType, TypeOfMeasurement,Orientation,HistogramType,DisplayMode
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, visualization_config, x_label="X-axis", y_label="Y-axis"):
        self.canvas = visualization_config.canvas
        self.selected_data = visualization_config.selected_data
        self.type_of_measurement = visualization_config.type_of_measurement
        self.selected_chart_type = visualization_config.selected_chart_type
        self.orientation = visualization_config.orientation
        self.histogram_type =visualization_config.histogram_type
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
    
    def _convert_to_percentage_split_event(self, events_count):
        total =0
        for date, events in events_count.items():
            total += sum(events.values())

        for date, events in events_count.items():
            for event in events:
                events[event] = (events[event] / total) * 100
        return events_count
    
    def _sort_x_axis(self, events_count):
        sorted_items = sorted(events_count.items())
        sorted_keys, sorted_values = zip(*sorted_items)
        return dict(zip(sorted_keys, sorted_values))

    def plot_line_chart(self, events_count):
        
        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.plot(x, y, marker='o')
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_bar_chart(self, events_count):

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
        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.pie(y, labels=x, autopct='%1.1f%%')
        self.ax.set_title(self.selected_data)

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_ring_chart(self, events_count):

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.pie(y, labels=x, autopct='%1.1f%%', wedgeprops=dict(width=0.65))
        self.ax.set_title(self.selected_data)

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_scatter_plot(self, events_count):

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.scatter(x, y)

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_bubble_chart(self, events_count):

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        sizes = y
        self.ax.scatter(x, y, sizes)
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_area_chart(self, events_count):

        events_count = self._sort_x_axis(events_count)
        x = list(events_count.keys())
        y = list(events_count.values())
        self.ax.fill_between(x, y, color="skyblue", alpha=0.4)
        self.ax.plot(x, y, color="Slateblue", alpha=0.6)
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_funnel(self, events_count):

        sorted_events_count = dict(reversed(sorted(events_count.items(), key=lambda item: item[1])))

        x = list(sorted_events_count.keys())
        y = list(sorted_events_count.values())
        self.ax.bar(x, y)
            
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_histogram_chart_split(self, element, event_types, data, x_label):
        if self.histogram_type == HistogramType.COMPARISON:
            width = 0.8 / len(event_types)
            positions = range(len(element))
            for i, event in enumerate(event_types):
                if self.orientation == Orientation.HORIZONTAL:
                    self.ax.bar([p + i * width for p in positions], data[event], width=width, label=event)
                elif self.orientation == Orientation.VERTICAL:
                    self.ax.barh([p + i * width for p in positions], data[event], height=width, label=event)

            if self.orientation == Orientation.HORIZONTAL:
                self.ax.set_xticks([p + width * (len(event_types) / 2) - width / 2 for p in positions])
                self.ax.set_xticklabels(element)
            elif self.orientation == Orientation.VERTICAL:
                self.ax.set_yticks([p + width * (len(event_types) / 2) - width / 2 for p in positions])
                self.ax.set_yticklabels(element)
            
            
        elif self.histogram_type == HistogramType.SUMMATION:
            bottom = [0] * len(element)
            for event in event_types:
                if self.orientation == Orientation.HORIZONTAL:
                    self.ax.bar(element, data[event], bottom=bottom, label=event)
                elif self.orientation == Orientation.VERTICAL:
                    self.ax.barh(element, data[event], left=bottom, label=event)
                bottom = [i + j for i, j in zip(bottom, data[event])]

        self.ax.set_ylabel('Counts')
        self.ax.set_xlabel(x_label)  
        self.ax.set_title(self.selected_data)  
        self.ax.legend()
        
        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_line_chart_split(self,element,event_types,data, x_label):

        for event in event_types:
            self.ax.plot(element, data[event], label=event)

        self.ax.set_ylabel('Counts')
        self.ax.set_xlabel(x_label)
        self.ax.set_title(self.selected_data)
        self.ax.legend()

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_scatter_chart_split(self,element,event_types, data, x_label):

        for event in event_types:
            self.ax.scatter(element, data[event], label=event)

        self.ax.set_ylabel('Counts')
        self.ax.set_xlabel(x_label)
        self.ax.set_title(self.selected_data)
        self.ax.legend()

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_area_chart_split(self,element,event_types, data, x_label):

        bottom = [0] * len(element)
        for event in event_types:
            self.ax.fill_between(element, bottom, [i + j for i, j in zip(bottom, data[event])], alpha=0.4, label=event)
            bottom = [i + j for i, j in zip(bottom, data[event])]

        self.ax.set_ylabel('Counts')
        self.ax.set_xlabel(x_label)
        self.ax.set_title(self.selected_data)
        self.ax.legend()

        self.canvas.figure = self.fig
        self.canvas.draw()

    def plot_split(self, events_count, x_label):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage_split_event(events_count)
        element = list(events_count.keys())
        event_types = list({event for events in events_count.values() for event in events})
        data = {event: [events.get(event, 0) for events in events_count.values()] for event in event_types}

        if self.selected_chart_type == GraphType.LINE.value:
            self.plot_line_chart_split(element,event_types,data, x_label)
        elif self.selected_chart_type == GraphType.SCATTER.value:
            self.plot_scatter_chart_split(element,event_types,data, x_label)
        elif self.selected_chart_type == GraphType.HISTOGRAM.value:
            self.plot_histogram_chart_split(element,event_types,data, x_label)
        elif self.selected_chart_type == GraphType.AREA.value:
            self.plot_area_chart_split(element,event_types,data, x_label)
        else:
            print("Error chart type")

        

    def plot_split_date(self, events_count):
        self.plot_split(events_count, 'Date')

    def plot_split_hour(self, events_count):    
        self.plot_split(events_count, 'Hours')

    def plot(self, events_count):
        if self.type_of_measurement == TypeOfMeasurement.PERCENTAGES:
            events_count = self._convert_to_percentage(events_count)

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
        elif self.selected_chart_type == GraphType.BUBBLE.value:
            self.plot_bubble_chart(events_count)
        elif self.selected_chart_type == GraphType.AREA.value:
            self.plot_area_chart(events_count)
        elif self.selected_chart_type == GraphType.FUNNEL.value:
            self.plot_funnel(events_count)
        else:
            pass