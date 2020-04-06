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

from config import *

# env = [ "mainnet", "testnet", "customize"]
# node_addresses = {
#     env[0]: "wss://api.cocosbcx.net",
#     env[1]: "wss://test.cocosbcx.net", 
#     env[2]: "ws://127.0.0.1:8049"
# }

def json_dumps(json_data):
    return json.dumps(json_data, indent=4)

def call_after(func):
    def _wrapper(*args, **kwargs):
        return wx.CallAfter(func, *args, **kwargs)
    return _wrapper

# 自定义窗口类WalletFrame
class WalletFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(WalletFrame, self).__init__(*args, **kwargs)
        # self.Center()
        # self.titleLock = Lock()
        self.env = env[1] #default testnet
        self.node_address = node_addresses[self.env]
        self.initGraphene(self.node_address, self.env)
        self.InitUI()

    def initGraphene(self, node_address, chain):
        print("init graphene: {} {}".format(node_address, chain))
        if ping(node=node_address, num_retries=1):
            print("init graphene 2222")
            self.gph = Graphene(node=node_address, num_retries=1, chain=chain) 
            set_shared_graphene_instance(self.gph)
        else:
            self.gph = None

    def InitUI(self):
        super().__init__(parent=None, title="pWallet", size=(900, 600))
        self.SetTitle('桌面钱包 -- {}'.format(self.env))
        self.SetSize(size=(900, 600))
        self.Center()

        sp_window = wx.SplitterWindow(parent=self, id=-1)
        self.panel_left = wx.Panel(parent=sp_window, name="Wallet")
        self.panel_right = wx.Panel(parent=sp_window, name="Commands")

        # 设置左右布局的分割窗口self.panel_left和self.panel_right
        sp_window.SplitVertically(self.panel_left, self.panel_right, 300)
        # 设置最小窗格大小，左右布局指左边窗口大小
        sp_window.SetMinimumPaneSize(80)

        # 为self.panel_left面板设置一个布局管理器
        left_boxsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_left.SetSizer(left_boxsizer)

        self.chain_boxsizer = self.create_chain_BoxSizer(self.panel_left)
        self.tree = self.create_TreeCtrl(self.panel_left)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.wallet_tree_on_click, self.tree)

        left_boxsizer.Add(self.chain_boxsizer, 1, flag=wx.EXPAND | wx.ALL, border=5)
        left_boxsizer.Add(self.tree, 9, flag=wx.EXPAND | wx.ALL, border=5)


        # 为self.panel_right面板设置一个布局管理器
        # default static_text
        self.right_boxsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_right.SetSizer(self.right_boxsizer)

        self.right_staticText_BoxSizer = wx.BoxSizer()
        self.right_static_text = wx.StaticText(self.panel_right, 2, label='Commands')
        self.right_staticText_BoxSizer.Add(self.right_static_text, 1, flag=wx.EXPAND | wx.ALL, border=5)

        self.right_boxsizer.Add(self.right_staticText_BoxSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        # self.right_boxsizer.Add(self.right_label_BoxSizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        self._thread = Thread(target = self.run, args = ())
        self._thread.daemon = True
        self._thread.start()
        self.started = True
 
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
        self.SetTitle('桌面钱包 -- {} | 区块高度：{}'.format(self.env, message))

    def on_customize_env(self, event):
        value = self.customizeChainText.GetValue()
        print("on_customize_env: {}".format(value))
        if value.startswith("ws"):
            node_addresses[env[2]] = value
        self.on_env(self.customizeCheck.GetLabel())

    def on_testnet_env(self, event):
        self.on_env(self.testnetCheck.GetLabel())

    def on_mainnet_env(self, event):
        self.on_env(self.mainnetCheck.GetLabel())

    def on_env(self, value):
        self.env = value
        self.node_address = node_addresses[value]
        print("on_customize_env: {} {}".format(self.env, self.node_address))
        self.initGraphene(self.node_address, value)
        self.SetTitle('桌面钱包 -- {}'.format(value))

    def wallet_tree_on_click(self, event):
        item = event.GetItem()
        # 根据不同的item，显示不同的参数列表
        # 无参command直接显示结果，有参参数列表，弹窗确认，执行后，显示命令和结果
        item_str = self.tree.GetItemText(item)
        status, result = self.wallet_tree_on_click_impl(item_str)
        if status:
            context = '>>> {}\n{}'.format(item_str, result)
            # if item_str == 'info':
            #     context += json_dumps(self.gph.info())
            # self.right_static_text.SetLabel(self.tree.GetItemText(item))
            self.right_static_text.SetLabel(context)

 
    def wallet_tree_on_click_impl(self, cmd_str):
        cmd = cmd_str.strip()
        result = ''
        status = True
        if cmd == 'info':
            result = self.gph.info()
        elif cmd == 'get_account':
            # label and label BoxSizer | 水平
            self.right_label_BoxSizer = wx.BoxSizer()
            cmd_label = wx.StaticText(self.panel_right, style=wx.ALIGN_CENTER, label=cmd)
            self.right_label_BoxSizer.Add(cmd_label, proportion=1, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, border=5)

            # param_list and param_list BoxSizer | 垂直
            self.right_param_BoxSizer = wx.BoxSizer(wx.VERTICAL)
            param1_label = wx.StaticText(self.panel_right, label="Account Name or ID")
            # self.right_param_BoxSizer.Add(param1_label, proportion=2, flag=wx.EXPAND|wx.ALL, border=5)
            self.right_param_BoxSizer.Add(param1_label, flag=wx.EXPAND|wx.ALL, border=5)
            self.param1_input_text = wx.TextCtrl(self.panel_right, value='eg: 1.2.3 or null-account')
            # self.right_param_BoxSizer.Add(self.param1_input_text, proportion=8, flag=wx.EXPAND|wx.ALL, border=5)
            self.right_param_BoxSizer.Add(self.param1_input_text, flag=wx.EXPAND|wx.ALL, border=5)

            # Buttons | 水平
            self.right_buttons_BoxSizer = wx.BoxSizer(wx.VERTICAL)
            self.cmd_ok_button = wx.Button(self.panel_right, label='OK')
            # self.right_buttons_BoxSizer.Add(self.cmd_ok_button, proportion=6, flag=wx.EXPAND|wx.ALL, border=5)
            self.right_buttons_BoxSizer.Add(self.cmd_ok_button, flag=wx.ALIGN_RIGHT, border=5)
            # self.buttonBox.Add(self.sendButton, proportion=2, flag=wx.EXPAND|wx.ALL, border=5)
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_account, self.cmd_ok_button)


            # result
            self.right_output_BoxSizer = wx.BoxSizer()
            self.output_text = wx.TextCtrl(self.panel_right, size = (1000, 768), style = wx.TE_MULTILINE | wx.HSCROLL)
            self.right_output_BoxSizer.Add(self.output_text, proportion=0, flag=wx.EXPAND|wx.ALL, border=5)

            # layout
            self.panel_right.SetSizer(self.right_boxsizer)
            # self.right_boxsizer.Add(self.right_label_BoxSizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
            # self.right_boxsizer.Add(self.right_param_BoxSizer, proportion=4, flag=wx.EXPAND|wx.ALL, border=5)
            # self.right_boxsizer.Add(self.right_buttons_BoxSizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
            # self.right_boxsizer.Add(self.right_output_BoxSizer, proportion=4, flag=wx.EXPAND|wx.ALL, border=5)
            self.right_boxsizer.Add(self.right_label_BoxSizer, flag=wx.EXPAND|wx.ALL, border=5)
            self.right_boxsizer.Add(self.right_param_BoxSizer, flag=wx.EXPAND|wx.ALL, border=5)
            self.right_boxsizer.Add(self.right_buttons_BoxSizer, flag=wx.EXPAND|wx.ALL, border=5)
            self.right_boxsizer.Add(self.right_output_BoxSizer, flag=wx.EXPAND|wx.ALL, border=5)

            self.right_boxsizer.Hide(self.right_staticText_BoxSizer)
            self.right_boxsizer.Layout()

            status = False
        
        if status:
            try:
                result = json_dumps(result)
            except Exception as e:
                result = '{} exception. {}'.format(cmd_str, repr(e))
        return status, result

    def show_output_text(self, text, is_clear_text=True):
        if is_clear_text:
            self.output_text.Clear()
        self.output_text.AppendText(text)
        self.output_text.AppendText('\n')

    def cmd_button_on_click_get_account(self, event):
        name = self.param1_input_text.GetValue()
        if len(name.split(".")) == 3:
            text = self.gph.rpc.get_object(name)
        else:
            account = Account(name)
            text = account.accounts_cache[name]
        self.show_output_text(json_dumps(text))

    def create_chain_BoxSizer(self, parent):
        chain_staticBox = wx.StaticBox(parent, label=u'请选择您使用的链: ')
        chain_boxsizer = wx.StaticBoxSizer(chain_staticBox, wx.VERTICAL)
        self.testnetCheck = wx.RadioButton(chain_staticBox, -1, env[1], style=wx.RB_GROUP) 
        self.mainnetCheck = wx.RadioButton(chain_staticBox, -1, env[0]) 
        self.customizeCheck = wx.RadioButton(chain_staticBox, -1, env[2]) 
        self.customizeChainText = wx.TextCtrl(chain_staticBox, value=node_addresses[env[2]], size = (180, 20))

        self.customizeCheck.Bind(wx.EVT_RADIOBUTTON, self.on_customize_env) 
        self.testnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_testnet_env) 
        self.mainnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_mainnet_env) 

        chain_boxsizer.Add(self.mainnetCheck, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        chain_boxsizer.Add(self.testnetCheck, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        chain_boxsizer.Add(self.customizeCheck, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        chain_boxsizer.Add(self.customizeChainText, proportion = 0,flag = wx.EXPAND|wx.ALL, border = 3)
        return chain_boxsizer

    def create_TreeCtrl(self, parent):
        tree = wx.TreeCtrl(parent)

        # 通过wx.ImageList()创建一个图像列表img_list并保存在树中
        img_list = wx.ImageList(16, 16, True, 2)
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        tree.AssignImageList(img_list)

        # 创建根节点和5个子节点并展开
        root = tree.AddRoot('钱包命令', image=0)
        item_wallet = tree.AppendItem(root, 'wallet', 0)
        item_chain = tree.AppendItem(root, 'chain', 0)
        item_account = tree.AppendItem(root, 'account', 0)
        item_asset = tree.AppendItem(root, 'asset', 0)
        item_contract = tree.AppendItem(root, 'contract', 0)
        item_transaction = tree.AppendItem(root, 'transaction', 0)
        item_file = tree.AppendItem(root, 'file', 0)
        tree.Expand(root)
        tree.SelectItem(root)
 
        # chain
        tree.AppendItem(item_chain, 'info', 1)
        tree.Expand(item_chain)

        # 给item_wallet节点添加5个子节点并展开
        for command in wallet_wallet_commands:
            tree.AppendItem(item_wallet, command, 1)
        # tree.AppendItem(item_wallet, 'lock', 1)
        # tree.AppendItem(item_wallet, 'unlock', 1)
        # tree.AppendItem(item_wallet, 'set_password', 1)
        # tree.AppendItem(item_wallet, 'get_accounts', 1)
        # tree.AppendItem(item_wallet, 'suggest_brain_key', 1)
        tree.Expand(item_wallet)
 
        # 给item_account节点添加5个子节点并展开
        tree.AppendItem(item_account, 'get_account', 1)
        tree.AppendItem(item_account, 'list_account_balances', 1)
        tree.AppendItem(item_account, 'create_account', 1)
        tree.AppendItem(item_account, 'update_account', 1)
        tree.Expand(item_account)
 
        # 返回树对象
        return tree
 
 
class App(wx.App):
    def OnInit(self):
        # 创建窗口对象
        frame = WalletFrame()
        frame.Show()
        return True
 
    def OnExit(self):
        print("应用程序退出")
        return 0
 
 
if __name__ == '__main__':
    app = App()
    app.MainLoop()

