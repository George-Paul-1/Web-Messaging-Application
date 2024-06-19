import socket 
import threading 
from constraints import * 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR) 

clients, nicknames = [], []

clients_lock = threading.Lock()

def broadcast(message):
    with clients_lock:
        for client in clients:
            try:
                client.send(message.encode(FORMAT))
            except:
                client.close()
                clients.remove(client)


def handle_client(client, addr):
    connected = True
    while connected:
        try: 
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                print(msg)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    broadcast(msg)
                    print("Message Received By Server")
        except: 
            connected = False
    
    with clients_lock:
        if client in clients:
            clients.remove(client)

    client.close()
    print(f"Connection with {addr} ended") 
    broadcast(f"{addr} has left the chat.")


def start():
    print("[STARTING] server is starting...")
    
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    
    while True:
        client, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected")

        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(HEADER).decode(FORMAT)
        with clients_lock:
            nicknames.append(nickname)
            clients.append(client)

        print(f"Nickname is: {nickname}")
        broadcast(f"{nickname} joined!\n")
        thread = threading.Thread(target=handle_client, args=(client,addr)) 

        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


start()





 


