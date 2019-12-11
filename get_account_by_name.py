import wx
from utils import *

def on_query_account(event):
    account_name = textInput.GetValue()
    showText = ""
    if account_name != "":
        req_data = {
            "method": "get_account_by_name",
            "params": [account_name],
            "id":1
        }
        showText = request_post(req_data)
        if showText == 'null':
            showText = '账户 {} 不存在'.format(account_name)
    else:
        showText = "account name is empty"
    textShow.Clear()
    textShow.AppendText(showText)
    queryButton.SetLabel("账户查询")

app = wx.App()
win = wx.Frame(None, title = "查询测试工具", size=(1000, 800))
win.Show()
 
queryButton = wx.Button(win, label = '账户查询',pos = (225, 5), size = (80, 25))
textInput = wx.TextCtrl(win, pos = (5, 5), size = (210, 25))
textShow = wx.TextCtrl(win, pos = (5, 35), size = (800, 600), style = wx.TE_MULTILINE | wx.HSCROLL)
app.Bind(wx.EVT_BUTTON, on_query_account, queryButton)

app.MainLoop()


