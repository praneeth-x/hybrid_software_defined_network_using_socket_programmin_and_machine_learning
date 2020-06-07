import socket
pingip='127.0.0.3'
ping_port=1234
type='utf-8'
ip='127.0.0.8'
port=1235
header=10
spam_ip='127.0.0.4'
spam_port=5678
def recieve_message(client_socket):
    message_length=int(client_socket.recv(header).decode(type))
    message=client_socket.recv(message_length).decode(type)
    return message
def add_header(message):
    message=f'{len(message):<{header}}'+message
    return bytes(message,type)

def main():
    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        ping_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ping_socket.connect((pingip,ping_port))
        ping_socket.send(add_header('hello'))
        message=recieve_message(ping_socket)
        if message==False:
            print('server hasnt sent me any message')
        if(message=='i woke him up'):
            print('he is woken up')
            del ping_socket
        if(message=='ping successful'):
            print('i came here')
            client_socket.connect((ip,port))
            print('connection is done beacuse of waking him up')
            site_name=input('enter site_name :')
            request=input('enter the request :')
            client_socket.send(add_header(site_name))
            del ping_socket
            ping_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            ping_socket.connect((pingip,ping_port))
            ping_socket.send(add_header('hello'))
            reply=recieve_message(ping_socket)
            if(reply=='ping successful'):
                client_socket.send(add_header(request))
                ans=recieve_message(client_socket)
                if(ans=='you got a spam message which is redirect to spam server'):
                    print(ans)
                    client_socket.send(add_header('client1'))
                else:
                    print(ans)
                del ping_socket
            del client_socket
            client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def check_spam():
    spam_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    spam_socket.connect((spam_ip,spam_port))
    spam_socket.send(add_header('please send my spam messsages to me'))
    spam_socket.send(add_header('client1'))
    length=recieve_message(spam_socket)
    length=int(length)
    print('your spam messages are')
    for i in range(length):
        message=recieve_message(spam_socket)
        print(message)

if __name__=='__main__':
    in1=int(input('press 1 to browse and press 2 to check your spam messages'))
    if(in1==1):
        main()
    if(in1==2):
        check_spam()
    else:
        print('please enter a valid key')
