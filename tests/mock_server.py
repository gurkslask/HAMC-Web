#!/usr/bin/python3

import asyncio
import pickle

__author__ = 'alexander'

'''mockserver'''

mockvalues = {'test1': 42,
              'test2': 2,
              'test3': 64}

class EchoServerClientProtocol(asyncio.Protocol):
    def __init__(self, hdata):
        # data_func method
        self.HAMC_data = hdata

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = pickle.loads(data)
        for read_or_write in message:
            if read_or_write is 'w':
                for value_to_write in message[read_or_write]:
                    #value_to_write = value_to_write.split(',')

                    self.HAMC_data[value_to_write[0]] = value_to_write[1]
                self.transport.write(pickle.dumps({'Done': 1}))
            elif read_or_write is 'r':
                data_to_send = {}
                for value_to_read in message[read_or_write]:
                    try:
                        data_to_send[value_to_read] = self.HAMC_data[value_to_read]
                    except KeyError:
                        data_to_send[value_to_read] = 'Keyerror'
                self.transport.write(pickle.dumps(data_to_send))

        print('Close the client socket')
        self.transport.close()

    def data_send(self, data):
        self.transport.write(data)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        lambda: EchoServerClientProtocol(mockvalues),
        '0.0.0.0',
        5008
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
