#!/usr/bin/env python3
from innocom.innocom import InnoCom
from innompl.innompl import InnoMpl
from innowpl.innowpl import InnoWpl

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
            self.pnlMGrp = InnoMpl(self.nbkMain)
            self.nbkMain.AddPage(self.pnlMGrp, "innompl")
            self.pnlWGrp = InnoWpl(self.nbkMain)
            self.nbkMain.AddPage(self.pnlWGrp, "innowpl")

            # demo plots
            self.DrawGraphs()

            # menu events
            self.Bind(wx.EVT_CLOSE, self.OnClose)

            # sizer
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(self.nbkMain,1, wx.EXPAND)

            self.SetSizer(self.sizer)
            self.SetAutoLayout(1)
            self.sizer.Fit(self)
            self.Show()

        def DrawGraphs(self):
            # matplotlib panel
            import matplotlib

            ax = self.pnlMGrp.AddSubPlot(111)
            # we need figure object
            fig = self.pnlMGrp.GetFigure()

            from matplotlib.colors import LightSource
            y,x = np.mgrid[-4:2:200j, -4:2:200j]
            z = 10 * np.cos(x**2 + y**2)

            cmap = matplotlib.cm.copper
            ls = LightSource(315, 45)
            rgb = ls.shade(z, cmap)

            ax.imshow(rgb, interpolation='bilinear')
            im = ax.imshow(z, cmap=cmap)
            im.remove()
            fig.colorbar(im)
            ax.set_title('Using a colorbar with a shaded plot', size='x-large')

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
