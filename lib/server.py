import socket 
import threading 
from constraints import * 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR) 

clients, nicknames = [], []


def broadcast(message):
    for client in clients:
        client.send(message.encode(FORMAT))


def handle_client(client, addr):
    connected = True
    while connected:
        try: 
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    client.close()
                    print("User has left")
                    break
                broadcast(msg)
                print("Message Received By Server")
        except: 
            client.close()
            broadcast(f'{addr} has left!')
            break

    client.close()
    print(f"Connection with {addr} ended") 


def start():
    print("[STARTING] server is starting...")
    
    server.listen(2)
    print(f"[LISTENING] Server is listening on {SERVER}")
    
    while True:
        client, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected")

        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(HEADER).decode(FORMAT)
        
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname is: {nickname}")
        broadcast(f"{nickname} joined!\n")
        thread = threading.Thread(target=handle_client, args=(client,addr)) 

        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


start()





 


