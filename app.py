#-*- coding: utf-8  -*-

import wx
import time
import json
import requests
from wx.lib.pubsub import pub
from threading import Thread, Lock

from graphsdk.graphene import Graphene, ping
from graphsdk.instance import set_shared_graphene_instance

env = [ u"主网", u"测试网(默认)", u"自定义"]
nodeAddresses = {
    env[0]: "wss://api.cocosbcx.net",
    env[1]: "wss://test.cocosbcx.net", 
    env[2]: "ws://127.0.0.1:8049"
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

def call_after(func):
    def _wrapper(*args, **kwargs):
        return wx.CallAfter(func, *args, **kwargs)
    return _wrapper

class WalletFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(WalletFrame, self).__init__(*args, **kwargs)
        # self.Center()
        self.titleLock = Lock()
        self.env = env[1] #default testnet
        self.nodeAddress = nodeAddresses[self.env]
        self.initGraphene(self.nodeAddress)
        self.InitUI()

    def initGraphene(self, nodeAddress):
        if ping(node=nodeAddress, num_retries=1):
            self.gph = Graphene(node=nodeAddress, num_retries=1) 
            set_shared_graphene_instance(self.gph)
        else:
            self.gph = None
    
    def InitUI(self):
        self.SetTitle('查询工具 -- {}'.format(self.env))
        self.SetSize(size=(900, 600))
        panel = wx.Panel(self, -1)
        mainBox = wx.BoxSizer(wx.VERTICAL)

        envBox = wx.BoxSizer()
        envText = wx.StaticText(panel, label=u'请选择您使用的链: ')
        self.testnetCheck = wx.RadioButton(panel, -1, env[1], style=wx.RB_GROUP) 
        self.prodCheck = wx.RadioButton(panel, -1, env[0]) 
        self.customizeCheck = wx.RadioButton(panel, -1, env[2]) 
        self.customizeChainText = wx.TextCtrl(panel, value=nodeAddresses[env[2]], size = (180, 20))

        self.customizeCheck.Bind(wx.EVT_RADIOBUTTON, self.on_customize_env) 
        self.testnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_testnet_env) 
        self.prodCheck.Bind(wx.EVT_RADIOBUTTON, self.on_prod_env) 

        envBox.Add(envText, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.prodCheck, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.testnetCheck, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.customizeCheck, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.customizeChainText, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        
        mainBox.Add(envBox)

        self.inputBox = wx.BoxSizer(wx.HORIZONTAL)
        paramsText = wx.StaticText(panel, label=u"输入  ")
        self.textInput = wx.TextCtrl(panel, size = (400, 22))
        self.inputBox.Add(paramsText, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        self.inputBox.Add(self.textInput, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 1)
        mainBox.Add(self.inputBox)

        self.queryAccountButton = wx.Button(panel, label = 'get_account')
        self.objectIDButton = wx.Button(panel, label = 'get_object')
        self.balanceButton = wx.Button(panel, label = 'account_balances')
        self.propertiesButton = wx.Button(panel, label = 'properties')
        self.clearButton = wx.Button(panel, label = '清空')

        self.Bind(wx.EVT_BUTTON, self.on_get_account, self.queryAccountButton)
        self.Bind(wx.EVT_BUTTON, self.on_get_object, self.objectIDButton)
        self.Bind(wx.EVT_BUTTON, self.on_list_account_balances, self.balanceButton)
        self.Bind(wx.EVT_BUTTON, self.on_properties, self.propertiesButton)
        self.Bind(wx.EVT_BUTTON, self.on_clear, self.clearButton)

        operationBox = wx.BoxSizer(wx.HORIZONTAL)
        operationBox.Add(self.queryAccountButton, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        operationBox.Add(self.objectIDButton, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        operationBox.Add(self.balanceButton, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        operationBox.Add(self.propertiesButton, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        operationBox.Add(self.clearButton, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)

        mainBox.Add(operationBox)

        self.textShow = wx.TextCtrl(panel, size = (1000, 768), style = wx.TE_MULTILINE | wx.HSCROLL)
        mainBox.Add(self.textShow, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 1)

        panel.SetSizer(mainBox) 
        self._thread = Thread(target = self.run, args = ())
        self._thread.daemon = True
        self._thread.start()
        self.started = True

        self.Show(True)

    def run(self):
        while True:
            try:
                if self.gph:
                    info = self.gph.info()
                    head_block_number = info['head_block_number']
                    self.updateDisplay(head_block_number)
            except Exception as e:
                print(repr(e))
            time.sleep(2)

    @call_after
    def updateDisplay(self, message):
        self.SetTitle('查询工具 -- {} | {}'.format(self.env, message))

    def on_customize_env(self, event):
        value = self.customizeChainText.GetValue()
        if value.startswith("ws"):
            nodeAddresses[env[2]] = value
        self.on_env(self.customizeCheck.GetLabel())

    def on_testnet_env(self, event):
        self.on_env(self.testnetCheck.GetLabel())

    def on_prod_env(self, event):
        self.on_env(self.prodCheck.GetLabel())

    def on_env(self, value):
        self.env = value
        self.nodeAddress = nodeAddresses[self.env]
        self.initGraphene(self.nodeAddress)
        self.SetTitle('查询工具 -- {}'.format(self.env))

    def on_clear(self, event):
        self.textInput.Clear()
        self.textShow.Clear()

    def on_show_text(self, method, params=[], is_clear_text=True):
        jsonText = request_post2(self.nodeAddress, method, params)
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
        self.on_show_text(method="get_dynamic_global_properties", is_clear_text=False)
        if len(is_simple) > 0:
            self.on_show_text(method="get_chain_properties", is_clear_text=False)
            self.on_show_text(method="get_global_properties", is_clear_text=False)
            self.on_show_text(method="get_config", is_clear_text=False)

def Main():
    app = wx.App()
    WalletFrame(None)
    app.MainLoop()

if __name__ == "__main__":
    Main()

