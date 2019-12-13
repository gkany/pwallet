import wx



class CFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="boxSizer test", size=(300, 120))
        self.Centre()

        panel = wx.Panel(parent=self)

        vbox = wx.BoxSizer(wx.VERTICAL) 
        self.staticText = wx.StaticText(parent=panel, label="单击")
        vbox.Add(self.staticText, proportion=2, 
            flag=wx.FIXED_MINSIZE|wx.TOP|wx.CENTER, border=10)

        b1 = wx.Button(parent=panel, id=10, label="按钮1")
        b2 = wx.Button(parent=panel, id=11, label="按钮2")
        self.Bind(wx.EVT_BUTTON, self.on_click, id=10, id2=20)
        
        #创建水平方向box布局管理器（默认水平方向）
        hbox = wx.BoxSizer()
        #将两个button添加到hbox布局管理器中
        hbox.Add(b1,0,wx.EXPAND | wx.BOTTOM ,border=5)
        hbox.Add(b2,0,wx.EXPAND | wx.BOTTOM ,border=5)

        vbox.Add(hbox, proportion=1, flag=wx.CENTER)

        panel.SetSizer(vbox)

    def on_click(self, event):
        pass

class CApp(wx.App):
    def OnInit(self):
        frame = CFrame()
        frame.Show()
        return True

    def OnExit(self):
        print("app exit")
        return 0

if __name__ == "__main__":
    app = CApp()
    app.MainLoop()
