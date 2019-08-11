from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from backend.monitor_backend import BaseMonitorBackend
from ui.align.align_widget import AlignWidget
from ui.widgets.monitor_overview import MonitorOverview


class MainWindow(QMainWindow):

    def __init__(self, backend: BaseMonitorBackend):
        super().__init__()
        # self.resize(1280, 720)
        self.resize(492, 219)
        # self.setMinimumSize(1280, 720)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QVBoxLayout())
        # self.centralWidget().layout().setContentsMargins(5, 5, 5, 5)
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)

        self.backend = backend

        widget = MonitorOverview(self.backend)
        self.centralWidget().layout().addWidget(widget)

        self.test = AlignWidget(self.backend.monitor_model.get(0))
        self.test.show()
