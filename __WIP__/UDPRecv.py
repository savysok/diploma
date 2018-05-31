### from https://github.com/JYamihud/Networking_Game_Test

import socket
#from mathutils import *
#from math import *
UDP_IP = "0.0.0.0"
UDP_PORT = 4567

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

sock.settimeout(1.0)
data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
print( str( data ) )
