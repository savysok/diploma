### https://stackoverflow.com/questions/42415207/send-receive-data-with-python-socket#42415879

import socket, select, sys, time

TCP_IP = '0.0.0.0'
TCP_PORT = 4567

BUFFER_SIZE = 1024
MESSAGE = "Message sent..\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, 5000))
s.sendto(MESSAGE.encode('utf-8'),(TCP_IP, TCP_PORT))
socket_list = [sys.stdin, s]

while 1:

    read_sockets = select.select(socket_list, [], [])

    for sock in read_sockets:
        # incoming message from remote server
        if sock == s:
            data = sock.recv(4096)
            if not data:
                print('\nDisconnected from server')
                sys.exit()
            else:
                sys.stdout.write("\n")
                message = data.decode()
                sys.stdout.write(message)
                sys.stdout.write('<Me> ')
                sys.stdout.flush()

        else:
            msg = sys.stdin.readline()
            s.send(bytes(msg))
            sys.stdout.write('<Me> ')
            sys.stdout.flush()
