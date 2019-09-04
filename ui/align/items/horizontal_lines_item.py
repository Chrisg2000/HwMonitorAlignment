from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem


class HorizontalLinesItem(QGraphicsItem):

    def __init__(self, model):
        """
        :type model: ui.align.models.align_model.AlignModel
        """
        super().__init__()
        self.model = model
        self.common_model = self.model.common_model

        self.setPos(0, 0)
        self.model.changed("offset").connect(self.update_offset)

        self.common_model.changed("line_thickness").connect(self._update)
        self.common_model.changed("line_spacing").connect(self._update)
        self.common_model.changed("show_horizontal_text").connect(self._update)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0,
                      self.model.monitor.screen_width,
                      self.model.monitor.screen_height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        painter.setPen(QPen(Qt.black, self.common_model.line_thickness))

        monitor = self.model.monitor
        for local_pos_y in range(monitor.screen_height):
            global_pos_y = monitor.position_y + local_pos_y - self.model.offset

            if global_pos_y % self.common_model.line_spacing == 0:
                painter.drawLine(0, local_pos_y, monitor.screen_width, local_pos_y)

                if self.common_model.show_horizontal_text:
                    rect = painter.boundingRect(QRectF(),
                                                Qt.AlignLeft | Qt.AlignHCenter,
                                                f"{global_pos_y}")
                    painter.drawText(
                        10, local_pos_y - rect.height(),
                        rect.width(), rect.height(),
                            Qt.AlignLeft | Qt.AlignHCenter,
                        f"{global_pos_y}"
                    )
                    painter.drawText(
                        monitor.screen_width - rect.width() - 10, local_pos_y - rect.height(),
                        rect.width(), rect.height(),
                        Qt.AlignRight | Qt.AlignHCenter,
                        f"{global_pos_y}"
                    )

    def _update(self, value):
        self.update(self.boundingRect())

    def update_offset(self, offset):
        self.setY(offset)
