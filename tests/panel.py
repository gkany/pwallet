import  wx

class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u"测试面板panel", size=(300, 200))

        #创建面板
        panel = wx.Panel(self)

        # 创建按钮, 添加到面板中
        button = wx.Button(panel, label=u"关闭窗口", pos=(100, 60), size=(100, 60))

        # 给按钮绑定事件
        # self.Bind(wx.EVT_BUTTON, self.onButton, button)
        self.Bind(wx.EVT_BUTTON, self.onButtonMessageDialog, button)

    def onButton(self, e):
        self.Close(True)

    def onButtonMessageDialog(self, e):
        dialog = wx.MessageDialog(None, u"消息对话框测试", u"标题信息", wx.YES_NO|wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close()
        dialog.Destroy()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()