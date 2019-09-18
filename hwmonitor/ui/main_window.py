from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QMainWindow

from hwmonitor.monitors.monitor_model import MonitorModel
from hwmonitor.ui.align.align_controller import AlignController
from hwmonitor.ui.main_window_ui import UiMainWindow


class MainWindow(QMainWindow):

    def __init__(self, monitor_model: MonitorModel):
        super().__init__()
        self.monitor_model = monitor_model
        self.align_controller = AlignController(self.monitor_model)

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
