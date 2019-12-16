#-*- coding: utf-8  -*-

import wx
import time
import json
import requests
from wx.lib.pubsub import pub
from threading import Thread, Lock

from graphsdk.graphene import Graphene, ping
from graphsdk.account import Account
from graphsdk.instance import set_shared_graphene_instance

env = [ u"主网", u"测试网(默认)", u"自定义"]
nodeAddresses = {
    env[0]: "wss://api.cocosbcx.net",
    env[1]: "wss://test.cocosbcx.net", 
    env[2]: "ws://127.0.0.1:8049"
}

common_api = ["info", "get_account", "get_object"]
wallet_api = ["create_wallet", "lock", "unlock"]
chain_api = ["get_account", "get_object", "account_balances"]


def json_dumps(json_data):
    return json.dumps(json_data, indent=4)

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
        self.SetTitle('测试工具 -- {}'.format(self.env))
        self.SetSize(size=(900, 600))

        mainBox = wx.BoxSizer(wx.VERTICAL)

        env_panel = wx.Panel(self, -1)
        envBox = wx.BoxSizer()
        envText = wx.StaticText(env_panel, label=u'请选择您使用的链: ')
        self.testnetCheck = wx.RadioButton(env_panel, -1, env[1], style=wx.RB_GROUP) 
        self.prodCheck = wx.RadioButton(env_panel, -1, env[0]) 
        self.customizeCheck = wx.RadioButton(env_panel, -1, env[2]) 
        self.customizeChainText = wx.TextCtrl(env_panel, value=nodeAddresses[env[2]], size = (180, 20))

        self.customizeCheck.Bind(wx.EVT_RADIOBUTTON, self.on_customize_env) 
        self.testnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_testnet_env) 
        self.prodCheck.Bind(wx.EVT_RADIOBUTTON, self.on_prod_env) 

        envBox.Add(envText, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.prodCheck, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.testnetCheck, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.customizeCheck, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        envBox.Add(self.customizeChainText, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)
        
        mainBox.Add(envBox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        tree_panel = wx.Panel(self, -1)
        cmd_panel = wx.Panel(self, -1)
        
        self.tree = wx.TreeCtrl(tree_panel, 1, wx.DefaultPosition, (-1, -1), 
                                wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        root = self.tree.AddRoot('wallet list')
        common_item = self.tree.AppendItem(root, '常用')
        wallet_item = self.tree.AppendItem(root, '钱包')
        chain_item = self.tree.AppendItem(root, '链')

        for api in common_api:
            self.tree.AppendItem(common_item, api)

        for api in wallet_api:
            self.tree.AppendItem(wallet_item, api)

        for api in chain_api:
            self.tree.AppendItem(chain_item, api)

        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, 
                       self.OnSelChanged, id=1)
        self.display = wx.StaticText(cmd_panel, -1, '', 
                                     (10, 10), style=wx.ALIGN_CENTER)
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(tree_panel, 1, wx.EXPAND)
        hbox.Add(cmd_panel, 1, wx.EXPAND)
        tree_panel.SetSizer(vbox)

        mainBox.Add(vbox)

        self.SetSizer(mainBox)
        self.Center()
        self.Show(True)

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
        self.SetTitle('桌面钱包 -- {}'.format(self.env))

    def OnSelChanged(self, event):
        item = event.GetItem()
        self.display.SetLabel(self.tree.GetItemText(item))

def Main():
    app = wx.App()
    WalletFrame(None)
    app.MainLoop()

if __name__ == "__main__":
    Main()

