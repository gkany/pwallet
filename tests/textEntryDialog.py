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
        # self.Bind(wx.EVT_BUTTON, self.onButtonMessageDialog, button)
        self.Bind(wx.EVT_BUTTON, self.onButtonTextEntryDialog, button)
        # self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)

    def onButton(self, e):
        self.Close(True)

    def onButtonMessageDialog(self, e):
        dialog = wx.MessageDialog(None, u"消息对话框测试", u"标题信息", wx.YES_NO|wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close()
        dialog.Destroy()

    def onButtonTextEntryDialog(self, e):
        dlg = wx.TextEntryDialog(None, u"请在下面文本框中输入内容", u"文本输入框标题", u"默认内容")
        print("dialog.....: {}, {} , {}".format(dlg.ShowModal(), dlg.ShowModal() == wx.ID_OK, dlg.GetValue()))
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetValue()  #获取输入框中的内容
            print(message)
            dialog_tip = wx.MessageDialog(None, message, u"标题信息", wx.OK | wx.ICON_INFORMATION)
            if dialog_tip.ShowModal() == wx.ID_YES:
                self.Close(True)
            dialog_tip.Destroy()
        dlg.Destroy()

    def OnCloseMe(self, event):
        dlg = wx.TextEntryDialog(None, u"请在下面文本框中输入内容:", u"文本输入框标题", u"默认内容")
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetValue() #获取文本框中输入的值
            dlg_tip = wx.MessageDialog(None, message, u"标题信息", wx.OK | wx.ICON_INFORMATION)
            if dlg_tip.ShowModal() == wx.ID_OK:
                self.Close(True)
            dlg_tip.Destroy()
        dlg.Destroy()

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
