class SharedState:
    def __init__(self):
        self.data_result = None
        self.events_result = None
        self.sessions_result = None
        self.users_result = None
        self.names = None
        self.json_tree = {}
    
    def is_session_create(self):
        return self.sessions_result!=None

    def is_users_create(self):
        return self.users_result!=None

    def is_events_create(self):
        return  self.events_result!=None
    
    def add_to_json_tree(self, json_data):
      

        def update_tree(tree, data):
            for key, value in data.items():            
                if isinstance(value, dict):
                    if key not in tree:
                        tree[key] = {}
                        update_tree(tree[key], value)
                else:
                    if key not in tree:
                        tree[key] = value

        update_tree(self.json_tree, json_data)

shared_state= SharedState()