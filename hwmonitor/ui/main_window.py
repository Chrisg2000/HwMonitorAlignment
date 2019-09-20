from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QMainWindow

from hwmonitor.monitors.vscreen_adapter import VScreenAdapter
from hwmonitor.ui.align.align_controller import AlignController
from hwmonitor.ui.main_window_ui import UiMainWindow


class MainWindow(QMainWindow):

    def __init__(self, monitor_model_adapter: VScreenAdapter):
        super().__init__()
        self.monitor_model_adapter = monitor_model_adapter
        self.align_controller = AlignController(self.monitor_model_adapter)

        self.ui = UiMainWindow(self, self.monitor_model_adapter)
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
