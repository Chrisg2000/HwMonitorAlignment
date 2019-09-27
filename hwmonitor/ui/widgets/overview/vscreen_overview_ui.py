from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainter, Qt, QColor
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene

from hwmonitor.ui.ui_util import index_from_device_name
from hwmonitor.ui.widgets.overview._monitor_item import MonitorRepresentation


class UiVScreenOverview:

    def __init__(self, view, vscreen):
        """
        :type view: PySide2.QtWidgets.QGraphicsView.QGraphicsView
        :param vscreen: hwmonitor.vscreen.vscreen.VScreen
        """
        self.view = view
        self.vscreen = vscreen

        self.view_margin = 10
        self.background_color = QColor(100, 100, 100)

        view.setInteractive(False)
        view.setStyleSheet('border: 0px;')
        view.setRenderHint(QPainter.Antialiasing)
        view.setCacheMode(QGraphicsView.CacheBackground)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = QGraphicsScene(view)
        self.scene.setBackgroundBrush(self.background_color)
        view.setSceneRect(QRectF(*vscreen.offset, *vscreen.size))

        for monitor in self.vscreen.monitors:
            item = MonitorRepresentation(index_from_device_name(monitor.device_name), monitor)
            item.setPos(monitor.position_x, monitor.position_y)
            self.scene.addItem(item)

        view.setScene(self.scene)

    def _update(self):
        self.resize_scene()

    def resize_scene(self):
        rect = self.scene.itemsBoundingRect()

        view_rect = self.view.viewport().rect().adjusted(self.view_margin, self.view_margin,
                                                         -self.view_margin, -self.view_margin)
        scene_rect = self.view.matrix().mapRect(rect)

        x_ratio = view_rect.width() / scene_rect.width()
        y_ratio = view_rect.height() / scene_rect.height()
        x_ratio = y_ratio = min(x_ratio, y_ratio)

        self.view.scale(x_ratio, y_ratio)
        self.view.centerOn(rect.center())
