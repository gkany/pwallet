#-*- coding: utf-8  -*-

import wx
import wx.adv
import time
import sys
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
from logmanager import LogManager


def json_dumps(json_data):
    return json.dumps(json_data, indent=4)

def call_after(func):
    def _wrapper(*args, **kwargs):
        return wx.CallAfter(func, *args, **kwargs)
    return _wrapper

log_manager = LogManager(config_path="./", add_time=True)


class MainFrame(wx.Frame):

    FRAMES_MIN_SIZE = (900, 600)
    API_BUTTON_CLICK_EVENT_PREFIX_ = "api_button_on_click_"

    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)

        #default testnet
        self.current_chain = TESTNET_CHAIN 
        self.faucet_url = FAUCET_CONFIG[self.current_chain] + FAUCET_ROUTE
        self.init_sdk()
        self.layout_mainframe()

    def _on_close(self, event):
        """Event handler for the wx.EVT_CLOSE event.

        This method is used when the user tries to close the program
        to save the options and make sure that the download & update
        processes are not running.

        """

        if APP_CONFIRM_EXIT:
            dlg = wx.MessageDialog(self, "Are you sure you want to exit?", "Exit", wx.YES_NO | wx.ICON_QUESTION)

            result = dlg.ShowModal() == wx.ID_YES
            dlg.Destroy()
        else:
            result = True

        if result:
            self.close()

    def close(self):
        self.Destroy()

    def status_bar_write(self, msg):
        """Display msg in the status bar. """
        self.status_bar.SetStatusText(msg)

    def title_write(self, title="桌面钱包"):
        self.SetTitle(title)

    def init_sdk(self):
        chain = CHAIN_CONFIG[self.current_chain]
        log_manager.log("init sdk. current chain: {}".format(chain))
        init_storage(self.current_chain) # init storage
        if ping(node=chain["address"], num_retries=1):
            self.gph = Graphene(node=chain["address"], num_retries=1, current_chain=self.current_chain) 
            set_shared_graphene_instance(self.gph)
        else:
            self.gph = None

    def layout_mainframe(self):
        super().__init__(parent=None, title="pWallet", size=(900, 600))
        self.title_write('桌面钱包 -- {}'.format(self.current_chain))
        # self.walletlogo = wx.Icon('./icons/walletlogo.ico', wx.BITMAP_TYPE_ICO)
        # self.SetIcon(self.walletlogo)  

        # Set the app icon
        app_icon_path = get_icon_file()
        if app_icon_path is not None:
            self.app_icon = wx.Icon(app_icon_path, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.app_icon)

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
        # self.chain_boxsizer = self.create_chain_BoxSizer_by_radioBox(self.panel_left)
        self.tree = self.create_TreeCtrl(self.panel_left)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.wallet_tree_on_click, self.tree)

        left_boxsizer.Add(self.chain_boxsizer, 1, flag=wx.EXPAND | wx.ALL, border=3)
        left_boxsizer.Add(self.tree, 9, flag=wx.EXPAND | wx.ALL, border=3)

        # 为self.panel_right面板设置一个布局管理器
        # default static_text
        self.right_boxsizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_right.SetSizer(self.right_boxsizer)

        # label and label BoxSizer | 水平
        self.right_label_BoxSizer = wx.BoxSizer()
        self.api_label = wx.StaticText(self.panel_right, style=wx.ALIGN_CENTER, label='钱包命令')
        self.right_label_BoxSizer.Add(self.api_label, proportion=1, flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER, border=3)

        # param_list and param_list BoxSizer | 垂直
        self.right_param_BoxSizer = wx.BoxSizer(wx.VERTICAL)

        # Buttons | 水平
        self.right_buttons_BoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.api_button_ok = wx.Button(self.panel_right, label='执行')
        self.right_buttons_BoxSizer.Add(self.api_button_ok, flag=wx.ALIGN_RIGHT, border=3)

        # result
        self.right_output_BoxSizer = wx.BoxSizer()
        self.output_text = wx.TextCtrl(self.panel_right, size=(1000, 768), style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_RICH|wx.TE_PROCESS_ENTER)
        self.right_output_BoxSizer.Add(self.output_text, proportion=0, flag=wx.EXPAND|wx.ALL, border=3)

        # layout
        self.panel_right.SetSizer(self.right_boxsizer)
        self.right_boxsizer.Add(self.right_label_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Add(self.right_param_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Add(self.right_buttons_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)
        self.right_boxsizer.Add(self.right_output_BoxSizer, flag=wx.EXPAND|wx.ALL, border=3)

        self.status_bar = self.CreateStatusBar()
        # Bind extra events
        self.Bind(wx.EVT_CLOSE, self._on_close)

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
                    # log_manager.log("wallet_status: {}".format(wallet_status))
                    if wallet_status:
                        locked_status = self.gph.wallet.locked()
                        if locked_status:
                            title_msg = "{} | 钱包已锁定".format(block_msg)
                        else:
                            title_msg = "{} | 钱包已解锁".format(block_msg)
                    else:
                        title_msg = "{} | 钱包未创建".format(block_msg)
                else:
                    title_msg = "节点无法连接"
            except Exception as e:
                title_msg = repr(e)
            # log_manager.log(title_msg)
            self.updateDisplay(title_msg)
            self.status_bar_write(get_random_verse())
            time.sleep(2)

    @call_after
    def updateDisplay(self, msg):
        # title = '桌面钱包 -- {} | {}              {}'.format(self.current_chain, msg, get_random_verse())
        title = '桌面钱包 -- {} | {}'.format(self.current_chain, msg)
        self.SetTitle(title)

    # current chain set
    def on_customize_chain(self, event):
        self.change_chain(chain_name=CUSTOMIZE_CHAIN)

    def on_testnet_chain(self, event):
        self.change_chain(chain_name=TESTNET_CHAIN)

    def on_mainnet_chain(self, event):
        self.change_chain(chain_name=MAINNET_CHAIN)

    def change_chain(self, chain_name):
        log_manager.log("change_chain event: {}-->{}".format(self.current_chain, chain_name))
        if chain_name == CUSTOMIZE_CHAIN:
            addresses = self.customizeChainText.GetValue().strip()
            tokens = addresses.split(",")
            if len(tokens) >= 1:
                chain_address = tokens[0]
                if chain_address.startswith("ws"):
                    CHAIN_CONFIG[CUSTOMIZE_CHAIN]["address"] = chain_address
                
                if len(tokens) >= 2:
                    faucet_url = tokens[1]
                    if faucet_url.startswith("http"):
                        FAUCET_CONFIG[CUSTOMIZE_CHAIN] = faucet_url
        self.current_chain = chain_name
        self.faucet_url = FAUCET_CONFIG[chain_name] + FAUCET_ROUTE
        init_storage(chain_name) # init storage
        self.init_sdk()
        self.title_write('桌面钱包 -- {}'.format(chain_name))

    def create_chain_BoxSizer(self, parent):
        chain_staticBox = wx.StaticBox(parent, label=u'请选择您使用的链: ')
        chain_boxsizer = wx.StaticBoxSizer(chain_staticBox, wx.VERTICAL)
        self.testnetCheck = wx.RadioButton(chain_staticBox, -1, TESTNET_CHAIN, style=wx.RB_GROUP) 
        self.mainnetCheck = wx.RadioButton(chain_staticBox, -1, MAINNET_CHAIN) 
        self.customizeCheck = wx.RadioButton(chain_staticBox, -1, CUSTOMIZE_CHAIN) 

        default = "{},{}".format(CHAIN_CONFIG[CUSTOMIZE_CHAIN]["address"], FAUCET_CONFIG[CUSTOMIZE_CHAIN])
        self.customizeChainText = wx.TextCtrl(chain_staticBox, value=default, size=(180, 20))

        self.customizeCheck.Bind(wx.EVT_RADIOBUTTON, self.on_customize_chain) 
        self.testnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_testnet_chain) 
        self.mainnetCheck.Bind(wx.EVT_RADIOBUTTON, self.on_mainnet_chain) 

        chain_boxsizer.Add(self.mainnetCheck, proportion=0, flag=wx.EXPAND|wx.ALL, border=3)
        chain_boxsizer.Add(self.testnetCheck, proportion=0, flag=wx.EXPAND|wx.ALL, border=3)
        chain_boxsizer.Add(self.customizeCheck, proportion=0,flag=wx.EXPAND|wx.ALL, border=3)
        chain_boxsizer.Add(self.customizeChainText, proportion=0,flag=wx.EXPAND|wx.ALL, border=3)
        return chain_boxsizer


    def create_TreeCtrl(self, parent):
        tree = wx.TreeCtrl(parent)

        # create image list
        img_list = wx.ImageList(16, 16, True, 3)
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        # img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        # img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        # unchecked = wx.Icon('./icons/unchecked26px.ico', wx.BITMAP_TYPE_ICO) 
        # checked = wx.Icon('./icons/checked26px.ico', wx.BITMAP_TYPE_ICO) 
        # img_list.Add(unchecked)
        # img_list.Add(checked)

        tree_img_data = (
            ("unchecked", "unchecked26px.ico"),
            ("checked", "checked26px.ico")
        )
        self._img_path = get_icons_dir()
        for item in tree_img_data:
            target, name = item
            img_list.Add(wx.Icon(os.path.join(self._img_path, name), wx.BITMAP_TYPE_ICO))
        tree.AssignImageList(img_list)

        # create api tree
        root = tree.AddRoot(text=u"钱包命令", image=0, selImage=2)
        # add api class
        self.on_use_api_class = []
        for class_name in API_CLASS:
            api_class_obj = API_CLASS[class_name]
            if api_class_obj["enable"]:
                item = tree.AppendItem(parent=root, text=class_name, image=0, selImage=2)
                item_name = "api_class_item_" + class_name
                setattr(self, item_name, item)
                self.on_use_api_class.append(class_name)
        
        # add api item
        for api_name in API_LIST:
            api_obj = API_LIST[api_name]
            class_name = api_obj["class"]
            if api_obj["enable"] and class_name in self.on_use_api_class:
                class_item_name = "api_class_item_" + class_name
                class_item = getattr(self, class_item_name)
                tree.AppendItem(parent=class_item, text=api_name, image=1, selImage=2)

                # init api empty param list
                if len(api_obj["params"]) == 0:
                    API_EMPTY_PARAM.append(api_name)

        # api class Expand or hide
        for class_name in API_CLASS:
            api_class_obj = API_CLASS[class_name]
            if api_class_obj["enable"]:
                class_item = getattr(self, "api_class_item_" + class_name)
                if api_class_obj["isExpand"]:
                    tree.Expand(class_item)

        tree.Expand(root)
        tree.SelectItem(root)
        return tree

    def wallet_tree_on_click(self, event):
        self.output_text.Clear()
        api_item = event.GetItem()
        item_name = self.tree.GetItemText(api_item).strip()
        log_manager.log(">>> api item name: {}".format(item_name))
        self.api_label.SetLabel(item_name)
        self.current_api_name = item_name
        result = self.wallet_tree_on_click_impl(item_name)
        # print("result: {}, len: {}, type: {}".format(result, len(result), type(result)))
        if result != '""':
            self.show_output_text(result)

    def gen_param_column(self, parent_panel, label_tip):
        boxsizer = wx.BoxSizer() # 水平: [label, input]
        param_label = wx.StaticText(parent_panel, label=label_tip[0])
        boxsizer.Add(param_label, proportion=2, flag=wx.EXPAND|wx.ALL, border=3)
        param_input_text = wx.TextCtrl(parent_panel, value=label_tip[1])
        boxsizer.Add(param_input_text, proportion=8, flag=wx.EXPAND|wx.ALL, border=3)
        return boxsizer, param_input_text

    def param_columns_layout(self, api_name):
        # clear param BoxSizer
        self.right_boxsizer.Hide(self.right_param_BoxSizer)
        self.right_boxsizer.Layout()

        if api_name in API_LIST:
            api_obj = API_LIST[api_name]
            # log_manager.log("params: {}".format(api_obj["params"]))
            params = api_obj["params"]
            for i in range(0, len(params)):
                column_text = "param{}_input_text".format(i+1)
                boxsizer, input_text = self.gen_param_column(self.panel_right, params[i])
                self.right_param_BoxSizer.Add(boxsizer, flag=wx.EXPAND|wx.ALL, border=3)
                setattr(self, column_text, input_text)
            self.right_boxsizer.Layout()

    def get_sdk_api(self, api_name):
        try:
            try:
                sdk_func = getattr(self.gph, api_name)
            except Exception as e:
                api_obj = API_LIST[api_name]
                # use api_obj["sdk_name"]  by sdk_name_index
                if api_obj["class"] == "wallet":
                    sdk_func = getattr(self.gph.wallet, api_name)
                else:
                    sdk_func = getattr(self.gph.rpc, api_name)
        except Exception as e:
            log_manager.log("[ERROR]get func failed. api_name:{}. {}".format(api_name, repr(e)))
            sdk_func = None
        return sdk_func

    def wallet_tree_on_click_impl(self, api_name):
        result = ""
        # param column layout
        self.param_columns_layout(api_name)
        
        # Button bind event
        if api_name not in API_CLASS:
            try:
                try:
                    func_name = self.API_BUTTON_CLICK_EVENT_PREFIX_ + api_name
                    bind_func = getattr(self, func_name)
                except Exception as e:
                    bind_func = self.api_button_on_click_default
                    log_manager.log("[WARN]bind use default. api_name: {}. {}".format(api_name, repr(e)))
                self.Bind(wx.EVT_BUTTON, bind_func, self.api_button_ok)

                if api_name in API_EMPTY_PARAM:
                    result = self.get_sdk_api(api_name)() # 不做判断，错误信息抛出
                    # sdk_func = self.get_sdk_api(api_name)
                    # if sdk_func:
                    #     result = sdk_func()
            except Exception as e:
                result = "run {} failed. {}".format(api_name, repr(e))
        else:
            result = API_CLASS[api_name]["desc"]
            log_manager.log("api_name: {}".format(api_name))

        if api_name == u"钱包命令":
            try:
                cherry_forever()
            except Exception as e:
                log_manager.log("cherry_forever exception: {}".format(repr(e)))

        try:
            result = json_dumps(result)
        except Exception as e:
            result = '{} exception. {}'.format(api_name, repr(e))
        return result

    def show_output_text(self, text, is_clear_text=True):
        # log_manager.log("text: {}".format(text))
        if is_clear_text:
            self.output_text.Clear()
        self.output_text.AppendText(text+'\n')
        # self.output_text.AppendText('\n')

    # Butten click event
    # default on click event
    def api_button_on_click_default(self, event):
        api_name = self.current_api_name
        api_obj = API_LIST[api_name]
        # params = api_obj["params"]
        args = []  # or {label:arg}
        size = len(api_obj["params"])
        for i in range(0, size):
            arg = "arg{}".format(i)
            input_text_obj_name = "param{}_input_text".format(i+1)
            input_text_obj = getattr(self, input_text_obj_name)
            value = input_text_obj.GetValue().strip()
            log_manager.log("input_text_obj_name: {}, value: {}", input_text_obj_name, value)
            args.append(value)

        sdk_func = self.get_sdk_api(api_name)
        if sdk_func:
            try:
                # sdk api args no support 变长参数
                if size == 0:
                    result = sdk_func()
                elif size == 1:
                    result = sdk_func(args[0])
                elif size == 2:
                    result = sdk_func(args[0], args[1])
                elif size == 3:
                    result = sdk_func(args[0], args[1], args[2])
                elif size == 4:
                    result = sdk_func(args[0], args[1], args[2], args[3])
                elif size == 5:
                    result = sdk_func(args[0], args[1], args[2], args[3], args[4])
                elif size == 6:
                    result = sdk_func(args[0], args[1], args[2], args[3], args[4], args[5])
                elif size == 7:
                    result = sdk_func(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
                elif size == 8:
                    result = sdk_func(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
                elif size == 9:
                    result = sdk_func(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8])
                else:
                    text = "{} api has too many args. button on_click default event no support! Please check api."
                if text is None:
                    text = "{} {} 执行成功!".format(api_name, args)
            except Exception as e:
                text = "{} {} 执行失败, {}".format(api_name, args, repr(e))
            self.show_output_text(text)
        else:
            result = "api_name: {}, sdk no api".format(api_name)

    ## faucet 
    def api_button_on_click_faucet_register_account(self, event):
        account_name = self.param1_input_text.GetValue().strip()
        try:
            brain_key = self.gph.suggest_key()
            owner_key = brain_key["owner_key"]
            brain_key_json = json_dumps(brain_key)
            log_manager.log(brain_key_json)
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

    ## wallet
    def api_button_on_click_new_wallet(self, event):
        password = self.param1_input_text.GetValue().strip()
        if len(password) == 0:
            password = "123456" # default
        try:
            self.gph.newWallet(password)
            text = "钱包创建成功!"
        except Exception as e:
            text = "钱包创建失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_unlock(self, event):
        password = self.param1_input_text.GetValue().strip()
        if len(password) == 0:
            password = "123456" # default
        try:
            self.gph.wallet.unlock(password)
            text = "钱包解锁成功!"
        except Exception as e:
            text = "钱包解锁失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_lock(self, event):
        try:
            self.gph.wallet.lock()
            text = "钱包锁定成功!"
        except Exception as e:
            text = "钱包锁定失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_setpassword(self, event):
        password = self.param1_input_text.GetValue().strip()
        if len(password) == 0:
            password = "123456" # default
        try:
            self.gph.wallet.changePassphrase(password)
            text = "钱包重置密码成功!"
        except Exception as e:
            text = "钱包重置密码失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_import_key(self, event):
        private_key = self.param1_input_text.GetValue().strip()
        try:
            self.gph.wallet.addPrivateKey(private_key)
            text = "导入私钥成功!"
        except Exception as e:
            text = "导入私钥失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_import_key(self, event):
        private_key = self.param1_input_text.GetValue().strip()
        try:
            self.gph.wallet.addPrivateKey(private_key)
            text = "导入私钥成功!"
        except Exception as e:
            text = "导入私钥失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_getAccounts(self, event):
        try:
            accounts = self.gph.wallet.getAccounts()
            text = json_dumps(accounts)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_suggest_key(self, event):
        try:
            text = json_dumps(self.gph.suggest_key())
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_getPrivateKeyForPublicKey(self, event):
        public_key = self.param1_input_text.GetValue().strip()
        try:
            result = self.gph.wallet.getPrivateKeyForPublicKey(public_key)
            text = json_dumps(result)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_getAccountFromPublicKey(self, event):
        public_key = self.param1_input_text.GetValue().strip()
        try:
            result = self.gph.wallet.getAccountFromPublicKey(public_key)
            text = json_dumps(result)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    ## chain api
    def api_button_on_click_info(self, event):
        try:
            text = json_dumps(self.gph.info())
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_get_object(self, event):
        object_id = self.param1_input_text.GetValue()
        object_id = object_id.strip()
        log_manager.log("name: {}".format(object_id))
        try:
            if len(object_id.split(".")) == 3:
                text = self.gph.rpc.get_object(object_id)
            else:
                text = 'param({}) error'.format(object_id)
            text = json_dumps(text)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_get_block(self, event):
        number = self.param1_input_text.GetValue().strip()
        try:
            result = self.gph.rpc.get_block(int(number))
            text = json_dumps(result)
        except Exception as e:
            text = repr(e)
        self.show_output_text(text)

    def api_button_on_click_get_config(self, event):
        try:
            text = json_dumps(self.gph.rpc.get_config())
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_get_chain_id(self, event):
        try:
            text = json_dumps(self.gph.rpc.get_chain_id())
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_get_chain_properties(self, event):
        try:
            text = json_dumps(self.gph.rpc.get_chain_properties())
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_get_global_properties(self, event):
        try:
            text = json_dumps(self.gph.rpc.get_global_properties())
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)
    
    def api_button_on_click_get_dynamic_global_properties(self, event):
        try:
            text = json_dumps(self.gph.rpc.get_dynamic_global_properties())
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    ## account api event
    def api_button_on_click_get_account(self, event):
        name = self.param1_input_text.GetValue()
        log_manager.log("name: {}".format(name))
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

    def api_button_on_click_transfer(self, event):
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

    def api_button_on_click_create_account(self, event):
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

    def api_button_on_click_account_balances(self, event):
        name = self.param1_input_text.GetValue()
        log_manager.log("name: {}".format(name))
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

    def api_button_on_click_get_account_history(self, event):
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

    def api_button_on_click_update_collateral_for_gas(self, event):
        from_account = self.param1_input_text.GetValue().strip()
        beneficiary = self.param2_input_text.GetValue().strip()
        collateral = self.param3_input_text.GetValue().strip()
        try:
            result = self.gph.update_collateral_for_gas(beneficiary, int(collateral), from_account)
            text = json_dumps(result)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    ## asset
    def api_button_on_click_get_asset(self, event):
        asset_symbol_or_id = self.param1_input_text.GetValue().strip()
        # asset_symbol_or_id = self.params_input[0].GetValue().strip()
        log_manager.log("name: {}".format(asset_symbol_or_id))
        try:
            text = json_dumps(self.gph.rpc.get_asset(asset_symbol_or_id))
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)
    
    ## contract api
    def api_button_on_click_get_contract(self, event):
        name_or_id = self.param1_input_text.GetValue().strip()
        log_manager.log("name: {}".format(name_or_id))
        try:
            if name_or_id.startswith("1.16."):
                text = self.gph.rpc.get_object(name_or_id)
            else:
                contract = Contract(name_or_id)
                text = contract.contracts_cache[name_or_id]
            text = json_dumps(text)
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    ## transaction
    '''
    def api_button_on_click_get_transaction_by_id(self, event):
        tx_id = self.param1_input_text.GetValue().strip()
        try:
            text = json_dumps(self.gph.rpc.get_transaction_by_id(tx_id))
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)

    def api_button_on_click_get_transaction_in_block_info(self, event):
        tx_id = self.param1_input_text.GetValue().strip()
        try:
            text = json_dumps(self.gph.rpc.get_transaction_in_block_info(tx_id))
        except Exception as e:
            text = "执行失败, {}".format(repr(e))
        self.show_output_text(text)
    '''

    ## file
 
class App(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show()
        return True
 
    def OnExit(self):
        return 0
 
def Main():
    app = App()
    app.MainLoop()
 
if __name__ == '__main__':
    Main()

