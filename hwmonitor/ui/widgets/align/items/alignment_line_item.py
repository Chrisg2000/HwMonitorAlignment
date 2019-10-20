from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem

from hwmonitor.ui.widgets.align.models.align_model import AlignModel


class AlignmentLineItem(QGraphicsItem):

    def __init__(self, model: AlignModel):
        super().__init__()
        self.model = model

        self.setPos(0, 0)
        self.model.monitor.changed("position_x").connect(self._update)
        self.model.monitor.changed("position_y").connect(self._update)

        self._update_graph()
        self.model.common_model.changed("line_thickness").connect(self._update)
        self.model.common_model.changed("line_spacing").connect(self._update)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0,
                      self.model.monitor.screen_width,
                      self.model.monitor.screen_height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        painter.setPen(QPen(Qt.black, self.model.common_model.line_thickness))

        monitor = self.model.monitor

        painter.drawLine(0, self._glob_h_over_mid_line,
                         self._h_line_length, self._glob_h_over_mid_line)
        painter.drawLine(monitor.screen_width, self._glob_h_over_mid_line,
                         monitor.screen_width - self._h_line_length, self._glob_h_over_mid_line)

        painter.drawLine(0, self._glob_h_mid_line,
                         monitor.screen_width, self._glob_h_mid_line)
        painter.drawLine(0, self._glob_h_under_mid_line,
                         self._h_line_length, self._glob_h_under_mid_line)
        painter.drawLine(monitor.screen_width, self._glob_h_under_mid_line,
                         monitor.screen_width - self._h_line_length, self._glob_h_under_mid_line)

    def _update_graph(self):
        primary_monitor = self.model.vscreen.primary_monitor
        monitor = self.model.monitor

        h_mid_line = primary_monitor.screen_height / 2
        h_over_mid_line = h_mid_line - self.model.common_model.line_spacing
        h_under_mid_line = h_mid_line + self.model.common_model.line_spacing

        self._h_line_length = monitor.screen_width / 5
        self._glob_h_over_mid_line = h_over_mid_line - monitor.position_y
        self._glob_h_mid_line = h_mid_line - monitor.position_y
        self._glob_h_under_mid_line = h_under_mid_line - monitor.position_y

    def _update(self, value):
        self.update(self.boundingRect())

    def update(self, rect: QRectF = None):
        self._update_graph()
        super().update(rect)
