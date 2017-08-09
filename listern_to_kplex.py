#client example
import socket
import ais
from display_basic import print_vessel_details
from display_basic import clear_terminal
from modules.vessel import Vessel
from modules.vessel import FileAccessWrapper
import modules.navigation as nav
import datetime
import time
import pickle

polar_file = FileAccessWrapper('/home/kelvin/github/Sailing-Navigation/modules/process/inter_polar.csv')
vessel = Vessel(polar_file)
connected =0
clear_terminal()

while connected == 0:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.129.1', 10110))
        connected = 1
    except:
        a =1

while True:
    try:
        data = client_socket.recv(512)
        if ( data == 'q' or data == 'Q'):
            client_socket.close()
        else:
            for line in data.split('\n'):
                vessel.NMEAInput(line)
                print_vessel_details((5,0),vessel)
    except KeyboardInterrupt:
        pass
        break

    except:
        a = 1

