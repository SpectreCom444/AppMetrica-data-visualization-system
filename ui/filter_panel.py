from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QTextEdit, QApplication, QSizePolicy
from PyQt5.QtCore import Qt
import sys
from typing import List


class FilterPanel(QWidget):
    def __init__(self, filters_layout_VS: QVBoxLayout, workspace_window: QWidget):
        super().__init__()
        self._filters_layout_VS: QVBoxLayout = filters_layout_VS
        self._workspace_window: QWidget = workspace_window
        self.filters: List[Filter] = []

    def add_filter(self) -> None:
        filter_widget = FilterWidget(self._workspace_window, self)
        self._filters_layout_VS.addWidget(filter_widget)
        self.filters.append(filter_widget.filter_instance)

    def remove_filter(self, filter_instance: 'Filter', filter_widget: QWidget) -> None:
        self._filters_layout_VS.removeWidget(filter_widget)
        filter_widget.deleteLater()
        self.filters.remove(filter_instance)

    def choose_metric(self, filter_instance: 'Filter') -> None:
        self._workspace_window.create_CEM_for_set_metric()
        self._workspace_window.custom_event_menu.set_parameters(
            filter_instance.apply_selected_options, filter_instance.selected_options)


class FilterWidget(QWidget):
    def __init__(self, workspace_window: QWidget, filter_panel: FilterPanel):
        super().__init__()
        self._filter_panel: FilterPanel = filter_panel
        self.filter_instance: Filter = Filter()

        filter_layout: QHBoxLayout = QHBoxLayout(self)

        self._path_metric_textedit: QTextEdit = QTextEdit()
        self._path_metric_textedit.setReadOnly(True)
        size_policy: QSizePolicy = self._path_metric_textedit.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Expanding)
        self._path_metric_textedit.setSizePolicy(size_policy)
        self.filter_instance.path_text = self._path_metric_textedit

        remove_filter_button: QPushButton = QPushButton("Remove")
        remove_filter_button.clicked.connect(self._remove_filter)

        invert_checkbox: QCheckBox = QCheckBox("Inverse")
        invert_checkbox.setChecked(False)
        invert_checkbox.stateChanged.connect(self._invert_filter)

        choose_metric_button: QPushButton = QPushButton("Choose")
        choose_metric_button.clicked.connect(self._choose_metric)

        filter_layout.addWidget(remove_filter_button)
        filter_layout.addWidget(invert_checkbox)
        filter_layout.addWidget(self._path_metric_textedit)
        filter_layout.addWidget(choose_metric_button)

    def _remove_filter(self) -> None:
        self._filter_panel.remove_filter(self.filter_instance, self)

    def _invert_filter(self, state: int) -> None:
        self.filter_instance.invert_filter(state)

    def _choose_metric(self) -> None:
        self._filter_panel.choose_metric(self.filter_instance)


class Filter:
    def __init__(self):
        self.invert: bool = False
        self.selected_options: List[str] = []
        self.path_text: QTextEdit = None

    def apply_selected_options(self, selected_options: List[str]) -> None:
        self.selected_options = selected_options
        self.path_text.clear()
        self.path_text.setText(" → ".join(selected_options))

    def invert_filter(self, state: int) -> None:
        self.invert = bool(state)
