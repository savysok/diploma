### https://stackoverflow.com/questions/42415207/send-receive-data-with-python-socket#42415879

import socket, select, sys
from threading import Thread

class ClientThread(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print ("[+] New thread started for "+ip+":"+str(port))


    def run(self):
        while True:
            data = conn.recv(2048)
            if not data: break
            print ("received data:", data)
            #conn.send("::Server:: Data received.\n".encode('utf-8'))

TCP_IP = '0.0.0.0'
TCP_PORT = 4567
BUFFER_SIZE = 1024  # Normally 1024
threads = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 5000))
server_socket.listen(10)

read_sockets, write_sockets, error_sockets = select.select([server_socket], [], [])

while True:
    print ("Waiting for incoming connections...")
    for sock in read_sockets:
        (conn, (ip,port)) = server_socket.accept()
        newthread = ClientThread(ip,port)
        newthread.start()
        threads.append(newthread)

        for t in threads:
            t.join()
            print (t)
