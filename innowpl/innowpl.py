
import wx
from wx.lib import plot as wxplot

class InnoWpl(wx.Panel):

    def __init__(self, *args, **kwgs):

        wx.Panel.__init__(self, *args, **kwgs)

        # canvas object
        self.canvas = wxplot.PlotCanvas(self)
        # toolbar id
        self.tidHome = wx.NewId()
        self.tidDrag = wx.NewId()
        self.tidZoom = wx.NewId()
        self.tidSave = wx.NewId()
        # toolbar
        self.toolbar = wx.ToolBar(self)
        # size
        self.toolbar.SetToolBitmapSize((24,24))
        # toolbar buttons
        self.toolbar.AddTool(self.tidHome, '', wx.Bitmap('home.png'),
                shortHelp = 'Home')
        self.toolbar.AddCheckTool(self.tidDrag, '', wx.Bitmap('move.png'),
                shortHelp = 'Pan')
        self.toolbar.AddCheckTool(self.tidZoom, '', wx.Bitmap('zoom.png'),
                shortHelp = 'Zoom')
        self.toolbar.AddTool(self.tidSave, '', wx.Bitmap('save.png'),
                shortHelp = 'Save')
        self.toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=self.tidHome)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=self.tidDrag)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=self.tidZoom)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=self.tidSave)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()


    def OnToolClick(self, evt):
        tid = evt.GetId()

        if tid == self.tidHome:
            self.canvas.Reset()

        elif tid == self.tidDrag:
            if self.toolbar.GetToolState(self.tidDrag):
                self.canvas.enableDrag = True
                self.toolbar.EnableTool(self.tidHome, False)
                self.toolbar.EnableTool(self.tidZoom, False)
                self.toolbar.EnableTool(self.tidSave, False)
            else:
                self.canvas.enableDrag = False
                self.toolbar.EnableTool(self.tidHome, True)
                self.toolbar.EnableTool(self.tidZoom, True)
                self.toolbar.EnableTool(self.tidSave, True)

        elif tid == self.tidZoom:
            if self.toolbar.GetToolState(self.tidZoom):
                self.canvas.enableZoom = True
                self.toolbar.EnableTool(self.tidHome, False)
                self.toolbar.EnableTool(self.tidDrag, False)
                self.toolbar.EnableTool(self.tidSave, False)
            else:
                self.canvas.enableZoom = False
                self.toolbar.EnableTool(self.tidHome, True)
                self.toolbar.EnableTool(self.tidDrag, True)
                self.toolbar.EnableTool(self.tidSave, True)

        elif tid == self.tidSave: 
            with wx.FileDialog(self, "Save plot file",
                    wildcard="image files (*.jpg)|*.jpg",
                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_OK:
                    print('file path', fileDialog.GetPath())

                    self.canvas.SaveFile(fileDialog.GetPath())


    def GetCanvas(self):
        return self.canvas


    ##
    #   plot wxplot.Graphics object
    #
    def Draw(self, graphics):
        self.canvas.Draw(graphics)

    def SetPen(self, pen):
        self.canvas.axesPen = pen

    def Clear(self):
        self.canvas.Clear()


if __name__=="__main__":

    import numpy as np

    class MyFrame(wx.Frame):

        def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title=title)

            # menu id
            self.idLine = wx.NewId()
            self.idHist= wx.NewId()
            # menu
            menu = wx.Menu()
            # menu item
            mitemLine = menu.Append(self.idLine, "Line", "")
            mitemHist = menu.Append(self.idHist, "Histogram", "")

            # menubar
            menubar = wx.MenuBar()
            menubar.Append(menu, "Demo")
            self.SetMenuBar(menubar)

            # panel
            self.pnlPlot = InnoWpl(self, size=(640,480))

            # event binding
            self.Bind(wx.EVT_MENU, self.OnDrawGraph, mitemLine)
            self.Bind(wx.EVT_MENU, self.OnDrawGraph, mitemHist)
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

                x = np.linspace(0,10,500)
                y = np.sin(x)

                # create lines
                line1 = wxplot.PolyLine(list(zip(x, np.sin(x))),
                        colour='red', width=3, style=wx.PENSTYLE_DOT_DASH)
                line2 = wxplot.PolyLine(list(zip(x, -np.sin(x))),
                        colour='blue', width=3, style=wx.PENSTYLE_LONG_DASH)

                # create a graphics
                graphics = wxplot.PlotGraphics([line1, line2])
                self.pnlPlot.Draw(graphics)

            # histogram
            elif evt.GetId() == self.idHist:
                # clear previous plot
                self.pnlPlot.Clear()

                np.random.seed(0)
                # fixed bins on the right
                x1 = np.random.normal(400, 25, size=100)
                h1,b1 = np.histogram(x1, bins=8)
                hist1 = wxplot.PolyHistogram(h1,b1,fillcolour='red')
                # variable bins on the left
                x2 = np.random.normal(200, 25, size=100)
                h2,b2 = np.histogram(x2,
                        bins=[100, 150, 180, 195, 205, 220, 250, 300])
                hist2 = wxplot.PolyHistogram(h2, b2,fillcolour='blue')

                # graph title and axis titles
                graphics = wxplot.PlotGraphics([hist1, hist2],
                        'Histogram with variable binsize and fixed binsize',
                        'value', 'count')
                self.pnlPlot.Draw(graphics)

        def OnClose(self, evt):
            # explicitly destroy the panel
            self.pnlPlot.Close()
            # destroy self
            self.Destroy()


    app = wx.App()
    frame = MyFrame(None, "innowpl demo")

    app.MainLoop()
