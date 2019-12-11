import wx
from utils import *
import time

class PWallet(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(PWallet, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        #File
        fileMenu = wx.Menu()
        newItem = fileMenu.Append(wx.ID_ANY, "New", "")
        openItem = fileMenu.Append(wx.ID_ANY, "Open", "")
        fileMenu.AppendSeparator()
        saveItem = fileMenu.Append(wx.ID_ANY, "Save", "")
        saveAsItem = fileMenu.Append(wx.ID_ANY, "Save As", "")
        fileMenu.AppendSeparator()
        # operationItem = fileMenu.Append(wx.ID_ANY, "Operation", "")
        infoItem = fileMenu.Append(wx.ID_ANY, "Info", "")

        exitItem = fileMenu.Append(wx.ID_EXIT, "Exit", "exit application")

        #Wallet        
        walletMenu = wx.Menu()
        #View
        viewMenu = wx.Menu()
        #Help
        helpMenu = wx.Menu()

        #Bind -- file menu
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.on_info, infoItem)
        
        #Application MenuBar
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(walletMenu, "&Wallet")
        menuBar.Append(viewMenu, "&View")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        self.SetTitle('PWallet')
        self.control = wx.TextCtrl(self, -1, '', style=wx.TE_MULTILINE)

        self.Show(True)

    def OnExit(self, e):
        self.Close()

    # get_dynamic_global_properties 
    def on_info(self, e):
        req_data = {
            "method": "get_dynamic_global_properties",
            "params": [],
            "id":1
        }
        status, result = request_post(req_data)
        if status:
            dynamic_global_properties = json_dumps(result)
            self.control.Clear()
            self.control.AppendText(dynamic_global_properties)
            # time.sleep(2)
    
def Main():
    app = wx.App()
    PWallet(None)
    app.MainLoop()

if __name__ == "__main__":
    Main()