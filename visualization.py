
import matplotlib.pyplot as plt
import numpy as np
from shared import shared_state, TypeOfData
from filters import data_filter
import constants



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
        names = check_event(event.__dict__[constants.EVENT_JSON], metric_names)
        if names is not None :
            if isinstance(names,str):
                if names in events_count:
                    events_count[names] += 1
                else:
                    events_count[names] = 1             
            else:
                for name in names:
                    if name in events_count:
                        events_count[name] += 1
                    else:
                        events_count[name] = 1
              
        
    
    return events_count


def create_chart(visualization_params):

    data = shared_state.events_result

    if visualization_params.get_time_limits:
        data= data_filter(data,visualization_params.start_date_entry,visualization_params.end_date_entry)

    if TypeOfData.TREE == visualization_params.type_of_data:
        events_count=counter_events_list(data,visualization_params.selected_data)
    elif TypeOfData.FIELD_NAME == visualization_params.type_of_data:
        events_count=counter_events(data,visualization_params.selected_data)

    visualization_params.selected_chart_type(visualization_params.canvas, events_count,visualization_params.selected_data)

def plot_line_chart(canvas,events_count,metric_name):
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    ax.set_title(metric_name)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig  
    canvas.draw()

def plot_bar_chart(canvas,events_count,metric_name):
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title(metric_name)
    ax.set_xlabel("Categories")
    ax.set_ylabel("Values")
    canvas.figure = fig  
    canvas.draw()

def plot_pie_chart(canvas,events_count,metric_name):
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.pie(y, labels=x, autopct='%1.1f%%')
    ax.set_title(metric_name)
    canvas.figure = fig 
    canvas.draw()

def plot_scatter_plot(canvas,events_count,metric_name):
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title(metric_name)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()


def plot_histogram(canvas,events_count,metric_name):
    x = list(events_count.keys())
    y = list(events_count.values())
    
    fig, ax = plt.subplots()
    ax.hist(y, bins=len(x), edgecolor='black')
    ax.set_title(metric_name)
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    canvas.figure = fig
    canvas.draw()

def plot_bubble_chart(canvas,events_count,metric_name):
    x = list(events_count.keys())
    y = list(events_count.values())
    sizes = y
    fig, ax = plt.subplots()
    ax.scatter(x, y,sizes)
    ax.set_title(metric_name)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()

def plot_area_chart(canvas,events_count,metric_name):
    
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.fill_between(x, y, color="skyblue", alpha=0.4)
    ax.plot(x, y, color="Slateblue", alpha=0.6)
    ax.set_title(metric_name)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    canvas.figure = fig 
    canvas.draw()