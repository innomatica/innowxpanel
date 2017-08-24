"""
================
Embedding In Wx2
================

An example of how to use wx or wxagg in an application with the new
toolbar - comment out the setA_toolbar line for no toolbar
"""

# Matplotlib requires wxPython 2.8+
# set the wxPython version in lib\site-packages\wx.pth file
# or if you have wxversion installed un-comment the lines below
#import wxversion
#wxversion.ensureMinimal('2.8')

from numpy import arange, sin, pi

import matplotlib

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import wx

class InnoMplot(wx.Panel):

    def __init__(self, parent, hideToolbar=False):

        wx.Panel.__init__(self, parent)

        # figure object
        self.figure = Figure()
        # canvas object
        self.canvas = FigureCanvas(self, -1, self.figure)
        # toolbar
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.ShowToolbar(not hideToolbar)
        self.SetSizer(self.sizer)
        self.Fit()


    def ShowToolbar(self, flag):
        self.toolbar.Show(flag)
        self.Layout()


    def AddSubPlot(self, *args, **kwgs):
        # create axes object and return
        return self.figure.add_subplot(*args, **kwgs)

    def GetCanvas(self):
        return self.canvas

    def GetFigure(self):
        return self.figure

    def GetColorMap(self):
        return matplotlib.cm

    def Draw(self):
        self.canvas.draw()

    def Clear(self):
        self.figure.clear()


if __name__=="__main__":

    import numpy as np

    class MyFrame(wx.Frame):

        def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title=title)

            # menu id
            self.idLine = wx.NewId()
            self.idHist = wx.NewId()
            self.idCont = wx.NewId()
            self.idShade = wx.NewId()
            # menu
            menu = wx.Menu()
            # menu item
            mitemLine = menu.Append(self.idLine, "Line", "")
            mitemHist = menu.Append(self.idHist, "Histogram", "")
            mitemCont = menu.Append(self.idCont, "Contour", "")
            mitemShade = menu.Append(self.idShade, "Shade", "")

            # menubar
            menubar = wx.MenuBar()
            menubar.Append(menu, "Demo")
            self.SetMenuBar(menubar)

            # panel
            self.pnlPlot = InnoMplot(self)

            # event binding
            self.Bind(wx.EVT_MENU, self.OnDrawGraph, mitemLine)
            self.Bind(wx.EVT_MENU, self.OnDrawGraph, mitemHist)
            self.Bind(wx.EVT_MENU, self.OnDrawGraph, mitemCont)
            self.Bind(wx.EVT_MENU, self.OnDrawGraph, mitemShade)
            self.Bind(wx.EVT_CLOSE, self.OnClose)

            # sizer
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(self.pnlPlot,1, wx.EXPAND)

            self.SetSizer(self.sizer)
            self.SetAutoLayout(1)
            self.sizer.Fit(self)
            self.Show()


        def OnDrawGraph(self, evt):

            # simple line plot
            if evt.GetId() == self.idLine:
                # clear previous plot
                self.pnlPlot.Clear()
                # acquire new axes
                ax = self.pnlPlot.AddSubPlot(111)

                x = np.linspace(0,10,500)
                dashes = [10,5,100,5]

                line1, = ax.plot(x, np.sin(x), '--', linewidth=2,
                        label='Dashes set retroactively')
                line1.set_dashes(dashes)

                line2, = ax.plot(x, -1 * np.sin(x), dashes=[30, 5, 10, 5],
                        label='Dashes set proactively')
                ax.legend(loc='lower right')

            # histogram
            elif evt.GetId() == self.idHist:
                # clear previous plot
                self.pnlPlot.Clear()
                # acquire new axes
                ax0 = self.pnlPlot.AddSubPlot(1,2,1)
                ax1 = self.pnlPlot.AddSubPlot(1,2,2)

                np.random.seed(0)
                mu = 200
                sigma = 25
                bins = [100, 150, 180, 195, 205, 220, 250, 300]
                x = np.random.normal(mu, sigma, size=100)

                ax0.hist(x, 20, normed=1, histtype='stepfilled', facecolor='g',
                        alpha=0.75)
                ax0.set_title('stepfilled')

                ax1.hist(x, bins, normed=1, histtype='bar', rwidth=0.8)
                ax1.set_title('unequal bins')

            # contour
            elif evt.GetId() == self.idCont:
                # clear previous plot
                self.pnlPlot.Clear()
                # acquire new axes
                ax = self.pnlPlot.AddSubPlot(111)
                # we need figure object
                fig = self.pnlPlot.GetFigure()

                Y,X = np.mgrid[-3:3:100j, -3:3:100j]
                U = -1 - X**2 + Y
                V = 1 + X - Y**2
                strm = ax.streamplot(X, Y, U, V, color=U, linewidth=2,
                        cmap=matplotlib.cm.autumn)
                fig.colorbar(strm.lines)

            elif evt.GetId() == self.idShade:
                # clear previous plot
                self.pnlPlot.Clear()
                # acquire new axes
                ax = self.pnlPlot.AddSubPlot(111)
                # we need figure object
                fig = self.pnlPlot.GetFigure()

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
                ax.set_title('Using a colorbar with a shaded plot',
                        size='x-large')

            # draw plot
            self.pnlPlot.Draw()


        def OnClose(self, evt):
            # explicitly destroy the panel
            self.pnlPlot.Close()
            # destroy self
            self.Destroy()



    app = wx.App()
    frame = MyFrame(None, "innocom demo")

    app.MainLoop()
