from datetime import datetime

def data_filter(data, start_date_entry, end_date_entry):
    filtered_data = []
    for event in data:
        event_datetime = event.get_value("event_datetime")
        if start_date_entry <= event_datetime <= end_date_entry:
            filtered_data.append(event)
    return filtered_data