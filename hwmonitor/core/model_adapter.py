from hwmonitor.core.model import Model
from hwmonitor.core.proxy_model import ProxyModel


class ModelAdapter(ProxyModel):

    def __init__(self, model: Model):
        super().__init__(model)

    def _item_added(self, item):
        self.item_added.emit(item)

    def _item_removed(self, item):
        self.item_removed.emit(item)

    def _model_reset(self):
        self.model_reset.emit()
