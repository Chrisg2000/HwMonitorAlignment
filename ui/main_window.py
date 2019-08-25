from PySide2.QtGui import QCloseEvent, Qt
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QDialogButtonBox

from align.align_controller import AlignController
from backend.monitor_backend import BaseMonitorBackend
from ui.common.monitor_info_box import MonitorInfoBox
from ui.widgets.monitor_overview import MonitorOverview


class MainWindow(QMainWindow):

    def __init__(self, backend: BaseMonitorBackend):
        super().__init__()
        self.setCentralWidget(QWidget())
        self.setWindowTitle("HwMonitorAlignment")
        self.centralWidget().setLayout(QVBoxLayout())
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)

        self.backend = backend
        self.align_controller = AlignController(self.backend)

        self.monitor_overview_widget = MonitorOverview(self.backend)
        self.centralWidget().layout().addWidget(self.monitor_overview_widget)

        self.sub_widget = QWidget()
        self.sub_layout = QVBoxLayout()
        self.sub_widget.setLayout(self.sub_layout)
        self.centralWidget().layout().addWidget(self.sub_widget)

        self.monitor_info_group = self.setup_monitor_info_group()
        self.sub_layout.addWidget(self.monitor_info_group)

        self.button_group = self.setup_button_group()
        self.sub_layout.addWidget(self.button_group)

    # noinspection PyAttributeOutsideInit
    def setup_monitor_info_group(self):
        _group = QGroupBox("Monitor Setup Information")
        _layout = QHBoxLayout()

        for monitor in self.backend.monitor_model.get_monitor_order():
            info_box = MonitorInfoBox(monitor, _group)
            _layout.addWidget(info_box)

        _group.setLayout(_layout)
        return _group

    def setup_button_group(self):
        _button_box = QDialogButtonBox(Qt.Horizontal)
        _button_box.addButton("Close", QDialogButtonBox.RejectRole).clicked.connect(self._button_close)
        _button_box.addButton("Adjust", QDialogButtonBox.ActionRole).clicked.connect(self._button_adjust)

        return _button_box

    def _button_close(self, checked=False):
        self.close()

    def _button_adjust(self, checked=False):
        self.align_controller.start()

    def finalize(self):
        if self.align_controller.active:
            self.align_controller.stop()

    def closeEvent(self, event: QCloseEvent):
        self.finalize()
