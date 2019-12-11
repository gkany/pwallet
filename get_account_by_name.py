import wx
from utils import *

def on_query_account(event):
    account_name = textInput.GetValue()
    print('account_name: {}'.format(account_name))
    req_data = {
        "method": "get_account_by_name",
        "params": [account_name],
        "id":1
    }
    status, result = request_post(req_data)
    if status:
        dynamic_global_properties = json_dumps(result)
        textShow.Clear()
        textShow.AppendText(dynamic_global_properties)
    queryButton.SetLabel("账户查询")

app = wx.App()
win = wx.Frame(None, title = "查询测试工具", size=(410,335))
win.Show()
 
queryButton = wx.Button(win, label = '账户查询',pos = (225,5), size = (80,25))
textInput = wx.TextCtrl(win, pos = (5,5), size = (210,25))
textShow = wx.TextCtrl(win, pos = (5,35), size = (390,260), style = wx.TE_MULTILINE | wx.HSCROLL)
app.Bind(wx.EVT_BUTTON, on_query_account, queryButton)

app.MainLoop()


