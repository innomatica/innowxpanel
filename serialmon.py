#!/usr/bin/env python3
from innocom.innocom import InnoCom
from innowpl.innowpl import InnoWpl

import serial
import numpy as np

import wx
import numpy as np


if __name__=="__main__":

    class MyFrame(wx.Frame):

        def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title=title)

            # notebook
            self.nbkMain = wx.Notebook(self,-1)
            # panel page
            self.pnlTerm = InnoCom(self.nbkMain)
            self.nbkMain.AddPage(self.pnlTerm, "innocom")
            self.pnlWGrp = InnoWpl(self.nbkMain)
            self.nbkMain.AddPage(self.pnlWGrp, "innowpl")

            # demo plots
            self.DrawGraphs()

            # timer event and serial object
            self.tmr = wx.Timer(self)
            self.ser = serial.Serial('COM25', 115200)
            self.t = 0.

            # menu events
            self.Bind(wx.EVT_CLOSE, self.OnClose)
            # timer event
            self.Bind(wx.EVT_TIMER, self.OnTimer)

            # sizer
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(self.nbkMain,1, wx.EXPAND)

            self.SetSizer(self.sizer)
            self.SetAutoLayout(1)
            self.sizer.Fit(self)
            self.Show()
            self.tmr.Start(1000)

        def OnTimer(self, evt):
            # 16bit sine waveform with period of 100
            v = (np.sin(2 * np.pi * self.t) + 1) * 32767
            #print('v, int(v), hex', v, int(v), format(int(v), '04x'))
            self.ser.write(bytes.fromhex(format(int(v), '04x')))
            self.t = self.t + 0.01

        def DrawGraphs(self):

            # wxpython panel
            from wx.lib import plot as wxplot

            x = np.linspace(0,10,500)
            y = np.sin(x)

            # create lines
            line1 = wxplot.PolyLine(list(zip(x, np.sin(x))),
                    colour='red', width=3, style=wx.PENSTYLE_DOT_DASH)
            line2 = wxplot.PolyLine(list(zip(x, -np.sin(x))),
                    colour='blue', width=3, style=wx.PENSTYLE_LONG_DASH)

            # create a graphics
            graphics = wxplot.PlotGraphics([line1, line2], 'PolyLine plot',
                    'y axis', 'x axis')
            self.pnlWGrp.Draw(graphics)

        def OnClose(self, evt):
            # destroy self
            self.Destroy()


    app = wx.App()
    frame = MyFrame(None, "InnoPanel Demo")

    app.MainLoop()
