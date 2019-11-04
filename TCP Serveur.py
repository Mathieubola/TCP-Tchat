import socket

print('ip : ' + str(socket.gethostbyname(socket.gethostname())))

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', int(input('Port : '))))

socket.listen(5)
client, address = socket.accept()
print('{} connected'.format(address))

while 1:
        response = client.recv(255).decode('utf-8')
        if response == 'Exit':
                print("Close")
                client.close()
                socket.close()
                break
        elif response != '':
                print(response)
