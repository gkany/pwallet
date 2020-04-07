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
from utils import *

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

        left_boxsizer.Add(self.chain_boxsizer, 1, flag=wx.EXPAND | wx.ALL, border=3)
        left_boxsizer.Add(self.tree, 9, flag=wx.EXPAND | wx.ALL, border=3)


        # 为self.panel_right面板设置一个布局管理器
        # default static_text
        self.right_boxsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_right.SetSizer(self.right_boxsizer)

        # self.right_staticText_BoxSizer = wx.BoxSizer()
        # self.right_static_text = wx.StaticText(self.panel_right, 2, label='Commands')
        # self.right_staticText_BoxSizer.Add(self.right_static_text, 1, flag=wx.EXPAND | wx.ALL, border=3)

        # self.right_boxsizer.Add(self.right_staticText_BoxSizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
        # self.right_boxsizer.Add(self.right_label_BoxSizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=3)

        ##### test start
        # label and label BoxSizer | 水平
        self.right_label_BoxSizer = wx.BoxSizer()
        self.cmd_label = wx.StaticText(self.panel_right, style=wx.ALIGN_CENTER, label='commands')
        self.right_label_BoxSizer.Add(self.cmd_label, proportion=1, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, border=3)

        # param_list and param_list BoxSizer | 垂直
        self.right_param_BoxSizer = wx.BoxSizer(wx.VERTICAL)

        # Buttons | 水平
        self.right_buttons_BoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.cmd_ok_button = wx.Button(self.panel_right, label='执行')
        self.right_buttons_BoxSizer.Add(self.cmd_ok_button, flag=wx.ALIGN_RIGHT, border=3)

        # result
        self.right_output_BoxSizer = wx.BoxSizer()
        self.output_text = wx.TextCtrl(self.panel_right, size = (1000, 768), style = wx.TE_MULTILINE | wx.HSCROLL)
        self.right_output_BoxSizer.Add(self.output_text, proportion=0, flag=wx.EXPAND|wx.ALL, border=3)

        # layout
        self.panel_right.SetSizer(self.right_boxsizer)
        self.right_boxsizer.Add(self.right_label_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Add(self.right_param_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Add(self.right_buttons_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Add(self.right_output_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)

        # self.right_boxsizer.Hide(self.right_staticText_BoxSizer)
        # self.right_boxsizer.Layout()
        ##### test end

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
                    block_msg = "区块高度：{}".format(head_block_number)

                    wallet_status = self.gph.wallet.created()
                    if wallet_status:
                        locked_status = self.gph.wallet.locked()
                        if locked_status:
                            show_msg = "{} | 钱包已锁定".format(block_msg)
                        else:
                            show_msg = "{} | 钱包已解锁".format(block_msg)
                    else:
                        show_msg = "{} | 钱包未创建".format(block_msg)
            except Exception as e:
                show_msg = repr(e)
            # print(show_msg)
            self.updateDisplay(show_msg)
            time.sleep(2)

    @call_after
    def updateDisplay(self, message):
        self.SetTitle('桌面钱包 -- {} | {}'.format(self.env, message))

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
        self.output_text.Clear()
        item = event.GetItem()
        item_str = self.tree.GetItemText(item)
        print(">>> {}".format(item_str))
        self.cmd_label.SetLabel(item_str)
        result = self.wallet_tree_on_click_impl(item_str)
        if len(result) > 0:
            self.show_output_text(result)

    def param_item_BoxSizer(self, parent_panel, label_note):
        item_BoxSizer = wx.BoxSizer() # 水平: [label, input]
        param_label = wx.StaticText(parent_panel, label=label_note[0])
        item_BoxSizer.Add(param_label, proportion=2, flag=wx.EXPAND|wx.ALL, border=3)
        param_input_text = wx.TextCtrl(parent_panel, value=label_note[1])
        item_BoxSizer.Add(param_input_text, proportion=8, flag = wx.EXPAND|wx.ALL, border=3)
        return item_BoxSizer, param_input_text

    def param_item_BoxSizer_v(self, parent_panel, label_note):
        # item_BoxSizer = wx.BoxSizer(wx.VERTICAL)
        param1_label = wx.StaticText(parent_panel, label=label_note[0])
        # item_BoxSizer.Add(param1_label, flag=wx.EXPAND|wx.ALL, border=3)
        param_input_text = wx.TextCtrl(parent_panel, value=label_note[1])
        # item_BoxSizer.Add(param_input_text, flag=wx.EXPAND|wx.ALL, border=3)
        return param1_label, param_input_text


    def wallet_tree_on_click_impl(self, cmd_str):
        # clear param BoxSizer
        self.right_boxsizer.Hide(self.right_param_BoxSizer)
        self.right_boxsizer.Layout()

        cmd = cmd_str.strip()
        result = ''
        # layout
        if cmd in no_params_commands:
            pass 
        elif cmd in one_params_commands:
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, cmd_param_notes[cmd])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)
            # self.right_boxsizer.Layout()
        elif cmd in two_params_commands:
            notes = cmd_param_notes[cmd]
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, notes[0])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer2, self.param2_input_text = self.param_item_BoxSizer(self.panel_right, notes[1])
            self.right_param_BoxSizer.Add(item_BoxSizer2, flag=wx.EXPAND|wx.ALL, border=3)
            # self.right_boxsizer.Layout()
        elif cmd in three_params_commands:
            notes = cmd_param_notes[cmd]
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, notes[0])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer2, self.param2_input_text = self.param_item_BoxSizer(self.panel_right, notes[1])
            self.right_param_BoxSizer.Add(item_BoxSizer2, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer3, self.param3_input_text = self.param_item_BoxSizer(self.panel_right, notes[2])
            self.right_param_BoxSizer.Add(item_BoxSizer3, flag=wx.EXPAND|wx.ALL, border=3)
            # self.right_boxsizer.Layout()
        elif cmd in four_params_commands:
            notes = cmd_param_notes[cmd]
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, notes[0])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer2, self.param2_input_text = self.param_item_BoxSizer(self.panel_right, notes[1])
            self.right_param_BoxSizer.Add(item_BoxSizer2, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer3, self.param3_input_text = self.param_item_BoxSizer(self.panel_right, notes[2])
            self.right_param_BoxSizer.Add(item_BoxSizer3, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer4, self.param4_input_text = self.param_item_BoxSizer(self.panel_right, notes[3])
            self.right_param_BoxSizer.Add(item_BoxSizer4, flag=wx.EXPAND|wx.ALL, border=3)
            # self.right_boxsizer.Layout()
        elif cmd in five_params_commands:
            notes = cmd_param_notes[cmd]
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, notes[0])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer2, self.param2_input_text = self.param_item_BoxSizer(self.panel_right, notes[1])
            self.right_param_BoxSizer.Add(item_BoxSizer2, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer3, self.param3_input_text = self.param_item_BoxSizer(self.panel_right, notes[2])
            self.right_param_BoxSizer.Add(item_BoxSizer3, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer4, self.param4_input_text = self.param_item_BoxSizer(self.panel_right, notes[3])
            self.right_param_BoxSizer.Add(item_BoxSizer4, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer5, self.param5_input_text = self.param_item_BoxSizer(self.panel_right, notes[4])
            self.right_param_BoxSizer.Add(item_BoxSizer5, flag=wx.EXPAND|wx.ALL, border=3)
            # self.right_boxsizer.Layout()
        elif cmd in six_params_commands:
            notes = cmd_param_notes[cmd]
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, notes[0])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer2, self.param2_input_text = self.param_item_BoxSizer(self.panel_right, notes[1])
            self.right_param_BoxSizer.Add(item_BoxSizer2, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer3, self.param3_input_text = self.param_item_BoxSizer(self.panel_right, notes[2])
            self.right_param_BoxSizer.Add(item_BoxSizer3, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer4, self.param4_input_text = self.param_item_BoxSizer(self.panel_right, notes[3])
            self.right_param_BoxSizer.Add(item_BoxSizer4, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer5, self.param5_input_text = self.param_item_BoxSizer(self.panel_right, notes[4])
            self.right_param_BoxSizer.Add(item_BoxSizer5, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer6, self.param6_input_text = self.param_item_BoxSizer(self.panel_right, notes[5])
            self.right_param_BoxSizer.Add(item_BoxSizer6, flag=wx.EXPAND|wx.ALL, border=3)
        elif cmd in seven_params_commands:
            notes = cmd_param_notes[cmd]
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, notes[0])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer2, self.param2_input_text = self.param_item_BoxSizer(self.panel_right, notes[1])
            self.right_param_BoxSizer.Add(item_BoxSizer2, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer3, self.param3_input_text = self.param_item_BoxSizer(self.panel_right, notes[2])
            self.right_param_BoxSizer.Add(item_BoxSizer3, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer4, self.param4_input_text = self.param_item_BoxSizer(self.panel_right, notes[3])
            self.right_param_BoxSizer.Add(item_BoxSizer4, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer5, self.param5_input_text = self.param_item_BoxSizer(self.panel_right, notes[4])
            self.right_param_BoxSizer.Add(item_BoxSizer5, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer6, self.param6_input_text = self.param_item_BoxSizer(self.panel_right, notes[5])
            self.right_param_BoxSizer.Add(item_BoxSizer6, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer7, self.param7_input_text = self.param_item_BoxSizer(self.panel_right, notes[6])
            self.right_param_BoxSizer.Add(item_BoxSizer7, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Layout()

        # bind button event
        if cmd == 'info':
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_info, self.cmd_ok_button)
            result = self.gph.info()
        elif cmd == "suggest_brain_key":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_suggest_key, self.cmd_ok_button)
            result = self.gph.suggest_key()
        elif cmd == 'list_my_accounts':
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_list_my_accounts, self.cmd_ok_button)
            result = self.gph.wallet.getAccounts()
        elif cmd == 'get_account':
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_account, self.cmd_ok_button)
        elif cmd == 'list_account_balances':
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_account_balances, self.cmd_ok_button)
        elif cmd == 'get_object':
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_unlock, self.cmd_ok_button)
        elif cmd == "get_asset":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_asset, self.cmd_ok_button)
        elif cmd == "unlock":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_unlock, self.cmd_ok_button)
        elif cmd == "set_password":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_unlock, self.cmd_ok_button)
        elif cmd == "lock":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_lock, self.cmd_ok_button)
            result = self.gph.wallet.lock()
        elif cmd == "transfer":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_transfer, self.cmd_ok_button)
        elif cmd == "create_account":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_create_account, self.cmd_ok_button)
        try:
            result = json_dumps(result)
        except Exception as e:
            result = '{} exception. {}'.format(cmd_str, repr(e))
        return result


    def wallet_tree_on_click_impl_old(self, cmd_str):
        # clear param BoxSizer
        self.right_boxsizer.Hide(self.right_param_BoxSizer)
        self.right_boxsizer.Layout()

        cmd = cmd_str.strip()
        result = ''
        if cmd == 'info':
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_info, self.cmd_ok_button)
            result = self.gph.info()
        elif cmd == "suggest_brain_key":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_suggest_key, self.cmd_ok_button)
            result = self.gph.suggest_key()
        elif cmd == 'list_my_accounts':
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_list_my_accounts, self.cmd_ok_button)
            result = self.gph.wallet.getAccounts()
        elif cmd == 'get_account':
            # param
            # param1_label = wx.StaticText(self.panel_right, label="Account Name or ID")
            # self.right_param_BoxSizer.Add(param1_label, flag=wx.EXPAND|wx.ALL, border=3)
            # self.param1_input_text = wx.TextCtrl(self.panel_right, value='eg: 1.2.3 or null-account')
            # self.right_param_BoxSizer.Add(self.param1_input_text, flag=wx.EXPAND|wx.ALL, border=3)

            # self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_account, self.cmd_ok_button)
            # self.right_boxsizer.Layout()

            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, cmd_param_notes[cmd])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_account, self.cmd_ok_button)
            self.right_boxsizer.Layout()
        elif cmd == 'list_account_balances':
            # param
            # param1_label = wx.StaticText(self.panel_right, label="Account Name or ID")
            # self.right_param_BoxSizer.Add(param1_label, flag=wx.EXPAND|wx.ALL, border=3)
            # self.param1_input_text = wx.TextCtrl(self.panel_right, value='eg: 1.2.3 or null-account')
            # self.right_param_BoxSizer.Add(self.param1_input_text, flag=wx.EXPAND|wx.ALL, border=3)

            # self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_account_balances, self.cmd_ok_button)
            # self.right_boxsizer.Layout()
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, cmd_param_notes[cmd])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_account_balances, self.cmd_ok_button)
            self.right_boxsizer.Layout()
        elif cmd == 'get_object':
            # param
            # param1_label = wx.StaticText(self.panel_right, label=cmd_param_notes[cmd][0])
            # self.right_param_BoxSizer.Add(param1_label, flag=wx.EXPAND|wx.ALL, border=3)
            # self.param1_input_text = wx.TextCtrl(self.panel_right, value=cmd_param_notes[cmd][1])
            # self.right_param_BoxSizer.Add(self.param1_input_text, flag=wx.EXPAND|wx.ALL, border=3)
            # self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_object, self.cmd_ok_button)
            # self.right_boxsizer.Layout()
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, cmd_param_notes[cmd])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_unlock, self.cmd_ok_button)
            self.right_boxsizer.Layout()
        elif cmd == "get_asset":
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, cmd_param_notes[cmd])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_asset, self.cmd_ok_button)
            self.right_boxsizer.Layout()
        elif cmd == "unlock":
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, cmd_param_notes[cmd])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_unlock, self.cmd_ok_button)
            self.right_boxsizer.Layout()
        elif cmd == "set_password":
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, cmd_param_notes[cmd])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_unlock, self.cmd_ok_button)
            self.right_boxsizer.Layout()
        elif cmd == "lock":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_lock, self.cmd_ok_button)
            result = self.gph.wallet.lock()
        elif cmd == "transfer":
            notes = cmd_param_notes[cmd]
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, notes[0])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer2, self.param2_input_text = self.param_item_BoxSizer(self.panel_right, notes[1])
            self.right_param_BoxSizer.Add(item_BoxSizer2, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer3, self.param3_input_text = self.param_item_BoxSizer(self.panel_right, notes[2])
            self.right_param_BoxSizer.Add(item_BoxSizer3, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer4, self.param4_input_text = self.param_item_BoxSizer(self.panel_right, notes[3])
            self.right_param_BoxSizer.Add(item_BoxSizer4, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer5, self.param5_input_text = self.param_item_BoxSizer(self.panel_right, notes[4])
            self.right_param_BoxSizer.Add(item_BoxSizer5, flag=wx.EXPAND|wx.ALL, border=3)

            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_transfer, self.cmd_ok_button)
            self.right_boxsizer.Layout()
        elif cmd == "create_account":
            notes = cmd_param_notes[cmd]
            item_BoxSizer1, self.param1_input_text = self.param_item_BoxSizer(self.panel_right, notes[0])
            self.right_param_BoxSizer.Add(item_BoxSizer1, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer2, self.param2_input_text = self.param_item_BoxSizer(self.panel_right, notes[1])
            self.right_param_BoxSizer.Add(item_BoxSizer2, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer3, self.param3_input_text = self.param_item_BoxSizer(self.panel_right, notes[2])
            self.right_param_BoxSizer.Add(item_BoxSizer3, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer4, self.param4_input_text = self.param_item_BoxSizer(self.panel_right, notes[3])
            self.right_param_BoxSizer.Add(item_BoxSizer4, flag=wx.EXPAND|wx.ALL, border=3)

            item_BoxSizer5, self.param5_input_text = self.param_item_BoxSizer(self.panel_right, notes[4])
            self.right_param_BoxSizer.Add(item_BoxSizer5, flag=wx.EXPAND|wx.ALL, border=3)

            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_create_account, self.cmd_ok_button)
            self.right_boxsizer.Layout()
        try:
            result = json_dumps(result)
        except Exception as e:
            result = '{} exception. {}'.format(cmd_str, repr(e))
        return result


    def show_output_text(self, text, is_clear_text=True):
        print("text: {}".format(text))
        if is_clear_text:
            self.output_text.Clear()
        self.output_text.SetValue(text)
        self.output_text.AppendText('\n')

    def cmd_button_on_click_unlock(self, event):
        password = self.param1_input_text.GetValue().strip()
        if len(password) == 0:
            password = "123456" # default
        try:
            self.gph.wallet.unlock(password)
            text = "钱包解锁成功!"
        except Exception as e:
            text = "钱包解锁失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_lock(self, event):
        try:
            self.gph.wallet.lock()
            text = "钱包锁定成功!"
        except Exception as e:
            text = "钱包锁定失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_setpassword(self, event):
        password = self.param1_input_text.GetValue().strip()
        if len(password) == 0:
            password = "123456" # default
        try:
            self.gph.wallet.changePassphrase(password)
            text = "钱包重置密码成功!"
        except Exception as e:
            text = "钱包重置密码失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_get_account(self, event):
        name = self.param1_input_text.GetValue()
        print("name: {}".format(name))
        try:
            if len(name.split(".")) == 3:
                text = self.gph.rpc.get_object(name)
            else:
                account = Account(name)
                text = account.accounts_cache[name]
            text = json_dumps(text)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_get_object(self, event):
        object_id = self.param1_input_text.GetValue()
        object_id = object_id.strip()
        print("name: {}".format(object_id))
        try:
            if len(object_id.split(".")) == 3:
                text = self.gph.rpc.get_object(object_id)
            else:
                text = 'param({}) error'.format(object_id)
            text = json_dumps(text)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_get_asset(self, event):
        asset_symbol_or_id = self.param1_input_text.GetValue().strip()
        # asset_symbol_or_id = self.params_input[0].GetValue().strip()
        print("name: {}".format(asset_symbol_or_id))
        try:
            text = json_dumps(self.gph.rpc.get_asset(asset_symbol_or_id))
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_transfer(self, event):
        from_account = self.param1_input_text.GetValue().strip()
        to_account = self.param2_input_text.GetValue().strip()
        amount = self.param3_input_text.GetValue().strip()
        asset = self.param4_input_text.GetValue().strip()
        memo = self.param5_input_text.GetValue().strip()
        try:
            result = self.gph.transfer(to_account, amount, asset, [memo, 0], from_account)
            text = json_dumps(result)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_create_account(self, event):
        account_name = self.param1_input_text.GetValue().strip()
        owner_key = self.param2_input_text.GetValue().strip()
        active_key = self.param3_input_text.GetValue().strip()
        memo_key = self.param4_input_text.GetValue().strip()
        register = self.param5_input_text.GetValue().strip()
        try:
            result = self.gph.create_account(account_name=name, registrar=registrar,
                        owner_key=owner_key, active_key=active_key, memo_key=memo_key)
            text = json_dumps(result)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_account_balances(self, event):
        name = self.param1_input_text.GetValue()
        print("name: {}".format(name))
        try:
            account = Account(name)
            text = []
            for balance in account.balances:
                text.append({
                    'symbol': balance['symbol'],
                    'amount': balance['amount']
                })
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_list_my_accounts(self, event):
        try:
            accounts = self.gph.wallet.getAccounts()
            text = json_dumps(accounts)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_info(self, event):
        try:
            text = json_dumps(self.gph.info())
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_suggest_key(self, event):
        try:
            text = json_dumps(self.gph.suggest_key())
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

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
 
        # tree item
        for command in wallet_chain_commands:
            tree.AppendItem(item_chain, command, 1)
        tree.Expand(item_chain)

        for command in wallet_wallet_commands:
            tree.AppendItem(item_wallet, command, 1)
        tree.Expand(item_wallet)
 
        for command in wallet_account_commands:
            tree.AppendItem(item_account, command, 1)
        tree.Expand(item_account)

        for command in wallet_asset_commands:
            tree.AppendItem(item_asset, command, 1)
        tree.Expand(item_asset)

        for command in wallet_contract_commands:
            tree.AppendItem(item_contract, command, 1)
        tree.Expand(item_contract)
 
        # 返回树对象
        return tree
 
 
class App(wx.App):
    def OnInit(self):
        frame = WalletFrame()  # 创建窗口对象
        frame.Show()
        return True
 
    def OnExit(self):
        print("应用程序退出")
        return 0
 
 
if __name__ == '__main__':
    app = App()
    app.MainLoop()

