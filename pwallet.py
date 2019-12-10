import wx

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
        exitItem = fileMenu.Append(wx.ID_EXIT, "Exit", "exit application")

        #Wallet        
        walletMenu = wx.Menu()
        #View
        viewMenu = wx.Menu()
        #Help
        helpMenu = wx.Menu()

        #Bind -- file menu
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

        #Application MenuBar
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(walletMenu, "&Wallet")
        menuBar.Append(viewMenu, "&View")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        self.SetTitle('PWallet')
        self.Show(True)

    def OnExit(self, e):
        self.Close()

def Main():
    app = wx.App()
    PWallet(None)
    app.MainLoop()

if __name__ == "__main__":
    Main()