from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QPainter, QColor, QLinearGradient, QFont, QFontMetrics
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from hwmonitor.monitors.monitor import Monitor


class MonitorRepresentation(QGraphicsItem):

    def __init__(self, index: str, monitor: Monitor, parent=None):
        super().__init__(parent)

        self.index = index
        self.monitor = monitor

        self.monitor_border_width = 20
        self.monitor_color_gradient_top = QColor(15, 125, 193)
        self.monitor_color_gradient_bottom = QColor(119, 196, 122)
        self.monitor_label_font = QFont('Arial')
        self.monitor_label_font_color = Qt.white

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0,
                      self.monitor.screen_width, self.monitor.screen_height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        # setup border pen
        pen = painter.pen()
        pen.setWidthF(self.monitor_border_width)
        pen.setCapStyle(Qt.FlatCap)
        painter.setPen(pen)

        # create monitor_rect
        rect_monitor = QRectF(0, 0,
                              self.monitor.screen_width, self.monitor.screen_height)

        # Draw gradient in the background
        gradient = QLinearGradient(rect_monitor.topRight(), rect_monitor.bottomLeft())
        gradient.setColorAt(0.0, self.monitor_color_gradient_top)
        gradient.setColorAt(1.0, self.monitor_color_gradient_bottom)
        painter.fillRect(rect_monitor, gradient)

        # draw monitor label
        self.draw_monitor_label(painter, rect_monitor, self.index)

        # draw borders inside monitor_rect
        border_offset = painter.pen().widthF() / 2
        border_rect = rect_monitor.adjusted(border_offset, border_offset, -border_offset, border_offset)
        painter.drawRect(border_rect)

    def draw_monitor_label(self, painter: QPainter, rect: QRectF, txt: str):
        painter.save()
        font = self.monitor_label_font
        font_metrics = QFontMetrics(font, painter.device())

        bounding_rect = font_metrics.boundingRect(rect.toRect(), 0, txt)
        x_factor = rect.width() / bounding_rect.width()
        y_factor = rect.height() / bounding_rect.height()
        factor = min(x_factor, y_factor)

        font.setPointSizeF(font.pointSizeF() * factor)
        painter.setFont(font)
        painter.setPen(self.monitor_label_font_color)

        painter.drawText(rect, Qt.AlignCenter, txt)
        painter.restore()
