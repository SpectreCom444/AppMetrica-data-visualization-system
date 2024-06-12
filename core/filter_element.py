class Filter:
    def __init__(self, path_text):
        self.invert = False
        self.selected_options = []
        self.path_text = path_text

    def applay_selected_options(self, selected_options):
        self.selected_options = selected_options
        self.path_text.clear()
        self.path_text.setText(" → ".join(selected_options))

    def invert_filter(self, state):
        invert = bool(state)
