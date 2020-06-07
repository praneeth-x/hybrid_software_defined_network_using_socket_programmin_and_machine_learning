import socket
spam_ip='127.0.0.4'
spam_port=5678
header=10
type='utf-8'
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((spam_ip,spam_port))
server_socket.listen()
client_messages={'client1':[],'client2':[],'client3':[]}
def recieve_message(client_socket):
    message_length=int(client_socket.recv(header).decode(type))
    message=client_socket.recv(message_length).decode(type)
    return message
def add_header(message):
    message=f'{len(message):<{header}}'+message
    return bytes(message,type)

while True:
        client_socket,client_address=server_socket.accept()
        request=recieve_message(client_socket)
        if(request=='please send my spam messsages to me'):
            client_name=recieve_message(client_socket)
            client_socket.send(add_header(str(len(client_messages[client_name]))))
            for i in range(len(client_messages[client_name])):
                client_socket.send(add_header(client_messages[client_name][i]))
        else:
            message=recieve_message(client_socket)
            client_messages[request].append(message)
