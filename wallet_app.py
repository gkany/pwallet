#-*- coding: utf-8  -*-

import wx
import time
import json
import requests

env = ["local", "testnet", "prod"]
nodes_url = {
    env[0]: "http://192.168.192.148:8049", 
    env[1]: "http://test.cocosbcx.net", 
    env[2]: "https://api.cocosbcx.net"
}

headers = {"content-type": "application/json"}

wallet_apis = ["transfer", "suggest_brain_key", "get_account_by_name"]  # test

def json_dumps(json_data):
    return json.dumps(json_data, indent=4)

def request_post(url, req_data={}):
    response = json.loads(requests.post(url, data = json.dumps(req_data), headers = headers).text)
    print('>> {} {}\n{}\n'.format(req_data['method'], req_data['params'], response))
    return response

def request_post2(url, method, params=""):
    req_data = {
        "method": method,
        "params": [params],
        "id":1
    }
    response = request_post(url, req_data)
    if 'error' in response:
        jsonText = response['error']
    elif 'result' in response:
        jsonText = response['result']
    else:
        jsonText = response
    return jsonText

class ToolFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ToolFrame, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        self.env = env[1] #default testnet
        self.url = nodes_url[self.env]
        self.SetTitle('cli_wallet api 工具 -- {}'.format(self.env))
        self.SetSize((1080, 768))

        self.api_choice = wx.ComboBox(self, pos = (5, 5), value='select api', choices=wallet_apis, style=wx.CB_SORT)
        self.api_params = wx.TextCtrl(self, pos = (200, 5), size = (200, 25))

        self.method = ""
        self.Bind(wx.EVT_COMBOBOX, self.on_api_choice, self.api_choice)

        # self.inputBox = wx.BoxSizer(wx.HORIZONTAL)
        # self.inputBox.Add(api_choice, 1, flag=wx.LEFT |wx.RIGHT|wx.FIXED_MINSIZE, border=5)
        # self.inputBox.Add(api_params, 1, flag=wx.LEFT |wx.RIGHT|wx.FIXED_MINSIZE, border=5)

        self.runButton = wx.Button(self, label = '检查',pos = (450, 5), size = (100, 30)) #check|run
        self.clearButton = wx.Button(self, label = '清空',pos = (580, 5), size = (100, 30))
        self.textShow = wx.TextCtrl(self, pos = (5, 35), size = (800, 600), style = wx.TE_MULTILINE | wx.HSCROLL)
        self.Bind(wx.EVT_BUTTON, self.on_run, self.runButton)
        self.Bind(wx.EVT_BUTTON, self.on_clear, self.clearButton)

        # local--本地，testnet--测试网，prod--主网
        self.localCheck = wx.RadioButton(self, -1, env[0], pos=(820, 3), size=(70, 50), style=wx.RB_GROUP) 
        self.testnetCheck = wx.RadioButton(self, -1, env[1], pos=(900, 3), size=(70, 50)) 
        self.prodCheck = wx.RadioButton(self, -1, env[2], pos=(980, 3), size=(70, 50)) 
        self.localCheck.Bind(wx.EVT_RADIOBUTTON, self.on_local_check) 
        self.testnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_testnet_check) 
        self.prodCheck.Bind(wx.EVT_RADIOBUTTON, self.on_prod_check) 

        self.Show(True)

    def on_api_choice(self, event):
        self.method = event.GetString()

    def on_run(self, event):
        label = self.runButton.GetLabel()
        params = self.api_params.GetValue()
        if label == u'检查':
            new_label = u'执行'
            req_cmd = '{} {}'.format(self.method, params)
            self.textShow.Clear()
            self.textShow.AppendText(req_cmd)
        else:
            new_label = u'检查'
            jsonText = request_post2(self.url, self.method, params)
            self.show_text(json_dumps(jsonText))
        self.runButton.SetLabel(new_label)

    def on_local_check(self, event):
        self.on_check(self.localCheck.GetLabel())

    def on_testnet_check(self, event):
        self.on_check(self.testnetCheck.GetLabel())

    def on_prod_check(self, event):
        self.on_check(self.prodCheck.GetLabel())

    def on_check(self, value):
        self.env = value
        self.url = nodes_url[self.env]
        self.SetTitle('cli_wallet api 工具 -- {}'.format(self.env))

    def on_clear(self, event):
        # self.api_choice.SetDefault()
        self.api_params.Clear()
        self.textShow.Clear()
        self.runButton.SetLabel("检查")

    def on_show_text(self, method, params):
        jsonText = request_post2(self.url, method, params)
        self.show_text(json_dumps(jsonText))

    def show_text(self, text):
        self.textShow.Clear()
        self.textShow.AppendText(text)

def Main():
    app = wx.App()
    ToolFrame(None)
    app.MainLoop()

if __name__ == "__main__":
    Main()

