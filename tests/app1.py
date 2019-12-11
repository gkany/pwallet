#coding=utf-8
import wx
 
class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self)
 
    def OnInit(self):
        self.frame = wx.Frame(parent=None,title = "多模自动化测试工具",pos = (520,250),size = (800,600))
        panel = wx.Panel(self.frame,-1)
        self.SetTopWindow(self.frame)
 
 
        label = wx.StaticText(panel,label = "相关测试人员周强，负责RRU与BBU的自动化测试",pos=(50,500),size=(800,50),style=wx.ALIGN_CENTER)
        font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        label.SetFont(font)
        #lbl.SetLabel(txt)
        label.SetBackgroundColour("balck")
        label.SetForegroundColour("red")
 
 
        self.button = wx.Button(panel, -1, "上传版本", pos=(500, 20),size=(150,40))
        self.button.SetFont(font)
        self.Bind(wx.EVT_BUTTON,self.one_play,self.button)
 
        inputext = wx.TextCtrl(panel,-1,"请您输入版本路径：",pos=(200,20),size = (200,30))
        inputext.SetInsertionPoint(0)
 
        # bmp = wx.Image("timg.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        # self.button1 = wx.BitmapButton(panel, -1, bmp, pos=(-1, 240), size=(-1, -1))
        # self.button1.Bind(wx.EVT_LEFT_DOWN,self.two_play)
 
 
        self.frame.Show()
        return True
 
    def one_play(self,event):
        print("这是第一次")
        self.button.SetLabel("版本上传成功")
 
    def two_play(self,event):
        print("这是第二次")
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()