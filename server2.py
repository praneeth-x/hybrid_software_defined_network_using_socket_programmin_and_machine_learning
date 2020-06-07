import socket
import threading
import time
type='utf-8'
header=10
server_list=['127.0.0.10','127.0.0.6']
server_port=[1863,1239]
server_name_dict={'127.0.0.10':'server1','127.0.0.6':'server3'}
main_ip='127.0.0.9'
main_port=4567
check_ip='127.0.0.5'
check_port=1238
killt1=False
killt2=False
def add_header(message):
    message=f'{len(message):<{header}}'+message
    return bytes(message,type)

def recieve_message(client_socket):
    message_length=int(client_socket.recv(header).decode(type))
    message=client_socket.recv(message_length).decode(type)
    return message

def check_other_servers():
    global killt2
    while(killt2==False):
        for i in range(len(server_list)):
            if(killt2==True):
                break
            else:
                try:
                    check_ip=server_list[i]
                    check_port=server_port[i]
                    check_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    check_socket.connect((check_ip,check_port))
                    check_socket.send(add_header('how are you'))
                    reply=recieve_message(check_socket)
                    if not len(reply):
                        send_to_main(server_name_dict[check_ip])
                    else:
                        del check_socket
                except:
                    send_to_main(server_name_dict[check_ip])
                    continue
        print('all servers checked')
        break

def send_to_main(message):
    con_soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    con_soc.connect((main_ip,main_port))
    con_soc.send(add_header(message))
    del con_soc
def reply_to_check():
    global killt1
    while (killt1==False):
        check_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        check_server.bind((check_ip,check_port))
        check_server.listen()
        client_socket,client_address=check_server.accept()
        message=recieve_message(client_socket)
        if (not len(message)):
            del check_server
            continue
        if(message=='how are you'):
            client_socket.send(add_header('i am fine'))
            break
def check():
        global killt1
        global killt2
        t1=threading.Timer(0,reply_to_check)
        t2=threading.Timer(0,check_other_servers)
        t1.start()
        t2.start()
        time.sleep(5)
        killt1=True
        killt2=True
        del t1
        del t2

if __name__=='__main__':
    t3=threading.Timer(60,check)
    t3.start()
