import json

KEY_JSON_FIELD = "event_json"

class Event:
    def __init__(self, field_names, values):
        if len(field_names) != len(values):
            raise ValueError(f"The data is corrupted!\n"
                             f"The number of field names does not match the number of values.\n"
                             f"{len(field_names)}/{len(values)}\n"
                             f"{field_names}/{values}")
            
        for key, value in zip(field_names, values):
            if key==KEY_JSON_FIELD:
                converted_value = self.convert_JSON_to_dict(value)
                setattr(self, key, converted_value)
            else:
                setattr(self, key, value)
            
    def get_value(self, key):
        return getattr(self,key)
    
    @classmethod
    def convert_JSON_to_dict(cls, stringJSON):
        def traverse_dict(d, parent=None):
            for key, value in d.items():
                if parent is not None:
                    result.append((parent, key))
                if isinstance(value, dict):
                    traverse_dict(value, key)
                else:
                    result.append((key, value)) 
                    
        if stringJSON=="":
            return stringJSON
        data = json.loads(stringJSON)  
        result=[]
        traverse_dict(data)
        return result


class Session:
    def __init__(self, event):
        self.events = [event]
        self.id_session = event.get_value("session_id")
        self.id_user = event.get_value("appmetrica_device_id");

    def add_event(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events
    
    def get_id_session(self):
        return self.id_session 
    
    def get_id_user(self):
        return self.id_user 

class User:
    def __init__(self, session):
        self.sessions = [session]
        self.id_user = session.get_id_user();
        
    def get_events(self):
        events = []
        for session in  self.sessions:
            events.extend(session.get_events())
        return events
    
    def get_session(self):
        return self.sessions
    
    def add_session(self, session):
        self.sessions.append(session)
    
    def get_id_user(self):
        return self.id_user 
