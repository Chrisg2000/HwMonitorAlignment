from PySide2.QtGui import Qt, QKeyEvent, QPainter, QShowEvent, QMouseEvent
from PySide2.QtOpenGL import QGLWidget, QGLFormat, QGL
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QToolTip

from ui.align.graphics_widget import GraphicsWidget
from ui.align.grid_item import GridItem
from ui.monitor_info_box import MonitorInfoBox

OPENGL_ACCELERATION = False


class AlignWidget(QGraphicsView):

    def __init__(self, controller):
        """
        :type controller: align.align_controller.AlignController
        """
        super().__init__()
        self.controller = controller
        self.backend = self.controller.backend
        self.resize(*self.backend.get_vscreen_size())
        self.setViewportMargins(0, 0, 0, 0)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scale(1, 1)

        self.graphics_scene = QGraphicsScene(self)
        self.setSceneRect(*self.backend.get_vscreen_normalize_offset(),
                          *self.backend.get_vscreen_size())
        self.setRenderHint(QPainter.Antialiasing)

        if OPENGL_ACCELERATION:
            # noinspection PyUnresolvedReferences
            self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))

        self.setViewportUpdateMode(self.BoundingRectViewportUpdate)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setScene(self.graphics_scene)

        _vscreen = self.backend.get_vscreen_size()
        _offset = self.backend.get_vscreen_normalize_offset()
        for monitor in self.backend.monitor_model:
            left_top_right_bottom = QGraphicsLineItem(monitor.position_x,
                                                      monitor.position_y,
                                                      monitor.position_x + monitor.screen_width,
                                                      monitor.position_y + monitor.screen_height)
            right_top_left_bottom = QGraphicsLineItem(monitor.position_x + monitor.screen_width,
                                                      monitor.position_y,
                                                      monitor.position_x,
                                                      monitor.position_y + monitor.screen_height)
            self.graphics_scene.addItem(left_top_right_bottom)
            self.graphics_scene.addItem(right_top_left_bottom)

            grid = GridItem(monitor, _vscreen, _offset, 100)
            self.graphics_scene.addItem(grid)

        for monitor in self.backend.monitor_model:
            """
            Iterate separately through model to create a layer-effect
            """
            info_box = MonitorInfoBox(monitor)
            proxy_info_box = GraphicsWidget(info_box)
            proxy_info_box.setPos(
                monitor.position_x + monitor.screen_width / 2 - info_box.geometry().width() / 2,
                monitor.position_y + monitor.screen_height / 2 - info_box.geometry().height() / 2
            )
            self.graphics_scene.addItem(proxy_info_box)

    def showEvent(self, event: QShowEvent):
        self.move(*self.backend.get_vscreen_normalize_offset())
        self.resize(*self.backend.get_vscreen_size())
        super().showEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        self.controller.key_pressed(event.key(), self)
        super().keyPressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        QToolTip.showText(event.globalPos(),
                          f"{event.globalPos().x()}, {event.globalPos().y()}",
                          self, self.rect())
        super().mouseMoveEvent(event)
