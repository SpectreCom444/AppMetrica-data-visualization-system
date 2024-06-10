from PyQt5 import QtWidgets


class CustomEventMenu:
    def __init__(self, workspace_window):

        self.workspace_window = workspace_window
        self.buttons_list_MS = workspace_window.buttons_list_MS
        self.path_text_MS = workspace_window.path_text_MS
        self.back_button_selction_MS = workspace_window.back_button_selction_MS
        self.back_button_selction_MS.clicked.connect(self.undo_last_selection)
        self.selected_options = []
        self.current_options = list(
            self.workspace_window.data_storage.json_structure.keys())
        self.update_buttons()
        self.workspace_window.apply_MS.clicked.connect(
            self.close_CEM_panel)

    def close_CEM_panel(self):
        self.workspace_window.visualization_settings_panel.show()
        self.workspace_window.metrics_list_panel.hide()

    def update_buttons(self):

        for i in reversed(range(self.buttons_list_MS.count())):
            widget = self.buttons_list_MS.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QPushButton) and widget != self.back_button_selction_MS:
                widget.deleteLater()

        current_level = self.workspace_window.data_storage.json_structure
        for opt in self.selected_options:
            if isinstance(current_level, dict):
                current_level = current_level.get(opt, {})
            else:
                current_level = {}
                break

        for idx, option in enumerate(self.current_options):
            has_children = isinstance(current_level.get(
                option, {}), dict) and bool(current_level.get(option, {}))
            button = QtWidgets.QPushButton(option)
            button.setEnabled(has_children)
            button.clicked.connect(self.create_button_handler(option))
            self.buttons_list_MS.addWidget(button)

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
        current_level = self.workspace_window.data_storage.json_structure
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
        self.path_text_MS.clear()
        for option in self.selected_options:
            self.path_text_MS.setPlainText(
                self.path_text_MS.toPlainText() + str(option) + '->')

    def get_selected_options(self):
        return self.selected_options
