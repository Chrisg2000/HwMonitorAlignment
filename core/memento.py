from abc import abstractmethod


class Memento:

    @abstractmethod
    def create_memento(self):
        """Returns an object of unspecified type, which represents the data state of self
        """

    @abstractmethod
    def set_memento(self, memento):
        """Set the state of self to the data stored in memento
        """

    @classmethod
    @abstractmethod
    def from_memento(cls, memento):
        """Create an instance of cls from memento state
        """
