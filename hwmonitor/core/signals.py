import inspect
import logging
import traceback
import weakref
from enum import Enum
from threading import RLock
from types import MethodType, BuiltinMethodType

from PySide2.QtCore import QObject, QEvent
from PySide2.QtWidgets import QApplication

__all__ = ['Signal', 'Connection']


def slot_id(slot_callable):
    """Return the id of the given slot_callable.

    This function is able to produce unique id(s) even for bounded methods, and
    builtin-methods using a combination of the function id and the object id.
    """
    if isinstance(slot_callable, MethodType):
        return id(slot_callable.__func__), id(slot_callable.__self__)
    elif isinstance(slot_callable, BuiltinMethodType):
        return id(slot_callable), id(slot_callable.__self__)
    else:
        return id(slot_callable)


def weak_call_proxy(weakref):
    def proxy(*args, **kwargs):
        if weakref() is not None:
            weakref()(*args, **kwargs)

    return proxy


class Slot:
    """Synchronous slot."""

    def __init__(self, slot_callable, callback=None):
        if isinstance(slot_callable, MethodType):
            self._reference = weakref.WeakMethod(slot_callable, self._expired)
        elif callable(slot_callable):
            self._reference = weakref.ref(slot_callable, self._expired)
        else:
            raise TypeError('slot must be callable')

        self._callback = callback
        self._slot_id = slot_id(slot_callable)
        self._no_args = len(inspect.signature(slot_callable).parameters) == 0

    def call(self, *args, **kwargs):
        """Call the callable object within the given parameters."""
        try:
            if self.is_alive():
                if self._no_args:
                    self._reference()()
                else:
                    self._reference()(*args, **kwargs)
        except Exception:
            logging.error(traceback.format_exc())

    def is_alive(self):
        return self._reference() is not None

    def _expired(self, reference):
        self._callback(self._slot_id)


class QtSlot(Slot):
    """Qt direct slot, execute the call inside the qt-event-loop."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a QObject and move it to mainloop thread
        self._invoker = QObject()
        self._invoker.moveToThread(QApplication.instance().thread())
        self._invoker.customEvent = self._custom_event

    def call(self, *args, **kwargs):
        QApplication.instance().sendEvent(self._invoker,
                                          self._event(*args, **kwargs))

    def _event(self, *args, **kwargs):
        return QSlotEvent(self._reference, *args, **kwargs)

    def _custom_event(self, event):
        super().call(*event.args, **event.kwargs)


class QtQueuedSlot(QtSlot):
    """Qt queued (safe) slot, execute the call inside the qt-event-loop."""

    def call(self, *args, **kwargs):
        QApplication.instance().postEvent(self._invoker,
                                          self._event(*args, **kwargs))


class QSlotEvent(QEvent):
    EVENT_TYPE = QEvent.Type(QEvent.registerEventType())

    def __init__(self, reference, *args, **kwargs):
        QEvent.__init__(self, QSlotEvent.EVENT_TYPE)
        self.reference = reference
        self.args = args
        self.kwargs = kwargs


class Connection(Enum):
    """Available connection modes."""
    Direct = Slot
    QtDirect = QtSlot
    QtQueued = QtQueuedSlot

    def new_slot(self, slot_callable, callback=None):
        return self.value(slot_callable, callback)


class Signal:
    """Signal/slot implementation.

    A signal object can be connected/disconnected to a callable object (slot),
    the connection can have different modes, any mode define the way a slot
    is called, those are defined in :class:`Connection`.

    .. note::
        * Any slot can be connected only once to a specific signal,
          if reconnected, the previous connection is overridden.
        * Internally, weak-references are used, so disconnection is not needed
          before delete a slot-owner object.
        * Signals with "arguments" can be connected to slot without arguments

    .. warning::
        Because of weakrefs, connecting like the following can't work:

        signal.connect(lambda: some_operation))
        signal.connect(NewObject().my_method)
        signal.connect(something_not_referenced)
    """

    def __init__(self):
        self.__slots = {}
        self.__lock = RLock()

    def connect(self, slot_callable, mode=Connection.Direct):
        """Connect the given slot, if not already connected.

        :param slot_callable: The slot (a python callable) to be connected
        :param mode: Connection mode
        :type mode: Connection
        :raise ValueError: if mode not in Connection enum
        """
        if mode not in Connection:
            raise ValueError('invalid mode value: {0}'.format(mode))

        with self.__lock:
            # Create a new Slot object, use a weakref for the callback
            # to avoid cyclic references.
            callback = weak_call_proxy(weakref.WeakMethod(self._remove_slot))
            self.__slots[slot_id(slot_callable)] = mode.new_slot(slot_callable,
                                                                 callback)

    def disconnect(self, slot=None):
        """Disconnect the given slot, or all if no slot is specified.

        :param slot: The slot to be disconnected or None
        """
        if slot is not None:
            self._remove_slot(slot_id(slot))
        else:
            with self.__lock:
                self.__slots.clear()

    # noinspection PyBroadException
    def emit(self, *args, **kwargs):
        """Emit the signal within the given arguments"""
        with self.__lock:
            for slot in self.__slots.values():
                try:
                    slot.call(*args, **kwargs)
                except Exception:
                    traceback.print_exc()

    def _remove_slot(self, id_):
        with self.__lock:
            self.__slots.pop(id_, None)
