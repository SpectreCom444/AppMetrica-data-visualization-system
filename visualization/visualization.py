
import matplotlib.pyplot as plt
from core.shared import shared_state
from enums.enums import TypeOfData
from filters.filters import Filters
import config.constants as constants


def counter(elements,metric_name,visualization_params, filters):
    count = {}
    if visualization_params.type_data == constants.EVENTS:
        counter_events(elements,metric_name,visualization_params,count,filters)   
    elif visualization_params.type_data == constants.SESSIONS:
       counter_sessions(elements,metric_name,visualization_params,count,filters)   
    elif visualization_params.type_data == constants.USERS:
        counter_users(elements,metric_name,visualization_params,count,filters) 
            
    return count

def counter_sessions(elements,metric_name,visualization_params, count,filters):
    for sessions in elements:
        sessions_count={}       
        counter_events(sessions.get_events() ,metric_name, visualization_params, sessions_count,filters) 
        for key in sessions_count.keys():
            if key in count:
                count[key] += 1
            else:
                count[key] = 1

def counter_users(elements,metric_name,visualization_params, count,filters):
    for user in elements:
        user_count= {}
        counter_sessions(user.get_sessions(),metric_name,visualization_params,user_count,filters)                 
        for key in user_count.keys():
            if key in count:
                count[key] += 1
            else:
                count[key] = 1

def counter_events(elements,metric_name,visualization_params, count,filters):
    for event in elements:
        if filters.event_verification(event):
            if TypeOfData.FIELD_NAME == visualization_params.type_of_data:
                value = event.get_value(metric_name)
                if value in count:
                    count[value] += 1
                else:
                    count[value] = 1
            elif TypeOfData.TREE == visualization_params.type_of_data:
                value = counter_events_list(event,metric_name)
                if isinstance(value,str):
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
    if names is not None :
        return names     
              
        
    
    return events_count

def counting_other(data, other_threshold):
    total = sum(data.values())
    other_sum = 0

    keys_to_remove = [key for key, value in data.items() if (value / total)*100 < other_threshold]

    for key in keys_to_remove:
        other_sum += data.pop(key)

    if other_sum >0:
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

    events_count=counter(data,visualization_params.selected_data,visualization_params, filters)

    events_count = counting_other(events_count,visualization_params.other_reference )

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

def plot_ring_chart(canvas,events_count,metric_name):
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


def plot_funnel(canvas,events_count,metric_name):
    x = list(events_count.keys())
    y = list(events_count.values())
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title(metric_name)
    ax.set_xlabel("Categories")
    ax.set_ylabel("Values")
    canvas.figure = fig  
    canvas.draw()