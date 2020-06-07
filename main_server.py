import socket

ip='127.0.0.1'
mainip='127.0.0.9'
mainport=4567
spam_server='129.0.0.1'
spam_port=6172
port=1234
header=10
type='utf-8'

main_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.bind((mainip,mainport))
sockets_list=[main_socket]
main_socket.listen()

def add_header(message):
    message=f'{len(message):<{header}}'+message
    return bytes(message,type)

def recieve_message(client_socket):
    message_length=int(client_socket.recv(header).decode(type))
    message=client_socket.recv(message_length).decode(type)
    return message

while True:
   client_socket,client_address=main_socket.accept()
   message=recieve_message(client_socket)
   print(f'{message}  is crashed please restart it')
   