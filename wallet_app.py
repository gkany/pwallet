#-*- coding: utf-8  -*-

import wx
import time
import json
import requests

env = ["local", "testnet", "prod"]
nodes_url = {
    env[0]: "http://192.168.192.148:8049", #192.168.192.148:8049
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
        mainBox = wx.BoxSizer(wx.VERTICAL)
        # self.SetSizer(mainBox)

        panel = wx.Panel(self, -1)
        # 1
        envBox = wx.BoxSizer()
        # # local--本地，testnet--测试网，prod--主网
        envText = wx.StaticText(panel, label=u'请选择使用的链: ')
        self.localCheck = wx.RadioButton(panel, -1, env[0], style=wx.RB_GROUP) 
        self.testnetCheck = wx.RadioButton(panel, -1, env[1]) 
        self.prodCheck = wx.RadioButton(panel, -1, env[2]) 

        self.localCheck.Bind(wx.EVT_RADIOBUTTON, self.on_local_check) 
        self.testnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_testnet_check) 
        self.prodCheck.Bind(wx.EVT_RADIOBUTTON, self.on_prod_check) 

        envBox.Add(envText, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.localCheck, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.testnetCheck, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.prodCheck, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        
        mainBox.Add(envBox)

        # 2
        inputBox = wx.BoxSizer(wx.HORIZONTAL)
        apiText = wx.StaticText(panel, label=u"选择接口")
        self.api_choice = wx.ComboBox(panel, value='select api', choices=wallet_apis)
        paramsText = wx.StaticText(panel, label=u"参数(多个逗号分隔)")
        self.api_params = wx.TextCtrl(panel, size=(400, 20))

        inputBox.Add(apiText, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        inputBox.Add(self.api_choice, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        inputBox.Add(paramsText, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        inputBox.Add(self.api_params, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)

        operationBox = wx.BoxSizer(wx.HORIZONTAL)
        self.checkButton = wx.Button(panel, label='检查') 
        self.runButton = wx.Button(panel, label='执行') 
        self.clearButton = wx.Button(panel, label='清空')
        operationBox.Add(self.checkButton, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        operationBox.Add(self.runButton, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        operationBox.Add(self.clearButton, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)

        self.method = ""
        self.Bind(wx.EVT_COMBOBOX, self.on_api_choice, self.api_choice)
        self.Bind(wx.EVT_BUTTON, self.on_call_check, self.checkButton)
        self.Bind(wx.EVT_BUTTON, self.on_run, self.runButton)
        self.Bind(wx.EVT_BUTTON, self.on_clear, self.clearButton)

        mainBox.Add(inputBox)
        mainBox.Add(operationBox)
        
        # 3
        self.textShow = wx.TextCtrl(panel, size = (1000, 768), style = wx.TE_MULTILINE | wx.HSCROLL)
        # self.textShow = wx.TextCtrl(panel, style = wx.TE_MULTILINE | wx.HSCROLL)
        mainBox.Add(self.textShow, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 1)

        panel.SetSizer(mainBox) 
        self.Show(True)

    def on_api_choice(self, event):
        self.method = event.GetString()

    def on_call_check(self, event):
        label = self.runButton.GetLabel()
        params = self.api_params.GetValue()
        req_cmd = '{} {}'.format(self.method, params)
        self.textShow.Clear()
        self.textShow.AppendText(req_cmd)

    def on_run(self, event):
        label = self.runButton.GetLabel()
        params = self.api_params.GetValue()
        jsonText = request_post2(self.url, self.method, params)
        self.show_text(json_dumps(jsonText))

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

