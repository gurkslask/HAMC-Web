
import pickle
import socket
import sys

__author__ = 'alexander'


# Echo client program
def call_server(message):
    '''
    This function takes a dict and returns a dict. Example:
    {'r': ['self.VS1_GT1.temp',
                     'self.VS1_GT2.temp',
                     'self.VS1_GT3.temp',
                     'self.SUN_GT2.temp',
                     'self.Setpoint_VS1',
                     'self.VS1_SV1_SP_Down',
                     'self.Komp.DictVarden',
                     'self.ThreeDayTemp'
    ]}
    or if you want to write:
    {'w': [['self.Setpoint_Vs1', 20.0]]
    }
    and returns a dict where the variable names is the keys
    paired with the values
    '''
    message = pickle.dumps(message)
    HOST = '192.168.1.8'    # The remote host
    PORT = 5004              # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(message)
    data = s.recv(1024)
    s.close()
    return pickle.loads(data)
    # print 'Received', repr(data)

if __name__ == '__main__':
    command_str = sys.argv[1].replace('\n', '').split(':')
    print(command_str)
    command = {command_str[0]: [command_str[1]]}
    print(call_server(command))
