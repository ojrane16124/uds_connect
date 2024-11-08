import can
from can.interfaces import pcan, vector, kvaser
from can_connect.CanConnection import CanConnection

class CanConnectionFactory:
    connections = {}
    config = {
        'can': {
            'interface': '',
            'baudrate': '500000'
        },
        'virtual': {
            'interfaceName': 'vcan0'
        },
        'peak': {
            'device': 'PCAN_USBBUS1'
        },
        'vector': {
            'appName': 'CANalyzer',
            'channel': '0'
        },
        'kvaser': {
            'device': '0',
            'channel': '0'
        }
    }

    @staticmethod
    def __call__(callback=None, filter=None, **kwargs):
        CanConnectionFactory.checkKwargs(**kwargs)
        connectionType = CanConnectionFactory.config['can']['interface']

        if connectionType == 'virtual':
            connectionName = CanConnectionFactory.config['virtual']['interfaceName']
            return CanConnectionFactory.getOrCreateConnection(
                connectionName, callback, filter, 
                lambda: can.interface.Bus(connectionName, bustype='virtual')
            )

        elif connectionType == 'peak':
            channel = CanConnectionFactory.config['peak']['device']
            baudrate = CanConnectionFactory.config['can']['baudrate']
            return CanConnectionFactory.getOrCreateConnection(
                channel, callback, filter, 
                lambda: pcan.PcanBus(channel, bitrate=baudrate)
            )

        elif connectionType == 'vector':
            channel = int(CanConnectionFactory.config['vector']['channel'])
            app_name = CanConnectionFactory.config['vector']['appName']
            baudrate = int(CanConnectionFactory.config['can']['baudrate'])
            connectionKey = f"{app_name}_{channel}"
            return CanConnectionFactory.getOrCreateConnection(
                connectionKey, callback, filter, 
                lambda: vector.VectorBus(channel, app_name=app_name, data_bitrate=baudrate)
            )

        elif connectionType == 'kvaser':
            channel = CanConnectionFactory.config['kvaser']['channel']
            baudrate = CanConnectionFactory.config['can']['baudrate']
            return CanConnectionFactory.getOrCreateConnection(
                channel, callback, filter, 
                lambda: kvaser.KvaserBus(channel, bitrate=int(baudrate))
            )

        else:
            raise ValueError(f"Unsupported connection type: {connectionType}")

    @staticmethod
    def getOrCreateConnection(key, callback, filter, createConnection):
        if key not in CanConnectionFactory.connections:
            CanConnectionFactory.connections[key] = CanConnection(callback, filter, createConnection())
        else:
            CanConnectionFactory.connections[key].addCallback(callback)
            CanConnectionFactory.connections[key].addFilter(filter)
        return CanConnectionFactory.connections[key]

    @staticmethod
    def checkKwargs(**kwargs):
        configMap = {
            'interface': ('can', 'interface'),
            'baudrate': ('can', 'baudrate'),
            'device': [('peak', 'device'), ('kvaser', 'device')],
            'appName': ('vector', 'appName'),
            'channel': [('vector', 'channel'), ('kvaser', 'channel')]
        }

        for key, paths in configMap.items():
            if key in kwargs:
                value = str(kwargs[key])
                if isinstance(paths, list):
                    for pathPair in paths:
                        CanConnectionFactory.config[pathPair[0]][pathPair[1]] = value
                else:
                    CanConnectionFactory.config[paths[0]][paths[1]] = value
