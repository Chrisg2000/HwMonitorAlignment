from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QMainWindow, QMessageBox

from backend.monitor_backend import BaseMonitorBackend
from ui.align.align_controller import AlignController
from ui.dialogs.settings_changed import DisplaySettingsChanged
from ui.main_window_ui import UiMainWindow


class MainWindow(QMainWindow):

    def __init__(self, backend: BaseMonitorBackend):
        super().__init__()
        self.backend = backend
        self.align_controller = AlignController(self.backend)

        self.ui = UiMainWindow(self, self.backend)
        self.ui.close_button.clicked.connect(self._button_close)
        self.ui.adjust_button.clicked.connect(self._button_adjust)

    def _button_close(self, checked=False):
        self.close()

    def _button_adjust(self, checked=False):
        self.align_controller.start()

    def finalize(self):
        self.align_controller.stop()

    def closeEvent(self, event: QCloseEvent):
        self.finalize()
