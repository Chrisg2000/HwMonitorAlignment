from PySide2.QtGui import QResizeEvent, Qt, QKeyEvent
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

        self.graphics_scene = QGraphicsScene(self)

        self.info_box = InfoBox(self.monitor)
        self.graphics_scene.addItem(self.info_box)

        self.graphics_scene.addRect(0, 0, 100, 100)

        self.graphics_view = QGraphicsView(self.graphics_scene, self)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout().addWidget(self.graphics_view)

    def resizeEvent(self, event: QResizeEvent):
        self.graphics_scene.setSceneRect(0, 0,
                                         event.size().width(), event.size().height())

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Z:
            self.monitor.monitor_name = 'Test monitor_name extra long'
        super().keyPressEvent(event)
