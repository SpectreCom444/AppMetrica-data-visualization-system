from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from core.data import DataStorage
from config.constants import SESSION_ID, DEVICE_ID, EVENT_DATETIME
from ui.workspace import WorkspaceWindow
from ui.message import error


class DataLoaderWindow(QMainWindow):
    def __init__(self, data_storage):
        super(DataLoaderWindow, self).__init__()
        loadUi('ui/data-loader.ui', self)
        self.setWindowTitle("Data visualization system")
        self.drop_frame.setAcceptDrops(True)
        self.drop_frame.dragEnterEvent = self.drag_enter_event
        self.drop_frame.dropEvent = self.drop_event
        self.indicator.hide()
        self.data_storage = data_storage

        self.drop_frame.mousePressEvent = self.open_file_dialog
        self.showMaximized()

    def uploading_and_processing(self, path):
        self.indicator.show()
        self.repaint()
        try:
            self.data_storage.load_data(path, self.load_data_callback)
            if EVENT_DATETIME not in self.data_storage.headers:
                error(f"The parameter {
                      EVENT_DATETIME} was not found. Add it when exporting data and try again.")
                return
            self.data_storage.process_events(self.create_events_callback)
            if SESSION_ID not in self.data_storage.headers:
                error(f"The parameter {
                      SESSION_ID} was not found. Add it when exporting data and try again.")
                return
            self.data_storage.process_sessions(self.create_sessions_callback)
            if DEVICE_ID not in self.data_storage.headers:
                error(f"The parameter {
                      DEVICE_ID} was not found. Add it when exporting data and try again.")
                return
            self.data_storage.process_users(self.create_users_callback)
            self.show_workspace_window()
        except FileNotFoundError:
            error("File not found.")
        except Exception as e:
            error(f"An error occurred: {e}")
        finally:
            self.indicator.hide()

    def load_data_callback(self):
        self.load_data_checkbox.setChecked(True)
        self.repaint()

    def create_events_callback(self):
        self.create_events_checkbox.setChecked(True)
        self.repaint()

    def create_sessions_callback(self):
        self.create_sessions_checkbox.setChecked(True)
        self.repaint()

    def create_users_callback(self):
        self.create_users_checkbox.setChecked(True)
        self.repaint()

    def show_workspace_window(self):
        self.window = WorkspaceWindow(self.data_storage)
        self.window.show()
        self.close()

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def drop_event(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.uploading_and_processing(file_path)

    def open_file_dialog(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a file", "", "CSV Files (*.csv)", options=options)
        if file_path:
            self.uploading_and_processing(file_path)
