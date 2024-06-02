from PyQt5.QtWidgets import QApplication
from ui.data_loader_interface import DataLoaderWindow
import sys

if __name__ == "__main__":
    app = QApplication([])
    window = DataLoaderWindow()
    window.show()

    sys.exit(app.exec())
   
    
    
    canvas_containr_layout



