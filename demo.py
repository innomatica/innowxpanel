#!/usr/bin/env python3
import wx
from innocom.innocom import InnoCom
from innompl.innompl import InnoMpl

if __name__=="__main__":

    class MyFrame(wx.Frame):

        def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title=title)

            # notebook
            self.nbkMain = wx.Notebook(self,-1)
            # panel page
            self.pnlTerm = InnoCom(self.nbkMain)
            self.nbkMain.AddPage(self.pnlTerm, "innocom")
            self.pnlGrp = InnoMpl(self.nbkMain)
            self.nbkMain.AddPage(self.pnlGrp, "innompl")

            # menu events
            self.Bind(wx.EVT_CLOSE, self.OnClose)

            # sizer
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(self.nbkMain,1, wx.EXPAND)

            self.SetSizer(self.sizer)
            self.SetAutoLayout(1)
            self.sizer.Fit(self)
            self.Show()


        def OnClose(self, evt):
            # destroy self
            self.Destroy()


    app = wx.App()
    frame = MyFrame(None, "InnoPanel Demo")

    app.MainLoop()
