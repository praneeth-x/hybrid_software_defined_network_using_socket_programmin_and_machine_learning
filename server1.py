import socket
import select
import threading
import time
import traffic_clustering_model as tcm
import spam_message_classifier as smc
pingip='127.0.0.3'
ping_port=1234
spam_ip='127.0.0.4'
spam_port=5678
ip='127.0.0.8'
port=1235
ip_dict={'facebook':'127.0.0.1','google':'127.0.0.2'}
port_dict={'facebook':1236,'google':1237}
server_list=['127.0.0.5','127.0.0.6']
server_port=[1238,1239]
server_name_dict={'127.0.0.5':'server2','127.0.0.6':'server3'}
ping_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ping_socket.bind((pingip,ping_port))
ping_socket.listen()
type='utf-8'
client_website={}
header=10
kill_thread_2=False
kill_thread_3=False
kill_thread_1=False
killt1=False
killt2=False
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((ip,port))
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sockets_list=[server_socket]
main_ip='127.0.0.9'
main_port=4567
check_ip='127.0.0.10'
check_port=1863

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
        if not len(message):
            del check_server
            continue
        if(message=='how are you'):
            client_socket.send(add_header('i am fine'))
            break
        
def check_other_servers():
    global killt2
    while(killt2==False):
        for i in range(len(server_list)):
            if(killt2==True):
                break
            else:
                try:
                    checking_ip=server_list[i]
                    checking_port=server_port[i]
                    check_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    check_socket.connect((checking_ip,checking_port))
                    check_socket.send(add_header('how are you'))
                    reply=recieve_message(check_socket)
                    if not len(reply):
                        print('sending to main server')
                        send_to_main(server_name_dict[checking_ip])
                    else:
                        del check_socket
                except:
                    print('sending to main server thro exception')
                    send_to_main(server_name_dict[checking_ip])
                    continue
        print('all servers checked')
        break

def send_to_spam(client_name,message):
    con_soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    con_soc.connect((spam_ip,spam_port))
    con_soc.send(add_header(client_name))
    con_soc.send(add_header(message))
    del con_soc

def get_from_website(site_name,request):
    ip_website=ip_dict[site_name]
    port_website=port_dict[site_name]
    new_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    new_socket.connect((ip_website,port_website))
    new_socket.send(add_header(request))
    ans=recieve_message(new_socket)
    del new_socket
    return ans

def add_header(message):
    message=f'{len(message):<{header}}'+message
    return bytes(message,type)

def recieve_message(client_socket):
    message_length=int(client_socket.recv(header).decode(type))
    message=client_socket.recv(message_length).decode(type)
    return message

def main():
    print('server working')
    global kill_thread_1
    ping_socket.listen()
    server_socket.listen()
    while(kill_thread_1==False):
        client_socket,client_address=ping_socket.accept()
        print('came here also')
        ping=recieve_message(client_socket)
        if(ping=='hello'):
            print('sneding that ping was a success')
            client_socket.send(add_header('ping successful'))
        else:
            continue
        read_sockets,_,exceptional_sockets=select.select(sockets_list,[],sockets_list)
        for notified_socket in read_sockets:
            if(notified_socket==server_socket):
                client_socket1,client_address1=server_socket.accept()
                sockets_list.append(client_socket1)
                site_name=recieve_message(client_socket1)
                print('i have recieved site name as',site_name)
                if site_name==False:
                    sockets_list.remove(client_socket1)
                    continue
                print('accepted site name')
                client_website[client_socket1]=site_name
            else:
                site_name=client_website[notified_socket]
                request=recieve_message(notified_socket)
                if(request==False):
                    sockets_list.remove(notified_socket)
                    del client_website[notified_socket]
                    pass
                print('sending the answer')
                ans=get_from_website(site_name,request)
                check_ans=[ans,]
                check_ans=smc.cv.transform(check_ans)
                class_name=smc.model.predict(check_ans)
                print('predicted the value as',class_name)

                if(class_name!='spam'):
                    print('declared as ham')
                    notified_socket.send(add_header(ans))
                else:
                    notified_socket.send(add_header('you got a spam message which is redirect to spam server'))
                    client_name=recieve_message(notified_socket)
                    send_to_spam(client_name,ans)

                sockets_list.remove(notified_socket)
                del client_website[notified_socket]
            for i in exceptional_sockets:
                sockets_list.remove(i)
                del i
    else:
        print('server quiting sir')
        return

def execution(starting_times,ending_times,intervals):
    global kill_thread_1
    global kill_thread_3
    global kill_thread_2
    for i in range(len(range1)):
        if kill_thread_2==True:
            print('breaking already existing schedule\n')
            kill_thread_1=False
            break
        thread3=threading.Timer(0,ping_func)

#        test_thread2=threading.Timer(0,ping_func)
        thread1=threading.Timer(0,main)
#        test_thread3=threading.Timer(0,main)

        kill_thread_1=False

        thread1.start()

        start=time.time()

        print('\ninterval',intervals[i])
        if kill_thread_2==True:
            print('breaking already existing schedule\n')
            kill_thread_1=False
            break
        end=time.time()
        while(end-start<=intervals[i]):
            end=time.time()
        print('worked for',end-start)
        kill_thread_1=True
#        test_thread3.start()
        print()
        thread3.start()
        time.sleep(starting_times[i+1])
        kill_thread_3=True
#        test_thread2.start()
    kill_thread_1=False

def ping_func():
    global kill_thread_3
    global kill_thread_2
    global kill_thread_1
    print('ping on duty')
    ping_socket.listen()
    while(kill_thread_3==False):
        client_socket,client_address=ping_socket.accept()
        ping =client_socket.recv(5)
        if ping==False:
            continue
        else:
            print('sorry for sleeping waking him up')
            client_socket.send(add_header('i woke him up'))
            kill_thread_2=True
            kill_thread_1=False
            print('executing main')
            main()
    else:
        print('pinging function signing off')


if __name__=='__main__':
    starting_times=[]
    ending_times=[]
    range1=tcm.range_times(tcm.data1,tcm.server1)
#    thread5=threading.Timer(65,check_other_servers)
 #   thread5.start()
    for i in range(len(range1)):
        starting_times.append(range1[i][0])
        ending_times.append(range1[i][1])
    starting_times.sort()
    ending_times.sort()
    print(starting_times)
    print(ending_times)

    intervals=[]
    for i in range(len(starting_times)):
        intervals.append(ending_times[i]-starting_times[i])
    for i in range(1,len(range1)):
        starting_times[i]=starting_times[i]-ending_times[i-1]
    starting_times.append(0)
    thread2=threading.Timer(0,execution,args=(starting_times,ending_times,intervals))
    thread4=threading.Timer(0,ping_func)
#    test_thread1=threading.Timer(0,ping_func)
    thread4.start()
    time.sleep(starting_times[0])
    kill_thread_3=True
#    test_thread1.start()
    kill_thread_3=False
    thread2.start()
    t3=threading.Timer(60,check)
    t3.start()
