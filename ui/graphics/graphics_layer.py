from PySide2.QtWidgets import QGraphicsItem


class GraphicsLayer:

    def __init__(self, visible=True):
        self.__items = []
        self.__visible = visible

    def add_to_layer(self, item: QGraphicsItem):
        self.__items.append(item)
        item.setVisible(self.__visible)

    def remove_from_layer(self, item: QGraphicsItem):
        self.__items.remove(item)
        item.setVisible(True)

    def set_visible(self, visible: bool):
        self.__visible = visible
        for item in self.__items:
            item.setVisible(visible)
