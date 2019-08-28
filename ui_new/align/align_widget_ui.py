from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem

from ui_new.graphics.graphics_layer import GraphicsLayer


class UiAlignWidget:

    def __init__(self, view, model, monitor):
        """UI for AlignWidgets

        :type view: PySide2.QtWidgets.QGraphicsView.QGraphicsView
        :type model: ui_new.align.align_widget_model.AlignWidgetModel
        :type monitor: monitors.monitor.Monitor
        """
        self.view = view
        self.model = model
        self.monitor = monitor

        view.scale(1, 1)
        view.resize(*self.model.vscreen_size)
        view.setWindowFlags(Qt.Dialog)
        view.setViewportMargins(0, 0, 0, 0)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        view.setRenderHint(QPainter.Antialiasing)
        view.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        view.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)

        self.graphics_scene = QGraphicsScene(view)
        view.setSceneRect(QRectF(0, 0, self.monitor.screen_width, self.monitor.screen_height))

        self.diagonal_lines_layer = GraphicsLayer(visible=True, level=1)
        self.horizontal_lines_layer = GraphicsLayer(visible=self.model.show_horizontal_lines, level=2)
        self.info_box_layer = GraphicsLayer(visible=self.model.show_info_box, level=3)

        self.create_diagonal_lines()

        view.setScene(self.graphics_scene)

    def create_diagonal_lines(self):
        left_top_right_bottom = QGraphicsLineItem(0, 0,
                                                  self.monitor.screen_width, self.monitor.screen_height)
        right_top_left_bottom = QGraphicsLineItem(self.monitor.screen_width, 0,
                                                  0, self.monitor.screen_height)

        self.diagonal_lines_layer.add_to_layer(left_top_right_bottom)
        self.diagonal_lines_layer.add_to_layer(right_top_left_bottom)

        self.graphics_scene.addItem(left_top_right_bottom)
        self.graphics_scene.addItem(right_top_left_bottom)
