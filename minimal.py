#!/usr/bin/env python3
import wx
from innocom.innocom import InnoCom

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        panel = InnoCom(self)
        self.Show()

app = wx.App()
MyFrame(None)
app.MainLoop()
