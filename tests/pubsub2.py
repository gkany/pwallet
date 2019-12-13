import time
import wx
  
from threading import Thread
# from wx.lib.pubsub import Publisher
from wx.lib.pubsub import pub
 
def call_after(func):
    def _wrapper(*args, **kwargs):
        return wx.CallAfter(func, *args, **kwargs)
    return _wrapper
 
class MyForm(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial")
  
        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.displayLbl = wx.StaticText(panel, label="Amount of time since thread started goes here")
        self.btn = btn = wx.Button(panel, label="Start Thread")
  
        btn.Bind(wx.EVT_BUTTON, self.onButton)
  
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.displayLbl, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)
  
        self._thread = Thread(target = self.run, args = ())
        self._thread.daemon = True
         
 
    def run(self):
        i = 0
        while True:
            i += 1
            time.sleep(1)
            self.updateDisplay('Seconds: %d' % i)
 
    #----------------------------------------------------------------------
    def onButton(self, event):
        """
        Runs the thread
        """
        self._thread.start()
        self.started = True
        self.displayLbl.SetLabel("Thread started!")
        btn = event.GetEventObject()
        btn.Disable()
 
    @call_after
    def updateDisplay(self, msg):
        """
        Receives data from thread and updates the display
        """
        self.displayLbl.SetLabel(msg)
  
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyForm().Show()
    app.MainLoop()