import can

class CanConnection(object):
    class CustomListener(can.Listener):  # Subclass Listener to handle messages
        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        def on_message_received(self, msg):
            self.callback(msg)

    def __init__(self, callback, filter, bus):
        self.__bus = bus
        listener = self.CustomListener(callback)  # Use CustomListener instead of can.Listener
        self.__notifier = can.Notifier(self.__bus, [listener], 0)
        self.__listeners = [listener]
        self.addFilter(filter)

    def addCallback(self, callback):
        listener = self.CustomListener(callback)  # Use CustomListener for each callback
        self.__notifier.add_listener(listener)
        self.__listeners.append(listener)

    def addFilter(self, filter):
        filters = self.__bus.filters
        if filters is not None:
            filters.append({"can_id": filter, "can_mask": 0xFFF, "extended": False})
        else:
            filters = [{"can_id": filter, "can_mask": 0xFFF, "extended": False}]
        self.__bus.set_filters(filters)

    def transmit(self, data, reqId, extended=False):
        canMsg = can.Message(arbitration_id=reqId, is_extended_id=extended)
        canMsg.dlc = 8
        canMsg.data = data
        self.__bus.send(canMsg)
