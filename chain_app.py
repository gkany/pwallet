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

assets = ["1.3.0", "1.3.1"]  # get_account_balances 默认查询 COCOS 和 GAS

headers = {"content-type": "application/json"}

def json_dumps(json_data):
    return json.dumps(json_data, indent=4)

def request_post(url, req_data={}):
    response = json.loads(requests.post(url, data = json.dumps(req_data), headers = headers).text)
    # print('>> {} {}\n{}\n'.format(req_data['method'], req_data['params'], response))
    return response

def request_post2(url, method, params=[]):
    req_data = {
        "method": method,
        "params": params,
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
        self.SetTitle('查询工具--{}'.format(self.env))
        self.SetSize((1080, 768))

        self.queryAccountButton = wx.Button(self, label = 'get_account',pos = (225, 5), size = (100, 30))
        self.objectIDButton = wx.Button(self, label = 'get_object',pos = (330, 5), size = (100, 30))
        self.balanceButton = wx.Button(self, label = 'account_balances',pos = (440, 5), size = (130, 30))
        self.propertiesButton = wx.Button(self, label = 'properties',pos = (580, 5), size = (100, 30))
        self.clearButton = wx.Button(self, label = '清空',pos = (690, 5), size = (100, 30))
        self.textInput = wx.TextCtrl(self, pos = (5, 5), size = (210, 25))
        self.textShow = wx.TextCtrl(self, pos = (5, 35), size = (800, 600), style = wx.TE_MULTILINE | wx.HSCROLL)
        self.Bind(wx.EVT_BUTTON, self.on_get_account, self.queryAccountButton)
        self.Bind(wx.EVT_BUTTON, self.on_get_object, self.objectIDButton)
        self.Bind(wx.EVT_BUTTON, self.on_list_account_balances, self.balanceButton)
        self.Bind(wx.EVT_BUTTON, self.on_properties, self.propertiesButton)
        self.Bind(wx.EVT_BUTTON, self.on_clear, self.clearButton)

        # local--本地，testnet--测试网，prod--主网
        self.localCheck = wx.RadioButton(self, -1, env[0], pos=(820, 3), size=(70, 50), style=wx.RB_GROUP) 
        self.testnetCheck = wx.RadioButton(self, -1, env[1], pos=(900, 3), size=(70, 50)) 
        self.prodCheck = wx.RadioButton(self, -1, env[2], pos=(980, 3), size=(70, 50)) 
        self.localCheck.Bind(wx.EVT_RADIOBUTTON, self.on_local_check) 
        self.testnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_testnet_check) 
        self.prodCheck.Bind(wx.EVT_RADIOBUTTON, self.on_prod_check) 

        self.Show(True)

    def on_local_check(self, event):
        self.on_check(self.localCheck.GetLabel())

    def on_testnet_check(self, event):
        self.on_check(self.testnetCheck.GetLabel())

    def on_prod_check(self, event):
        self.on_check(self.prodCheck.GetLabel())

    def on_check(self, value):
        self.env = value
        self.url = nodes_url[self.env]
        self.SetTitle('查询工具--{}'.format(self.env))

    def on_clear(self, event):
        self.textInput.Clear()
        self.textShow.Clear()

    def on_show_text(self, method, params=[], is_clear_text=True):
        jsonText = request_post2(self.url, method, params)
        self.show_text(json_dumps(jsonText), is_clear_text)

    def show_text(self, text, is_clear_text=True):
        if is_clear_text:
            self.textShow.Clear()
        self.textShow.AppendText(text)
        self.textShow.AppendText('\n')

    def on_get_account(self, event):
        name = self.textInput.GetValue()
        if len(name.split(".")) == 3:
            self.on_show_text("get_objects", [[name]])
        else:
            self.on_show_text("get_account_by_name", [name])
    
    def on_get_object(self, event):
        object_id = self.textInput.GetValue()
        self.on_show_text("get_objects", [[object_id]])

    def on_list_account_balances(self, event):
        name = self.textInput.GetValue()
        if len(name.split(".")) == 3:
            method = "get_account_balances"
        else:
            method = "get_named_account_balances"
        self.on_show_text(method, [name, assets])

    def on_properties(self, event):
        is_simple = self.textInput.GetValue()
        self.textShow.Clear()
        self.on_show_text(method="get_chain_properties", is_clear_text=False)
        self.on_show_text(method="get_dynamic_global_properties", is_clear_text=False)
        if len(is_simple) > 0:
            self.on_show_text(method="get_global_properties", is_clear_text=False)
            self.on_show_text(method="get_config", is_clear_text=False)

def Main():
    app = wx.App()
    ToolFrame(None)
    app.MainLoop()

if __name__ == "__main__":
    Main()

