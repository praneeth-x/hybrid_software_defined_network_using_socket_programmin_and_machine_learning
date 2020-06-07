import socket
facebook_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip='127.0.0.1'
port=1236
facebook_socket.bind((ip,port))
facebook_socket.listen()
header=10
type='utf-8'
request_dict={"hello": 'welcome to facebook',"feed":"no feed","requests":"no request",'spam request':'Get your garden ready for summer with a FREE selection of summer bulbs and seeds worth ÃƒÂ¥Ã‚Â£33:50 only with The Scotsman this Saturday. To stop go2 notxt.co.uk'}
def add_header(message):
    message=f'{len(message):<{header}}'+message
    return bytes(message,type)
def recieve_msg(client_socket):
    message_length=int(client_socket.recv(header).decode(type))
    if not message_length:
        return False
    message=client_socket.recv(message_length)
    return message.decode(type)
while True:
    client_socket,client_address=facebook_socket.accept()
    request=recieve_msg(client_socket)
    print(f'recieved an {request} request')
    ans=request_dict[request]
    print(f'sending ans as {ans}')
    ans=add_header(ans)
    client_socket.send(ans)
