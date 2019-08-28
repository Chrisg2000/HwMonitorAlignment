from PySide2.QtGui import Qt, QKeyEvent, QPainter, QShowEvent, QMouseEvent
from PySide2.QtOpenGL import QGLWidget, QGLFormat, QGL
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QToolTip

from align import AdjustDirection
from ui.align.hlines_align_item import HLinesAlignItem
from ui.align.hlines_position_item import HLinesPositionItem
from ui.common.control_box import ControlBox
from ui.common.monitor_info_box import MonitorInfoBox
from ui.graphics.graphics_layer import GraphicsLayer
from ui.graphics.graphics_widget import GraphicsWidget

OPENGL_ACCELERATION = False


class AlignWidget(QGraphicsView):

    def __init__(self, controller, parent=None):
        """
        :type controller: align.align_controller.AlignController
        """
        super().__init__(parent)
        self.scale(1, 1)
        self.controller = controller
        self.backend = self.controller.backend
        self.resize(*self.backend.get_vscreen_size())
        self.setViewportMargins(0, 0, 0, 0)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.graphics_scene = QGraphicsScene(self)
        self.setSceneRect(*self.backend.get_vscreen_normalize_offset(),
                          *self.backend.get_vscreen_size())
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(self.MinimalViewportUpdate)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setScene(self.graphics_scene)

        if OPENGL_ACCELERATION:
            self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))

        self.controller.property_changed.connect(self._controller_property_changed)

        self._selected_widget: MonitorInfoBox = None

        self.dlines_layer = GraphicsLayer(visible=self.controller.show_diagonal_lines)
        self.hlines_layer = GraphicsLayer(visible=self.controller.show_alignment_lines)
        self.hlines_position_layer = GraphicsLayer(visible=self.controller.show_line_positions)
        self.info_box_layer = GraphicsLayer(visible=self.controller.show_info_box)

        self.setup_monitor()

    #
    # Adjustment logic
    #

    def adjust_monitor(self, monitor, direction: AdjustDirection):
        print(self.hlines_layer[monitor])

    #
    # Setup UI-Stuff
    #
    def setup_monitor(self):
        for monitor in self.backend.monitor_model:
            self.create_diagonal_lines(monitor)
            self.create_hlines(monitor)
            self.create_hlines_position(monitor)
            self.create_box(monitor)

    def create_box(self, monitor):
        info_box = self.create_info_box(monitor)
        if monitor.primary:
            control_box = self.create_control_box()
            control_box.setPos(
                info_box.x() + info_box.geometry().width() / 2,
                info_box.y() + info_box.geometry().height() / 2 - control_box.geometry().height() / 2
            )
            info_box.setPos(
                info_box.x() - info_box.geometry().width() / 2,
                info_box.y()
            )

    def create_control_box(self):
        control_box = ControlBox(self.controller)
        proxy_control_box = GraphicsWidget(control_box)
        proxy_control_box.setZValue(100)
        self.graphics_scene.addItem(proxy_control_box)
        return proxy_control_box

    def create_info_box(self, monitor):
        info_box = MonitorInfoBox(monitor)
        proxy_info_box = GraphicsWidget(info_box)
        proxy_info_box.setPos(
            monitor.position_x + monitor.screen_width / 2 - info_box.geometry().width() / 2,
            monitor.position_y + monitor.screen_height / 2 - info_box.geometry().height() / 2
        )
        proxy_info_box.setZValue(99)
        self.graphics_scene.addItem(proxy_info_box)

        self.info_box_layer.add_to_layer(proxy_info_box, key=monitor)
        return proxy_info_box

    def create_diagonal_lines(self, monitor):
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

        self.dlines_layer.add_to_layer(left_top_right_bottom, key=monitor)
        self.dlines_layer.add_to_layer(right_top_left_bottom, key=monitor)
        return left_top_right_bottom, right_top_left_bottom

    def create_hlines(self, monitor):
        grid = HLinesAlignItem(monitor, 100)
        self.graphics_scene.addItem(grid)

        self.hlines_layer.add_to_layer(grid, key=monitor)
        return grid

    def create_hlines_position(self, monitor):
        hlines_positions = HLinesPositionItem(monitor, 100)
        self.graphics_scene.addItem(hlines_positions)

        self.hlines_position_layer.add_to_layer(hlines_positions, key=monitor)
        return hlines_positions

    def _controller_property_changed(self, instance, name, value):
        if name == 'show_diagonal_lines':
            self.dlines_layer.set_visible(value)
        elif name == 'show_alignment_lines':
            self.hlines_layer.set_visible(value)
        elif name == 'show_info_box':
            self.info_box_layer.set_visible(value)
        elif name == 'show_line_positions':
            self.hlines_position_layer.set_visible(value)
        elif name == 'show_cursor_position':
            self.setMouseTracking(value)
        elif name == 'selected_monitor':
            if self._selected_widget:
                self._selected_widget.selected = False
            self._selected_widget = self.info_box_layer[value].widget
            self._selected_widget.selected = True

    #
    # Controller pass through's
    #
    def showEvent(self, event: QShowEvent):
        self.move(*self.backend.get_vscreen_normalize_offset())
        self.resize(*self.backend.get_vscreen_size())
        super().showEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        self.controller.key_pressed(event.key())
        super().keyPressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.controller.show_cursor_position:
            QToolTip.showText(event.globalPos(),
                              f"{event.globalPos().x()}, {event.globalPos().y()}",
                              self, self.rect())
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        self.controller.mouse_pressed(event)
        super().mousePressEvent(event)
