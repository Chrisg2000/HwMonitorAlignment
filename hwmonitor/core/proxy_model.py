from abc import abstractmethod
from typing import Iterator

from hwmonitor.core.model import Model


class ProxyModel(Model):

    def __init__(self, model: Model):
        super().__init__()

        if not isinstance(model, Model):
            raise TypeError(
                "ProxyModel model must be a Model object, not {}".format(
                    type(model)
                ))

        self._model = model
        self._model.item_added.connect(self._item_added)
        self._model.item_removed.connect(self._item_removed)
        self._model.model_reset.connect(self._model_reset)

    @property
    def model(self) -> Model:
        return self._model

    @abstractmethod
    def _item_added(self, item):
        pass

    @abstractmethod
    def _item_removed(self, item):
        pass

    @abstractmethod
    def _model_reset(self):
        pass

    def add(self, item):
        return self._model.add(item)

    def remove(self, item):
        return self._model.remove(item)

    def reset(self):
        return self._model.reset()

    def __len__(self) -> int:
        return self._model.__len__()

    def __iter__(self) -> Iterator:
        return self._model.__iter__()

    def __contains__(self, __x: object) -> bool:
        return __x in self._model
