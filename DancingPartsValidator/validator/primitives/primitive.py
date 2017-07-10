from abc import ABCMeta, abstractmethod

class Primitive:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getVolume(self):
        pass

    @abstractmethod
    def getSignature(self):
        pass

    @abstractmethod
    def getName(self):
        pass
