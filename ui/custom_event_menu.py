from PyQt5 import QtWidgets, QtCore
from typing import List, Union, Dict, Callable


class CustomEventMenu:
    def __init__(self, workspace_window: QtWidgets.QWidget):
        self._workspace_window: QtWidgets.QWidget = workspace_window
        self._buttons_list_layout: QtWidgets.QVBoxLayout = workspace_window.buttons_list_MS
        self._path_text_widget: QtWidgets.QTextEdit = workspace_window.path_text_MS
        self._back_button: QtWidgets.QPushButton = workspace_window.back_button_selection_MS
        self._selected_options: List[str] = []
        self._current_options: List[str] = list(
            workspace_window.data_storage.json_structure.keys())
        self._method_callback: Callable[[List[str]], None] = lambda x: None

        self._setup_ui()
        self._update_interface()

    def _setup_ui(self) -> None:
        self._buttons_list_layout.setAlignment(QtCore.Qt.AlignTop)
        self._back_button.clicked.connect(self._undo_last_selection)
        self._workspace_window.apply_MS.clicked.connect(self._apply)

    def _apply(self) -> None:
        self._workspace_window.visualization_settings_panel.show()
        self._workspace_window.metrics_list_panel.hide()
        self._method_callback(self._selected_options)

    def set_parameters(self, method_callback: Callable[[List[str]], None], selected_options: List[str]) -> None:
        self._method_callback = method_callback
        self._selected_options = selected_options
        self._update_interface()

    def _update_buttons(self) -> None:
        self._clear_buttons()
        current_level:  Dict = self._get_current_level()

        for option in self._current_options:
            button: QtWidgets.QPushButton = self._create_button(
                option, self._has_children(current_level, option))
            self._buttons_list_layout.addWidget(button)

    def _create_button(self, text: str, enabled: bool) -> QtWidgets.QPushButton:
        button: QtWidgets.QPushButton = QtWidgets.QPushButton(text)
        button.setEnabled(enabled)
        button.clicked.connect(self._create_button_handler(text))
        return button

    def _clear_buttons(self) -> None:
        while self._buttons_list_layout.count():
            widget: QtWidgets.QWidget = self._buttons_list_layout.takeAt(
                0).widget()
            if widget and isinstance(widget, QtWidgets.QPushButton) and widget != self._back_button:
                widget.deleteLater()

    def _get_current_level(self) -> Dict:
        current_level:  Dict = self._workspace_window.data_storage.json_structure
        for option in self._selected_options:
            current_level = current_level.get(
                option, {}) if isinstance(current_level, dict) else {}
        return current_level

    def _has_children(self, current_level:  Dict, option: str) -> bool:
        if isinstance(current_level, dict):
            child_level:  Dict = current_level.get(option, {})
            return isinstance(child_level, dict) and bool(child_level)
        return False

    def _create_button_handler(self, option: str) -> Callable[[], None]:
        def handler() -> None:
            self._add_to_selected(option)
        return handler

    def _add_to_selected(self, option: str) -> None:
        self._selected_options.append(option)
        self._update_interface()

    def _undo_last_selection(self) -> None:
        if self._selected_options:
            self._selected_options.pop()
            self._update_interface()

    def _update_back_button(self) -> None:
        self._back_button.setVisible(bool(self._selected_options))

    def _update_options(self) -> None:
        current_level: Dict = self._get_current_level()
        self._current_options = list(current_level.keys()) if isinstance(
            current_level, dict) else [current_level]
        self._update_buttons()

    def _update_path_text_widget(self) -> None:
        self._path_text_widget.clear()
        for i, option in enumerate(self._selected_options):
            indent: str = '    ' * i
            self._path_text_widget.append(
                f"{indent}﹂{option}" if i > 0 else f"{indent}{option}")

    def _update_interface(self) -> None:
        self._update_path_text_widget()
        self._update_options()
        self._update_back_button()
