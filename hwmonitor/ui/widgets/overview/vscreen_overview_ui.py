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

        for monitor in self.vscreen.monitors:
            item = MonitorRepresentation(index_from_device_name(monitor.device_name), monitor)
            item.update_position()
            self.scene.addItem(item)

        view.setScene(self.scene)

    def update_position(self):
        for item in self.scene.items():
            item.update_position()

    def resize_scene(self):
        """Resize the scene to fit inside the available space of the viewport with an given margin.

        Update the scene rect, since it probably changes when changing the layout.
        """
        rect = self.scene.itemsBoundingRect()
        self.view.setSceneRect(rect)

        view_rect = self.view.viewport().rect().adjusted(self.view_margin, self.view_margin,
                                                         -self.view_margin, -self.view_margin)
        scene_rect = self.view.matrix().mapRect(rect)

        x_factor = view_rect.width() / scene_rect.width()
        y_factor = view_rect.height() / scene_rect.height()
        factor = min(x_factor, y_factor)

        self.view.scale(factor, factor)
        self.view.centerOn(rect.center())
