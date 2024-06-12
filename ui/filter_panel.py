from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QTextEdit, QApplication, QSizePolicy
from PyQt5.QtCore import Qt
import sys
from ui.filter_element import Filter


class FilterPanel(QWidget):
    def __init__(self, filters_layout_VS, workspace_window):
        super().__init__()
        self.filters_layout_VS = filters_layout_VS
        self.workspace_window = workspace_window
        self.filters = []

    def add_filter(self):
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)

        path_metric_textedit = QTextEdit()
        path_metric_textedit.setReadOnly(True)
        size_policy = path_metric_textedit.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Expanding)
        path_metric_textedit.setSizePolicy(size_policy)

        filter_instance = Filter(path_metric_textedit)

        remove_filter_button = QPushButton("Remove")
        remove_filter_button.clicked.connect(
            lambda: self.remove_filter(filter_instance, filter_widget))

        invert_checkbox = QCheckBox("Inverse")
        invert_checkbox.setChecked(False)
        invert_checkbox.stateChanged.connect(
            lambda state: filter_instance.invert_filter(state))

        choose_metric_button = QPushButton("Choose")
        choose_metric_button.clicked.connect(
            lambda: self.choose_metric(filter_instance))

        filter_layout.addWidget(remove_filter_button)
        filter_layout.addWidget(invert_checkbox)
        filter_layout.addWidget(path_metric_textedit)
        filter_layout.addWidget(choose_metric_button)

        self.filters_layout_VS.addWidget(filter_widget)
        self.filters.append(filter_instance)

    def remove_filter(self, filter_instance, filter_widget):
        self.filters_layout_VS.removeWidget(filter_widget)
        filter_widget.deleteLater()
        self.filters.remove(filter_instance)

    def choose_metric(self, filter_instance):
        self.workspace_window.create_CEM_for_set_metric()
        self.workspace_window.custom_event_menu.set_parameters(
            filter_instance.applay_selected_options, filter_instance.selected_options)
