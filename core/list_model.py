from typing import Iterator

from core.model import Model


class ListModel(Model):

    def __init__(self):
        super().__init__()
        self.__list = []

    def item(self, index):
        return self.__list[index]

    def insert(self, index, item):
        self.__list.insert(index, item)
        self.item_added.emit(index, item)

    def pop(self, index):
        item = self.__list.pop(index)
        self.item_removed.emit(index, item)
        return item

    def add(self, item):
        self.insert(len(self.__list), item)

    def remove(self, item):
        index = self.__list.index(item)
        self.pop(index)

    def reset(self):
        self.__list.clear()
        self.model_reset.emit()

    def get(self, index, default=None):
        try:
            return self.__list[index]
        except IndexError:
            return default

    def empty(self):
        return not self.__list

    def __len__(self) -> int:
        return len(self.__list)

    def __iter__(self) -> Iterator:
        return self.__list.__iter__()

    def __contains__(self, x: object) -> bool:
        return self.__list.__contains__(x)
