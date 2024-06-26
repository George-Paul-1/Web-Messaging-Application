import wx
from client import Client 
from login_window import *


class Chat(wx.Frame):
    
    def __init__(self):
        super().__init__(parent=None, title='Chat')
        
        self.cli = Client(self.update_chat_window)
        
        if not self.cli.nickname:
            self.show_login_window()
        
        self.cli.start_()
        
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(panel, pos=(5, 5))
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        
        my_btn = wx.Button(panel, label='Press Me', pos=(5, 55))
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)

        self.st = wx.StaticText(panel, label ="") 

        my_sizer.Add(self.st, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(my_sizer)
        self.Show() 
    
    def show_login_window(self):
        login_dialog = LoginWindow(self)
        if login_dialog.ShowModal() == wx.ID_OK:
            self.cli.set_nickname(login_dialog.username)
        login_dialog.Destroy()

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            self.cli.send_msg(value)
            self.text_ctrl.SetValue('')
    
    def update_chat_window(self, message):
        current_text = self.st.GetLabel()
        new_text = f"{current_text}\n{message}"
        self.st.SetLabel(new_text)
    
    
if __name__=='__main__':
    app = wx.App()
    frame = Chat()
    app.MainLoop()