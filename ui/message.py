from PyQt5.QtWidgets import QMessageBox
import traceback


def show_message_box(message_type: QMessageBox.Icon, title: str, text: str, buttons: QMessageBox.StandardButtons = QMessageBox.Ok) -> int:
    msg_box = QMessageBox()
    msg_box.setIcon(message_type)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(buttons)
    return msg_box.exec()


def warning_dialog(text: str) -> bool:
    result = show_message_box(
        QMessageBox.Warning, "Warning", text, QMessageBox.Ok | QMessageBox.Cancel)
    return result == QMessageBox.Ok


def warning(text: str) -> None:
    show_message_box(QMessageBox.Warning, "Warning", text)


def error(text: str) -> None:
    show_message_box(QMessageBox.Critical, "Error", str(text))
    traceback.print_exc()
