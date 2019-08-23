from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from core.monitor import Monitor


class GridItem(QGraphicsItem):

    def __init__(self, monitor: Monitor, vscreen, offset, spacing):
        super().__init__()

        self._monitor = monitor

        self.setPos(*self._monitor.position)

        self._vscreen_width, self._vscreen_height = vscreen
        self._vscreen_offset_x, self._vscreen_offset_y = offset
        self._spacing = spacing

        self._line_thickness = 3

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0,
                      self._monitor.screen_width,
                      self._monitor.screen_height)

    # noinspection PyMethodOverriding
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        painter.setPen(QPen(Qt.black, self._line_thickness))

        for local_pos_y in range(self._monitor.screen_height):
            global_pos_y = self._monitor.position_y + local_pos_y

            if global_pos_y % self._spacing == 0:
                painter.drawText(0, local_pos_y, f"{local_pos_y}, {global_pos_y}")
                painter.drawLine(0, local_pos_y, self._monitor.screen_width, local_pos_y)
