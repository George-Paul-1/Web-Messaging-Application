import socket 
import threading 
from constraints import * 
from login_window import *
import wx

class Client:
    
    def __init__(self, update_callback):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = ""
        self.connected = True 
        self.history = []
        self.update_callback = update_callback
    
    def set_nickname(self, nickname):
        
        self.nickname = nickname

    def start_(self):
        self.client.connect(ADDR)
        
        receive_thread = threading.Thread(target=self.receive, daemon=True)
        receive_thread.start()

    def receive(self):
        while self.connected:
            try:
                message = self.client.recv(2048).decode(FORMAT)
                if message == 'NICK':
                    self.client.send(self.nickname.encode(FORMAT))
                else:
                    print(message)
                    wx.CallAfter(self.update_callback, message)
            except:
                print("An error occured!")
                self.disconnect()
                break

    def calculate_send_length(self, message):
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        return send_length

    def send_msg(self, message):
        if self.connected:
            self.history.append(message)
            send_length = self.calculate_send_length(message)
            self.client.send(send_length)
            self.client.send(message.encode(FORMAT))
            if message.endswith(DISCONNECT_MESSAGE):
                self.disconnect()


    def disconnect(self):
        print("Disconnecting...")
        try:
            self.client.close()
            self.connected = False
            print("Disconnected")
        except:
            print("There was an error disconnecting")
