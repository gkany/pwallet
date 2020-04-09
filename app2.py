#-*- coding: utf-8  -*-

import wx
import wx.adv
import time
import json
import requests
from wx.lib.pubsub import pub
from threading import Thread, Lock

from graphsdk.graphene import Graphene, ping
from graphsdk.account import Account
from graphsdk.contract import Contract
from graphsdk.instance import set_shared_graphene_instance
from graphsdk.storage import init_storage
from eggs import cherry_forever, get_random_verse

from config import *
from utils import *

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
        # self.titleLock = Lock()
        self.env = env[1] #default testnet
        self.node_address = node_addresses[self.env]
        self.faucet_url = faucet_urls[self.env]
        self.initGraphene(self.node_address, self.env)
        self.InitUI()

    def initGraphene(self, node_address, current_chain):
        print("init graphene: {} {}".format(node_address, current_chain))
        # global g_current_chain
        # g_current_chain = current_chain
        init_storage(current_chain) # init storage
        if ping(node=node_address, num_retries=1):
            print("init graphene 2222")
            self.gph = Graphene(node=node_address, num_retries=1, current_chain=current_chain) 
            set_shared_graphene_instance(self.gph)
        else:
            self.gph = None

    def InitUI(self):
        super().__init__(parent=None, title="pWallet", size=(900, 600))
        self.SetTitle('桌面钱包 -- {}'.format(self.env))
        self.walletlogo = wx.Icon('./icons/walletlogo.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.walletlogo)  

        # self.taskBar_icon = wx.adv.TaskBarIcon()
        # self.taskBar_icon.SetIcon(self.walletlogo, "pWallet")

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
                    # print("wallet_status: {}".format(wallet_status))
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
    def updateDisplay(self, msg):
        title = '桌面钱包 -- {} | {}              {}'.format(self.env, msg, get_random_verse())
        self.SetTitle(title)

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

        # global g_current_chain
        # g_current_chain = self.env
        init_storage(self.env) # init storage

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
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_object, self.cmd_ok_button)
        elif cmd == "get_asset":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_asset, self.cmd_ok_button)
        elif cmd == "unlock":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_unlock, self.cmd_ok_button)
        elif cmd == "new_wallet":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_new_wallet, self.cmd_ok_button)
        elif cmd == "import_key":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_import_key, self.cmd_ok_button)
        elif cmd == "getAccountFromPublicKey":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_getAccountFromPublicKey, self.cmd_ok_button)
        elif cmd == "getPrivateKeyForPublicKey":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_getPrivateKeyForPublicKey, self.cmd_ok_button)
        elif cmd == "set_password":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_setpassword, self.cmd_ok_button)
        elif cmd == "lock":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_lock, self.cmd_ok_button)
            result = self.gph.wallet.lock()
        elif cmd == "transfer":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_transfer, self.cmd_ok_button)
        elif cmd == "create_account":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_create_account, self.cmd_ok_button)
        elif cmd == "update_collateral_for_gas":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_collateral_gas, self.cmd_ok_button)
        elif cmd == "get_account_history":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_account_history, self.cmd_ok_button)
        elif cmd == "get_contract":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_contract, self.cmd_ok_button)
        elif cmd == "get_transaction_by_id":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_tx_by_id, self.cmd_ok_button)
        elif cmd == "get_transaction_in_block_info":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_tx_in_block_info, self.cmd_ok_button)
        elif cmd == "get_chain_properties":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_info, self.cmd_ok_button)
            result = self.gph.rpc.get_chain_properties()
        elif cmd == "get_global_properties":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_info, self.cmd_ok_button)
            result = self.gph.rpc.get_global_properties()
        elif cmd == "get_config":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_info, self.cmd_ok_button)
            result = self.gph.rpc.get_config()
        elif cmd ==  "get_chain_id":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_info, self.cmd_ok_button)
            result = self.gph.rpc.get_chain_id()
        elif cmd == "get_dynamic_global_properties":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_info, self.cmd_ok_button)
            result = self.gph.rpc.get_dynamic_global_properties()
        elif cmd == "get_block":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_get_block, self.cmd_ok_button)
        elif cmd == "faucet_register_account":
            self.Bind(wx.EVT_BUTTON, self.cmd_button_on_click_faucet_register_account, self.cmd_ok_button)

        if cmd == u"钱包命令":
            try:
                cherry_forever()
            except Exception as e:
                print("cherry_forever exception: {}".format(repr(e)))

        try:
            result = json_dumps(result)
        except Exception as e:
            result = '{} exception. {}'.format(cmd_str, repr(e))
        return result

    def show_output_text(self, text, is_clear_text=True):
        print("text: {}".format(text))
        if is_clear_text:
            self.output_text.Clear()
        self.output_text.AppendText(text+'\n')
        # self.output_text.AppendText('\n')

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

    def cmd_button_on_click_import_key(self, event):
        private_key = self.param1_input_text.GetValue().strip()
        try:
            self.gph.wallet.addPrivateKey(private_key)
            text = "导入私钥成功!"
        except Exception as e:
            text = "导入私钥失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_getPrivateKeyForPublicKey(self, event):
        public_key = self.param1_input_text.GetValue().strip()
        try:
            result = self.gph.wallet.getPrivateKeyForPublicKey(public_key)
            text = json_dumps(result)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_getAccountFromPublicKey(self, event):
        public_key = self.param1_input_text.GetValue().strip()
        try:
            result = self.gph.wallet.getAccountFromPublicKey(public_key)
            text = json_dumps(result)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_import_key(self, event):
        private_key = self.param1_input_text.GetValue().strip()
        try:
            self.gph.wallet.addPrivateKey(private_key)
            text = "导入私钥成功!"
        except Exception as e:
            text = "导入私钥失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_new_wallet(self, event):
        password = self.param1_input_text.GetValue().strip()
        if len(password) == 0:
            password = "123456" # default
        try:
            self.gph.newWallet(password)
            text = "钱包创建成功!"
        except Exception as e:
            text = "钱包创建失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_get_block(self, event):
        number = self.param1_input_text.GetValue().strip()
        try:
            result = self.gph.rpc.get_block(int(number))
            text = json_dumps(result)
        except Exception as e:
            text = repr(e)
        self.show_output_text(text)

    def cmd_button_on_click_faucet_register_account(self, event):
        account_name = self.param1_input_text.GetValue().strip()
        try:
            brain_key = self.gph.suggest_key()
            owner_key = brain_key["owner_key"]
            brain_key_json = json_dumps(brain_key)
            print(brain_key_json)
            req_data = {
                "account":{
                    "name": account_name,
                    "owner_key": owner_key,
                    "active_key": owner_key,
                    "id":1
                }
            }
            response = json.loads(requests.post(self.faucet_url, data=json.dumps(req_data), headers=faucet_headers).text)
            text = {
                "brain_key": brain_key,
                "faucet_response": response
            }
            # text = '{\n"brain_key": %s, \n"faucet_response": %s\n}' % (brain_key_json, json_dumps(response))
            text = json_dumps(text)
        except Exception as e:
            text = repr(e)
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
                # account = Account(name)
                # text = account.accounts_cache[name]
                text = self.gph.rpc.get_account_by_name(name)
            text = json_dumps(text)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_get_contract(self, event):
        name_or_id = self.param1_input_text.GetValue().strip()
        print("name: {}".format(name_or_id))
        try:
            # if len(name_or_id.split(".")) == 3:
            #     text = self.gph.rpc.get_object(name_or_id)
            # else:
            contract = Contract(name_or_id)
            text = contract.contracts_cache[name_or_id]
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

    def cmd_button_on_click_tx_by_id(self, event):
        tx_id = self.param1_input_text.GetValue().strip()
        try:
            text = json_dumps(self.gph.rpc.get_transaction_by_id(tx_id))
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_tx_in_block_info(self, event):
        tx_id = self.param1_input_text.GetValue().strip()
        try:
            text = json_dumps(self.gph.rpc.get_transaction_in_block_info(tx_id))
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

    def cmd_button_on_click_account_history(self, event):
        name_or_id = self.param1_input_text.GetValue().strip()
        limit = self.param2_input_text.GetValue().strip()
        start, stop  = "1.11.0", "1.11.0"
        if limit == "":
            limit = 5
        else:
            limit = min(100, int(limit))
        try:
            if len(name_or_id.split(".")) == 3:
                account_object = self.gph.rpc.get_object(name_or_id)
            else:
                account = Account(name_or_id)
                account_object = account.accounts_cache[name_or_id]
            result = self.gph.rpc.get_account_history(account_object['id'], stop, limit, start, api="history")
            text = json_dumps(result)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def cmd_button_on_click_collateral_gas(self, event):
        from_account = self.param1_input_text.GetValue().strip()
        beneficiary = self.param2_input_text.GetValue().strip()
        collateral = self.param3_input_text.GetValue().strip()
        try:
            result = self.gph.update_collateral_for_gas(beneficiary, int(collateral), from_account)
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
            text = json_dumps(text)
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
        img_list = wx.ImageList(16, 16, True, 3)
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        # img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        # img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, size=(16, 16)))

        # openedFolder128px.ico
        # openedFolder = wx.Icon('./icons/openedFolder128px.ico', wx.BITMAP_TYPE_ICO) 
        # img_list.Add(openedFolder)

        unchecked = wx.Icon('./icons/unchecked26px.ico', wx.BITMAP_TYPE_ICO) 
        checked = wx.Icon('./icons/checked26px.ico', wx.BITMAP_TYPE_ICO) 
        # checked = wx.Icon('./icons/checked16px.ico', wx.BITMAP_TYPE_ICO) 

        img_list.Add(unchecked)
        img_list.Add(checked)
        tree.AssignImageList(img_list)

        # 创建根节点和子节点并展开
        root = tree.AddRoot(text=u"钱包命令", image=0, selImage=2)
        item_faucet = tree.AppendItem(parent=root, text="faucet", image=0, selImage=2)
        item_wallet = tree.AppendItem(parent=root, text="wallet", image=0, selImage=2)
        item_chain = tree.AppendItem(parent=root, text="chain", image=0, selImage=2)
        item_account = tree.AppendItem(parent=root, text="account", image=0, selImage=2)
        item_asset = tree.AppendItem(parent=root, text="asset", image=0, selImage=2)
        item_contract = tree.AppendItem(parent=root, text="contract", image=0, selImage=2)
        item_transaction = tree.AppendItem(parent=root, text="transaction", image=0, selImage=2)
        item_file = tree.AppendItem(parent=root, text="file", image=0, selImage=2)
        tree.Expand(root)
        tree.SelectItem(root)
 
        # tree item
        for cmd in faucet_commands:
            tree.AppendItem(parent=item_faucet, text=cmd, image=1, selImage=2)
        tree.Expand(item_faucet)

        for cmd in wallet_chain_commands:
            tree.AppendItem(parent=item_chain, text=cmd, image=1, selImage=2)
        tree.Expand(item_chain)

        for cmd in wallet_wallet_commands:
            tree.AppendItem(parent=item_wallet, text=cmd, image=1, selImage=2)
        tree.Expand(item_wallet)
 
        for cmd in wallet_account_commands:
            tree.AppendItem(parent=item_account, text=cmd, image=1, selImage=2)
        tree.Expand(item_account)

        for cmd in wallet_asset_commands:
            tree.AppendItem(parent=item_asset, text=cmd, image=1, selImage=2)
        tree.Expand(item_asset)

        for cmd in wallet_contract_commands:
            tree.AppendItem(parent=item_contract, text=cmd, image=1, selImage=2)
        tree.Expand(item_contract)

        for cmd in wallet_transaction_commands:
            tree.AppendItem(parent=item_transaction, text=cmd, image=1, selImage=2)
        tree.Expand(item_transaction)

        for cmd in wallet_file_commands:
            tree.AppendItem(parent=item_file, text=cmd, image=1, selImage=2)
 
        # 返回树对象
        return tree
 
 
class App(wx.App):
    def OnInit(self):
        frame = WalletFrame()
        frame.Show()
        return True
 
    def OnExit(self):
        return 0
 
def Main():
    app = App()
    app.MainLoop()
 
if __name__ == '__main__':
    Main()

