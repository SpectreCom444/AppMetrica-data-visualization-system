from typing import Optional
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QFrame
from PyQt5.uic import loadUi
from PyQt5.QtCore import QEvent
from core.data import DataStorage
from config.constants import SESSION_ID, DEVICE_ID, EVENT_DATETIME
from ui.workspace import WorkspaceWindow
from ui.message import error


class DataLoaderWindow(QMainWindow):
    def __init__(self, data_storage: DataStorage) -> None:
        super(DataLoaderWindow, self).__init__()
        loadUi('ui/data-loader.ui', self)
        self.setWindowTitle("Data visualization system")
        self.drop_frame.setAcceptDrops(True)
        self.drop_frame.dragEnterEvent = self._drag_enter_event
        self.drop_frame.dropEvent = self._drop_event
        self.indicator.hide()
        self.data_storage = data_storage

        self.drop_frame.mousePressEvent = self._open_file_dialog
        self.showMaximized()

    def _uploading_and_processing(self, path: str) -> None:
        self.indicator.show()
        self.repaint()
        try:
            self.data_storage.load_data(path, self._load_data_callback)
            if EVENT_DATETIME not in self.data_storage.headers:
                error(f"The parameter {
                      EVENT_DATETIME} was not found. Add it when exporting data and try again.")
                return
            self.data_storage.process_events(self._create_events_callback)
            if SESSION_ID not in self.data_storage.headers:
                error(f"The parameter {
                      SESSION_ID} was not found. Add it when exporting data and try again.")
                return
            self.data_storage.process_sessions(self._create_sessions_callback)
            if DEVICE_ID not in self.data_storage.headers:
                error(f"The parameter {
                      DEVICE_ID} was not found. Add it when exporting data and try again.")
                return
            self.data_storage.process_users(self._create_users_callback)
            self._show_workspace_window()
        except FileNotFoundError:
            error("File not found.")
        except Exception as e:
            error(f"An error occurred: {e}")
        finally:
            self.indicator.hide()

    def _load_data_callback(self) -> None:
        self.load_data_checkbox.setChecked(True)
        self.repaint()

    def _create_events_callback(self) -> None:
        self.create_events_checkbox.setChecked(True)
        self.repaint()

    def _create_sessions_callback(self) -> None:
        self.create_sessions_checkbox.setChecked(True)
        self.repaint()

    def _create_users_callback(self) -> None:
        self.create_users_checkbox.setChecked(True)
        self.repaint()

    def _show_workspace_window(self) -> None:
        self._window = WorkspaceWindow(self.data_storage)
        self._window.show()
        self.close()

    def _drag_enter_event(self, event: QEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def _drop_event(self, event: QEvent) -> None:
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self._uploading_and_processing(file_path)

    def _open_file_dialog(self, event: QEvent) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a file", "", "CSV Files (*.csv)", options=options)
        if file_path:
            self._uploading_and_processing(file_path)
