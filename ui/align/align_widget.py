from PySide2.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGridLayout

from core.monitor import Monitor
from ui.align.info_box import InfoBox


class AlignWidget(QWidget):

    def __init__(self, monitor: Monitor):
        super().__init__()
        self.resize(1280, 720)
        self.setLayout(QGridLayout())
        self.layout().setSpacing(0)
        self.layout().setMargin(0)

        self.monitor = monitor

        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)

        self.info_group = InfoBox(self.monitor)
        self.graphics_scene.addItem(self.info_group)

        self.layout().addWidget(self.graphics_view)
