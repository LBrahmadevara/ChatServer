import socket
import json
import select

clientSocket = socket.socket()
user_input = ''
username = ''


def initial():
    print("Command: \n0. Connect to the server \n1. Get the user list \n2. Send a message \n3. Get my messages \n4. Initiate a chat with my friend \n5. Chat with my friend")
    user_input = input("Your option<Enter a number>: ")
    return user_input

def end_of_line():
    print("---------------------------------------------------------------------")

def con_to_server():
    serverName = input("Please enter the IP address: ")
    serverPort = input("Please enter the port number: ")
    # serverName = "127.0.0.1"
    # serverPort = 8000
    clientSocket.connect((serverName,int(serverPort)))
    print("Connecting...")
    print("Connected! \nWelcome! Please log in.")
    login()
    

def login():
    global username 
    username = input("Username: ")
    password = input("Password: ")
    login_details = {"Username": username, "Password": password}
    print(login_details)
    clientSocket.send(json.dumps(login_details).encode('utf-8'))
    modifiedSentence = clientSocket.recv(1024).decode('utf-8')
    if modifiedSentence: 
        print("Login success!")
        end_of_line()
        

def user_list():
    msg = {'cmd': '1'}
    clientSocket.send(json.dumps(msg).encode('utf-8'))
    user = clientSocket.recv(1024).decode('utf-8')
    user_details = json.loads(user)
    print(user_details)
    print(f"There are {len(user_details['msg'])} user/s.")
    for each_user in user_details['msg']:
        print(each_user)
    end_of_line()
    

def send_msg():
    send_to = input("Please enter username: ")
    message = input("Please enter message: ")
    msg = {'cmd':'2', 'to': send_to, 'from': username, 'msg': message}
    clientSocket.send(json.dumps(msg).encode('utf-8'))
    recv_msg = clientSocket.recv(1024).decode('utf-8')
    if recv_msg == 'true':
        print('\nMessage sent successfully!')
    end_of_line()
    

def initiate_chat():
    msg = {'cmd': '4', 'user': username}
    clientSocket.send(json.dumps(msg).encode('utf-8'))
    recv_msg = clientSocket.recv(1024).decode('utf-8')
    if recv_msg == 'true':
        print('----------------------disconnected with server----------------------')
    clientSocket.close()
    serverPort = input("Enter the port number you want to listen on: ")
    print(f"Listening on 127.0.0.1:{serverPort}")
    serverId = '127.0.0.1'

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((serverId, int(serverPort)))
    serverSocket.listen()
    sockets_list = [serverSocket]

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for each_socket in read_sockets:
            if each_socket == serverSocket:
                client_socket, client_addr = serverSocket.accept()
                user = client_socket.recv(1024).decode('utf-8')
                print(f"{user} is connected!")
                sockets_list.append(client_socket)
            else:
                print("<Type Bye to stop conversation>")
                client_details = client_socket.recv(1024).decode('utf-8')
                print(client_details)
                if client_details.lower() == 'bye':
                    sockets_list.remove(client_socket)
                    break
                text = input(f"{username}: ")
                if text.lower() == "bye":
                    client_socket.send('bye'.encode('utf-8'))
                    sockets_list.remove(client_socket)
                    break
                text_str = username+" "+text
                client_socket.send(text_str.encode('utf-8'))
        if len(sockets_list) == 1:
            client_socket.close()
            print("Disconnected from friend!")
            end_of_line()
            break


def get_msg():
    msg = {'cmd': '3', 'user': username}
    clientSocket.send(json.dumps(msg).encode('utf-8'))
    recv_msg = json.loads(clientSocket.recv(1024).decode('utf-8'))
    print(f"You have {len(recv_msg['msg'])} message/s.")
    for i in recv_msg['msg']:
        print(i)
    end_of_line()

def chat_with_frnd():
    msg = {'cmd': '4', 'user': username}
    clientSocket.send(json.dumps(msg).encode('utf-8'))
    recv_msg = clientSocket.recv(1024).decode('utf-8')
    cli_socket = socket.socket()
    if recv_msg == 'true':
        print('----------------------disconnected with server----------------------')
    clientSocket.close()
    serverIp = input("Enter your friend's IP: ")
    serverPort = input("Enter your friend's port number: ")
    cli_socket.connect((serverIp,int(serverPort)))
    cli_socket.send(username.encode('utf-8'))
    print(f"Connecting to your friend \nConnected!")
    while True:
        print("<Type Bye to stop conversation>")
        text = input(f"{username}: ")
        text_str = username + ": "+ text
        if text.lower() == 'bye':
            cli_socket.send('bye'.encode('utf-8'))
            cli_socket.close()
            print("Disconnected from friend!")
            end_of_line()
            break
        
        cli_socket.send(text_str.encode('utf-8'))
        recv_text = cli_socket.recv(1024).decode('utf-8')
        if recv_text.lower() == 'bye':
            cli_socket.close()
            print("Disconnected from friend!")
            end_of_line()
            break
        print(recv_text)


while True:
    user_input = initial()
    if user_input == '0':
        con_to_server()
    elif user_input == '1':
        user_list()
    elif user_input == '2':
        send_msg()
    elif user_input == '4':
        initiate_chat()
    elif user_input == '3':
        get_msg()
    elif user_input == '5':
        chat_with_frnd()



