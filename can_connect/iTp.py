from abc import ABCMeta, abstractmethod


class iTp(object):
    __metaclass__ = ABCMeta

    ##
    # @brief interface method
    @abstractmethod
    def send(self, payload):
        raise NotImplementedError("send function not implemented")

    ##
    # @brief interface method
    @abstractmethod
    def recv(self, timeout_ms):
        raise NotImplementedError("receive function not implemented")

    ##
    # @brief interface method
    @abstractmethod
    def closeConnection(self):
        raise NotImplementedError("closeConnection function not implemented")