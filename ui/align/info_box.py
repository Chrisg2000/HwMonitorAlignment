from PySide2.QtWidgets import QGraphicsItemGroup, QGraphicsItem, QGraphicsTextItem, QGraphicsRectItem, \
    QGraphicsSceneMouseEvent

from core.monitor import Monitor

TEXT_DEVICE_NAME = "DEVICE NAME:<br><b>{}</b>"
TEXT_MONITOR_NAME = "MONITOR NAME:<br><b>{}</b>"
TEXT_SCREEN_RESOLUTION = "SCREEN RESOLUTION:<br><b>{}x{}</b>"
TEXT_VSCREEN_POSITION = "VIRTUAL SCREEN POSITION:<br><b>({}, {})</b>"
TEXT_MONITOR_ORIENTATION = "ORIENTATION:<br><b>{}</b>"
TEXT_MONITOR_PRIMARY = "IS PRIMARY:<br><b>{}</b>"


class InfoBox(QGraphicsItemGroup):

    def __init__(self, monitor: Monitor):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self.monitor = monitor

        self.device_name = QGraphicsTextItem(self)
        self.device_name.setHtml(
            TEXT_DEVICE_NAME.format(self.monitor.device_name))
        self.monitor_name = QGraphicsTextItem(self)
        self.monitor_name.setHtml(
            TEXT_MONITOR_NAME.format(self.monitor.monitor_name))
        self.screen_resolution = QGraphicsTextItem(self)
        self.screen_resolution.setHtml(
            TEXT_SCREEN_RESOLUTION.format(self.monitor.screen_width, self.monitor.screen_height))
        self.position = QGraphicsTextItem(self)
        self.position.setHtml(
            TEXT_VSCREEN_POSITION.format(self.monitor.position_x, self.monitor.position_y))
        self.orientation = QGraphicsTextItem(self)
        self.orientation.setHtml(
            TEXT_MONITOR_ORIENTATION.format(self.monitor.orientation))
        self.primary = QGraphicsTextItem(self)
        self.primary.setHtml(
            TEXT_MONITOR_PRIMARY.format(self.monitor.primary))

        self.monitor_name.setY(self.device_name.y() + self.device_name.boundingRect().height())
        self.screen_resolution.setY(self.monitor_name.y() + self.monitor_name.boundingRect().height())
        self.position.setY(self.screen_resolution.y() + self.screen_resolution.boundingRect().height())
        self.orientation.setY(self.position.y() + self.position.boundingRect().height())
        self.primary.setY(self.orientation.y() + self.orientation.boundingRect().height())

        self.bounding_rect = QGraphicsRectItem(self.childrenBoundingRect(), self)

        monitor.property_changed.connect(self._property_changed)

    def _property_changed(self, instance, name, value):
        if name is 'device_name':
            self.device_name.setHtml(TEXT_DEVICE_NAME.format(self.monitor.device_name))
        elif name is 'monitor_name':
            self.monitor_name.setHtml(TEXT_MONITOR_NAME.format(self.monitor.monitor_name))
        elif name is 'screen_width' or name is 'screen_height':
            self.screen_resolution.setHtml(
                TEXT_SCREEN_RESOLUTION.format(self.monitor.screen_width, self.monitor.screen_height))
        elif name is 'position_x' or name is 'position_y':
            self.position.setHtml(
                TEXT_VSCREEN_POSITION.format(self.monitor.position_x, self.monitor.position_y))
        elif name is 'orientation':
            self.orientation.setHtml(TEXT_MONITOR_ORIENTATION.format(self.monitor.orientation))
        elif name is 'primary':
            self.primary.setHtml(TEXT_MONITOR_PRIMARY.format(self.monitor.primary))

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        super().mouseMoveEvent(event)
