from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem


class HorizontalLinesItem(QGraphicsItem):

    def __init__(self, model):
        """
        :type model: ui_new.align.models.align_model.AlignModel
        """
        super().__init__()
        self.model = model
        self.common_model = self.model.common_model
        self.line_spacing = self.common_model.line_spacing
        self.line_thickness = self.common_model.line_thickness

        self.setPos(0, 0)
        self.model.monitor.changed("position_y").connect(self.setY)

        self.common_model.changed("line_thickness").connect(self.set_line_thickness)
        self.common_model.changed("line_spacing").connect(self.set_line_spacing)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0,
                      self.model.monitor.screen_width,
                      self.model.monitor.screen_height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        painter.setPen(QPen(Qt.black, self.line_thickness))

        for local_pos_y in range(self.model.monitor.screen_height):
            global_pos_y = self.model.top_left[1] + local_pos_y

            if global_pos_y % self.line_spacing == 0:
                painter.drawLine(0, local_pos_y, self.model.monitor.screen_width, local_pos_y)

    def set_line_thickness(self, value):
        self.line_thickness = value
        self.update(self.boundingRect())

    def set_line_spacing(self, value):
        self.line_spacing = value
        self.update(self.boundingRect())

    def setY(self, y: float):
        pos = self.pos()
        pos.setY(y)
        self.setPos(pos)
        self.update(self.boundingRect())
