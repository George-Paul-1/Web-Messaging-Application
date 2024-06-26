import wx 

class LoginWindow(wx.Dialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent, title='Login', size=(300, 200))

        self.username = ""
        
        panel = wx.Panel(self)
        my_sizer= wx.BoxSizer(wx.VERTICAL)

        self.st = wx.StaticText(panel, label = "CHOOSE YOUR USERNAME")
        my_sizer.Add(self.st, 0, wx.ALL | wx.CENTER, 5) 
    
        self.text_control = wx.TextCtrl(panel, pos=(5, 5))
        my_sizer.Add(self.text_control, 0, wx.ALL | wx.EXPAND, 5)

        my_btn = wx.Button(panel, label='Submit', pos=(5, 55))
        my_btn.Bind(wx.EVT_BUTTON, self.submit_username)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
    
        panel.SetSizer(my_sizer)

        dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        dialog_sizer.Add(panel, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(dialog_sizer)
        self.Layout()


    def submit_username(self, event):
        user = self.text_control.GetValue()
        self.username = user.strip()
        self.EndModal(wx.ID_OK)
    
if __name__=='__main__':
    app = wx.App()
    dialog = LoginWindow()
    dialog.ShowModal()
    print(f"Username entered: {dialog.username}")
    dialog.Destroy()
    app.MainLoop()