#coding=utf-8 
   
import wx 
   
class MyFrame(wx.Frame): 
   
    def __init__(self): 
        wx.Frame.__init__(self,None,-1,"多模测试热补丁工具",size = (800,600)) 
        panel = wx.Panel(self) 
        #第一种方法使用wx.RadioButton类 
        self.check1 = wx.RadioButton(panel,-1,"BPN2",pos = (50,20),size = (50,20),style = wx.RB_GROUP) 
        self.check2 = wx.RadioButton(panel, -1, "BPL1", pos=(100,20), size=(50, 20)) 
        self.check3 = wx.RadioButton(panel, -1, "BPC", pos=(150,20), size=(50, 20)) 
        self.check4 = wx.RadioButton(panel, -1, "RRU1", pos=(50,40), size=(50, 20), style=wx.RB_GROUP) 
        self.check5 = wx.RadioButton(panel, -1, "RRU2", pos=(100,40), size=(50, 20)) 
        self.check6 = wx.RadioButton(panel, -1, "RRU3", pos=(150,40), size=(50, 20)) 
        self.check1.Bind(wx.EVT_RADIOBUTTON,self.One_Play) 
        self.check4.Bind(wx.EVT_RADIOBUTTON, self.Two_Play) 
        #第二种方法使用wx.RadioBox类 
        list1 = ["BPN2","BPL1" ,"BPC"] 
        list2 = ["RRU1", "RRU2", "RRU3"] 
        self.radiobox1 = wx.RadioBox(panel,-1,"基带板选择",(50,80),(200, 20),list1,3,wx.RA_SPECIFY_COLS) 
        self.radiobox2 = wx.RadioBox(panel, -1, "射频设备选择", (50, 150), (200, 20), list2, 3, wx.RA_SPECIFY_ROWS) 
        self.radiobox1.Bind(wx.EVT_RADIOBOX,self.Three_Play) 
        self.radiobox2.Bind(wx.EVT_RADIOBOX, self.End_Play) 
   
    def One_Play(self,event): 
        # print("本次选择了吗：",self.check1.GetLabel() )
        pass
   
    def Two_Play(self,event): 
        # print("本次选择了吗：", self.check4.GetLabel() )
        pass
   
    def Three_Play(self,event): 
        pass
        # print ("本次选择了吗：", self.radiobox1.GetStringSelection(),self.radiobox1.GetSelection() )
   
   
    def End_Play(self,event): 
        pass
        # print self.radiobox2.GetStringSelection() 
   
if __name__ == "__main__": 
    app = wx.App() 
    frame = MyFrame() 
    frame.Show() 
    app.MainLoop() 