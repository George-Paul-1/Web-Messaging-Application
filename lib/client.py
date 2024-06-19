import socket 
import threading 
from constraints import * 


class Client:
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = ""
        self.connected = True 
    
    def start_(self):
        self.client.connect(ADDR)
        receive_thread = threading.Thread(target=self.receive)
        send_thread = threading.Thread(daemon=True, target=self.send_msg)
        receive_thread.start()
        send_thread.start()

    def get_nickname(self):
        self.nickname = input("Choose Your Nickname: ")
        # Once database is built this will query database 

    def receive(self):
        while self.connected:
            try:
                message = self.client.recv(2048).decode(FORMAT)
                if message == 'NICK':
                    self.client.send(self.nickname.encode(FORMAT))
                else:
                    print(message)
            except:
                print("An error occured!")
                self.client.close()
                self.connected = False
                break
        self.client.close()

    def send_msg(self):
        while self.connected:
            message = f"{self.nickname}: {input('')}"
            if message.endswith(DISCONNECT_MESSAGE):
                self.connected = False
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message.encode(FORMAT))
        
        self.client.close()

cli = Client()
cli.get_nickname()
cli.start_()