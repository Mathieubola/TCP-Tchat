import socket

hote = input('ip : ')
port = int(input('Port : '))

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))

print("Connection on {}".format(port))

while 1:
    a=input('>')
    
    socket.send(a.encode('utf-8'))
    
    if a=='Exit':
        print("Close")
        socket.close()
        break
