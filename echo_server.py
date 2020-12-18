import socket
import select
import json

serverPort = 8000
serverId = "127.0.0.1"
# storing client users in client_sockets_list (active userlist)
client_sockets_list = []
msgs = []
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((serverId, serverPort)) 
serverSocket.listen()
sockets_list=[serverSocket]
client_count = 0
# using static user list
static_userlist = ["Alice", "Bob"]
print(f"Server Started! \nListen on {serverId}:{serverPort}")

def recv_msg(clientSocket):
    try:
        client_details = clientSocket.recv(1024).decode('utf-8')
        recv_details = json.loads(client_details)
        # to get user list
        if recv_details['cmd'] == '1':
            # for active user list ----------------------------------
            # user_list = []
            # for i in client_sockets_list:
            #     user_list.append(i['Username'])
            # user_json_list = json.dumps({'msg': user_list})
            # clientSocket.send(user_json_list.encode('utf-8'))
            # -------------------------------------------------------

            # for static user list ----------------------------------
            user_json_list = json.dumps({'msg': static_userlist})
            clientSocket.send(user_json_list.encode('utf-8'))
            # -------------------------------------------------------
            print('Returned user list.')
        #for sending a message
        elif recv_details['cmd'] == '2':
            del recv_details['cmd']
            msgs.append(recv_details)
            clientSocket.send('true'.encode('utf-8'))
            print(f"A message to {recv_details['to']}")
            print(f"Message: \n{recv_details['msg']}")
        # for chating with a friend
        elif recv_details['cmd'] == '4':
            user = recv_details['user']
            for i,v in enumerate(client_sockets_list):
                if user in v.values():
                    del client_sockets_list[i]
            clientSocket.send('true'.encode('utf-8'))
            sockets_list.remove(clientSocket)
            clientSocket.close()
            print('Client disconnected!')
        # for getting messages
        elif recv_details['cmd'] == '3':
            user = recv_details['user']
            msg_list = []
            for i in msgs:
                if i['to'] == user:
                    msg_list.append(i['msg'])
            print(f"Sent back {user} message!")
            clientSocket.send(json.dumps({'msg': msg_list}).encode('utf-8'))
        return True
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for each_socket in read_sockets:
        if each_socket == serverSocket:
            client_count = client_count + 1
            print(f"client {client_count} connected.")
            clientSocket, clientAddr = serverSocket.accept()
            client_details = clientSocket.recv(1024).decode('utf-8')
            client_user = json.loads(client_details)
            # adding user to the lsit
            client_sockets_list.append(client_user)
            clientSocket.send(client_details.encode('utf-8'))
            for i in client_user:
                print(f"Login {i} is {client_user[i]}")
            sockets_list.append(clientSocket)
        else:
            msg = recv_msg(each_socket)
            if msg is False:
                sockets_list.remove(each_socket)
                continue