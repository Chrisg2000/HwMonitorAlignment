from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from monitors.monitor import Monitor


class HLinesPositionItem(QGraphicsItem):

    def __init__(self, monitor: Monitor, spacing):
        super().__init__()
        self._monitor = monitor
        self._spacing = spacing

        self.setPos(*self._monitor.position)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0,
                      self._monitor.screen_width,
                      self._monitor.screen_height)

    # noinspection PyMethodOverriding
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):

        for local_pos_y in range(self._monitor.screen_height):
            global_pos_y = self._monitor.position_y + local_pos_y

            if global_pos_y % self._spacing == 0:
                painter.drawText(0, local_pos_y, f"Global y-position: {global_pos_y}")
