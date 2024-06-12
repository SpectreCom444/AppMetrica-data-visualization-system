from PyQt5 import QtWidgets, QtCore
from typing import List, Union, Dict, Callable


class CustomEventMenu:
    def __init__(self, workspace_window):
        self.workspace_window = workspace_window
        self.buttons_list_layout = workspace_window.buttons_list_MS
        self.path_text_widget = workspace_window.path_text_MS
        self.back_button = workspace_window.back_button_selection_MS
        self.selected_options: List[str] = []
        self.current_options: List[str] = list(
            workspace_window.data_storage.json_structure.keys())

        self.setup_ui()
        self.update_buttons()
        self.update_back_button()

    def setup_ui(self):
        self.buttons_list_layout.setAlignment(QtCore.Qt.AlignTop)
        self.back_button.clicked.connect(self.undo_last_selection)
        self.workspace_window.apply_MS.clicked.connect(self.apply)

    def apply(self):
        self.workspace_window.visualization_settings_panel.show()
        self.workspace_window.metrics_list_panel.hide()
        self.method_callback(self.selected_options)

    def set_parameters(self, method_callback, selected_options: List[str]):
        self.method_callback = method_callback
        self.selected_options = selected_options
        self.update_interface()

    def update_buttons(self):
        self.clear_buttons()
        current_level = self.get_current_level()

        for option in self.current_options:
            button = self.create_button(
                option, self.has_children(current_level, option))
            self.buttons_list_layout.addWidget(button)

    def create_button(self, text: str, enabled: bool) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(text)
        button.setEnabled(enabled)
        button.clicked.connect(self.create_button_handler(text))
        return button

    def clear_buttons(self):
        for i in reversed(range(self.buttons_list_layout.count())):
            widget = self.buttons_list_layout.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QPushButton) and widget != self.back_button:
                widget.deleteLater()

    def get_current_level(self) -> Union[Dict, str]:
        current_level = self.workspace_window.data_storage.json_structure
        for option in self.selected_options:
            current_level = current_level.get(
                option, {}) if isinstance(current_level, dict) else {}
        return current_level

    def has_children(self, current_level: Dict, option: str) -> bool:
        child_level = current_level.get(option, {})
        return isinstance(child_level, dict) and bool(child_level)

    def create_button_handler(self, option: str):
        def handler():
            self.add_to_selected(option)
        return handler

    def add_to_selected(self, option: str):
        self.selected_options.append(option)
        self.update_interface()

    def undo_last_selection(self):
        if self.selected_options:
            self.selected_options.pop()
            self.update_interface()

    def update_back_button(self):
        self.back_button.setVisible(bool(self.selected_options))

    def update_options(self):
        current_level = self.get_current_level()
        self.current_options = list(current_level.keys()) if isinstance(
            current_level, dict) else [current_level]
        self.update_buttons()

    def update_path_text_widget(self):
        self.path_text_widget.clear()
        for i, option in enumerate(self.selected_options):
            indent = '    ' * i
            self.path_text_widget.append(
                f"{indent}﹂{str(option)}" if i > 0 else f"{indent}{str(option)}")

    def update_interface(self):
        self.update_path_text_widget()
        self.update_options()
        self.update_back_button()
