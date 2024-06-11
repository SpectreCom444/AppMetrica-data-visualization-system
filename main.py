from PyQt5.QtWidgets import QApplication
from ui.data_loader_interface import DataLoaderWindow
from core.data import DataStorage
import sys

if __name__ == "__main__":
    app = QApplication([])
    data_storage = DataStorage()
    window = DataLoaderWindow(data_storage)
    window.show()

    sys.exit(app.exec())
