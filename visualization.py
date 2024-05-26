
import matplotlib.pyplot as plt
import numpy as np
from data import shared_state

def counter_events(events, metric_name):
    events_count = {}
    for event in events:
        value = event.get_value(metric_name)
        if value in events_count:
            events_count[value] += 1
        else:
            events_count[value] = 1
    return events_count

def plot_line_chart(canvas,event_name):
    events_count=counter_events(shared_state.events_result,event_name)
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    ax.set_title("Line Chart")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig  
    canvas.draw()

def plot_bar_chart(canvas,event_name):
    events_count=counter_events(shared_state.events_result,event_name)
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title("Bar Chart")
    ax.set_xlabel("Categories")
    ax.set_ylabel("Values")
    canvas.figure = fig  
    canvas.draw()

def plot_pie_chart(canvas,event_name):
    events_count=counter_events(shared_state.events_result,event_name)
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.pie(y, labels=x, autopct='%1.1f%%')
    ax.set_title("Pie Chart")
    canvas.figure = fig 
    canvas.draw()

def plot_scatter_plot(canvas,event_name):
    events_count=counter_events(shared_state.events_result,event_name)
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title("Scatter Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()


def plot_histogram(canvas, event_name):
    events_count = counter_events(shared_state.events_result, event_name)
    x = list(events_count.keys())
    y = list(events_count.values())
    
    fig, ax = plt.subplots()
    ax.hist(y, bins=len(x), edgecolor='black')
    ax.set_title("Histogram")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    canvas.figure = fig
    canvas.draw()


def plot_heatmap(canvas,event_name):
    data = np.random.rand(10, 10)
    fig, ax = plt.subplots()
    cax = ax.imshow(data, cmap='hot', interpolation='nearest')
    fig.colorbar(cax)
    ax.set_title("Heatmap")
    canvas.figure = fig 
    canvas.draw()

def plot_bubble_chart(canvas,event_name):
    events_count=counter_events(shared_state.events_result,event_name)
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

def plot_area_chart(canvas,event_name):
    events_count=counter_events(shared_state.events_result,event_name)
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