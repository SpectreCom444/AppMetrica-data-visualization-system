
import matplotlib.pyplot as plt
import numpy as np
from shared import shared_state, TypeOfData

def counter_events(events, metric_name):
    events_count = {}
    for event in events:
        value = event.get_value(metric_name)
        if value in events_count:
            events_count[value] += 1
        else:
            events_count[value] = 1
    return events_count

def counter_events_list(events, metric_names):      

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
    for event in events:
        names = check_event(event.__dict__["event_json"], metric_names)
        if names is not None:
            for name in names:
                if name in events_count:
                    events_count[name] += 1
                else:
                    events_count[name] = 1
    
    return events_count


def create_chart(type_of_data, canvas,event_name,chart_type):
    if TypeOfData.TREE == type_of_data:
        events_count=counter_events_list(shared_state.events_result,event_name)
    elif TypeOfData.FIELD_NAME == type_of_data:
        events_count=counter_events(shared_state.events_result,event_name)


    if chart_type == 'line':
        plot_line_chart(canvas,events_count)
    elif chart_type == 'bar':
        plot_bar_chart(canvas,events_count)
    elif chart_type == 'pie':
        plot_pie_chart(canvas,events_count)
    elif chart_type == 'scatter':
        plot_scatter_plot(canvas,events_count)
    elif chart_type == 'histogram':
        plot_histogram(canvas,events_count)
    elif chart_type == 'heatmap':
        plot_heatmap(canvas,events_count)
    elif chart_type == 'bubble':
        plot_bubble_chart(canvas,events_count)
    elif chart_type == 'area':
        plot_area_chart(canvas,events_count)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

def plot_line_chart(canvas,events_count):
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    ax.set_title("Line Chart")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig  
    canvas.draw()

def plot_bar_chart(canvas,events_count):
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title("Bar Chart")
    ax.set_xlabel("Categories")
    ax.set_ylabel("Values")
    canvas.figure = fig  
    canvas.draw()

def plot_pie_chart(canvas,events_count):
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.pie(y, labels=x, autopct='%1.1f%%')
    ax.set_title("Pie Chart")
    canvas.figure = fig 
    canvas.draw()

def plot_scatter_plot(canvas,events_count):
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title("Scatter Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()


def plot_histogram(canvas,events_count):
    x = list(events_count.keys())
    y = list(events_count.values())
    
    fig, ax = plt.subplots()
    ax.hist(y, bins=len(x), edgecolor='black')
    ax.set_title("Histogram")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    canvas.figure = fig
    canvas.draw()

def plot_heatmap(canvas,events_count):
    data = np.random.rand(10, 10)
    fig, ax = plt.subplots()
    cax = ax.imshow(data, cmap='hot', interpolation='nearest')
    fig.colorbar(cax)
    ax.set_title("Heatmap")
    canvas.figure = fig 
    canvas.draw()

def plot_bubble_chart(canvas,events_count):
    x = list(events_count.keys())
    y = list(events_count.values())
    sizes = y
    fig, ax = plt.subplots()
    ax.scatter(x, y,sizes)
    ax.set_title("Bubble Chart")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()

def plot_area_chart(canvas,events_count):
    
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.fill_between(x, y, color="skyblue", alpha=0.4)
    ax.plot(x, y, color="Slateblue", alpha=0.6)
    ax.set_title("Area Chart")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()