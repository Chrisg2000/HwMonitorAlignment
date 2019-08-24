from PySide2.QtCore import Qt, QRectF
from PySide2.QtWidgets import QGraphicsWidget, QGraphicsItem, QSizePolicy, QGraphicsLinearLayout, QGraphicsProxyWidget, \
    QWidget


class GraphicsWidget(QGraphicsWidget):

    def __init__(self, widget: QWidget):
        super().__init__()
        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._widget = widget
        self._widget_proxy = QGraphicsProxyWidget()
        self._widget_proxy.setWidget(self._widget)
        self._layout = QGraphicsLinearLayout(Qt.Vertical)
        self._layout.addItem(self._widget_proxy)

        self.setLayout(self._layout)

    def geometry(self) -> QRectF:
        return self._widget.geometry()
