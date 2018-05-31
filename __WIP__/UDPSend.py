### from https://github.com/JYamihud/Networking_Game_Test

#import bge
import socket
import time

#cont = bge.logic.getCurrentController()
#own = cont.owner

cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

DATA_TO_SEND = "This is some data to send"

cs.sendto(DATA_TO_SEND.encode(), ('0.0.0.0', 4567))

#time.sleep(1)
