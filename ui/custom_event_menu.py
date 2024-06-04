from core.shared import shared_state
from PyQt5 import QtWidgets

class CustomEventMenu:
    def __init__(self,workspace_window):

        self.matrix_of_buttons_grid= workspace_window.matrix_of_buttons_grid
        self.dictionary_path=workspace_window.dictionary_path
        self.undo_button= workspace_window.undo_button
        self.undo_button.clicked.connect(self.undo_last_selection)        
        self.selected_options = []
        self.current_options = list(shared_state.json_tree.keys())
        self.update_buttons()  
    
    def update_buttons(self):        

        for i in reversed(range(self.matrix_of_buttons_grid.count())):
            widget = self.matrix_of_buttons_grid.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QPushButton) and widget != self.undo_button:
                widget.deleteLater()
        
        current_level = shared_state.json_tree
        for opt in self.selected_options:
            if isinstance(current_level, dict):
                current_level = current_level.get(opt, {})
            else:
                current_level = {}
                break
        
        for idx, option in enumerate(self.current_options):     
            has_children = isinstance(current_level.get(option, {}), dict) and bool(current_level.get(option, {}))
            button = QtWidgets.QPushButton(option)
            button.setEnabled(has_children)
            button.clicked.connect(self.create_button_handler(option))
            self.matrix_of_buttons_grid.addWidget(button)

    def create_button_handler(self, option):
        def handler():
            self.add_to_selected(option)
        return handler
    
    def add_to_selected(self, option):
        if option not in self.selected_options:
            self.selected_options.append(option)
            self.update_text_widget()
            self.update_options()

    def undo_last_selection(self):
        if self.selected_options:
            self.selected_options.pop()
            self.update_text_widget()
            self.update_options()

    def update_options(self):
        current_level = shared_state.json_tree
        for opt in self.selected_options:
            if isinstance(current_level, dict):
                current_level = current_level.get(opt, {})
            else:
                current_level = {}
                break

        if isinstance(current_level, dict):
            self.current_options = list(current_level.keys())
        else:
            self.current_options = [current_level]
        self.update_buttons()
    
    def update_text_widget(self):
        self.dictionary_path.clear()
        for option in self.selected_options:
            self.dictionary_path.setText(self.dictionary_path.text() + str(option) + '->')

    def get_selected_options(self):
        return self.selected_options 
