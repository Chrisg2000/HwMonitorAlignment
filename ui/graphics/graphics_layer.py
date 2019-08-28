from PySide2.QtWidgets import QGraphicsItem


class GraphicsLayer:

    def __init__(self, visible=True):
        self.__items = {}
        self.__visible = visible

    def add_to_layer(self, item: QGraphicsItem, key=None):
        """Add item to this layer.
        A added item will only by visible if this layer visibility is set.
        Key Argument if for creating (key, item) pairs, which can be requested
        by layer[key].
        """
        key = key or id(item)
        self.__items[key] = item
        item.setVisible(self.__visible)

    def remove_from_layer(self, key=None, item: QGraphicsItem = None):
        """Remove item from this layer.
        Removing a item from an invisible layer will make it visible again.
        """
        key = key or id(item)
        item = self.__items.pop(key)
        item.setVisible(True)

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value):
        self.set_visible(value)

    def set_visible(self, visible: bool):
        """Change visibility of items"""
        self.__visible = visible
        for item in self.__items.values():
            item.setVisible(visible)

    def __getitem__(self, key):
        return self.__items[key]
