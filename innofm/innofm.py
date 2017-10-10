import os
import subprocess
import wx
import wx.html2 as html2

from wx.lib.embeddedimage import PyEmbeddedImage

peiFTree = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAA3XAAAN1wFCKJt4'
    b'AAAAg0lEQVRIx92WQQ6AIAwEp8Z/6c+sP6svwwsHY0ygxBJ0LxxIOqVdCgIkAjURrO8D5rwe'
    b'gL0cewUWcpM1IHkFUrcS3cklWW1JnwBbZXI2lIuu2guu2L2Oq3WROseKAmluOHUJIv8cFR5J'
    b'NEA9+y2AzQMYqgfWA2DD2VTyzQx70ST623IC41wZdsPmJLYAAAAASUVORK5CYII=')

peiFList = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAQAAABKfvVzAAAABGdBTUEAALGPC/xhBQAAACBj'
    b'SFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIA'
    b'AAAJcEhZcwAADdcAAA3XAUIom3gAAAAHdElNRQfhCgkDJTjkw+OMAAABF0lEQVQ4y6XUQStE'
    b'URjG8d8VGkPYWsjCB/A5ZoGlptjZqGkWdspOdrKylJTmYssnUVKWVhbCiBlzKddmxq25Z3Fv'
    b'zrt533pOz/P+Ox0WxRJpgUrEFokLiQcVRxLjip+vSFpCjpFycki1C2vb0tIOo3/dnG3H7i2r'
    b'54K+2PM4HKkpdYi7IM7mIFLm0FJxiS2rOYdXrUEbSb2Z7RP7AdO5Cz29vsNMFqnm3SYuAoE+'
    b'1fKUKiZMYjqAZkwlFKmqi8h8LtK750GkbOkpa648WbISwHriYxhrQ+oAt0GsjTzWa0vOsG8j'
    b'4HCdDSXfUuawYNeRG/Wgw46Hf+9w6tMV1oOUTrMh0VEttEFVRxKJ1XV9F7gwpupc2W/mF0om'
    b'v3PMxIaqAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDE3LTEwLTA5VDAzOjM3OjU2KzAyOjAw4HG2'
    b'dAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxNy0xMC0wOVQwMzozNzo1NiswMjowMJEsDsgAAAAZ'
    b'dEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC')

peiFView = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAQAAABKfvVzAAAABGdBTUEAALGPC/xhBQAAACBj'
    b'SFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIA'
    b'AAAJcEhZcwAADdcAAA3XAUIom3gAAAAHdElNRQfhCgkDIgXz6jlaAAAA2klEQVQ4y93Uv0oD'
    b'QRCA8d9dLAw2KmiVwiImlZXvIz6KWGjnA1znWwR9ABHBwkJExMo/AS3vWsfGC8lpkr3WmWKH'
    b'3e8rZndYegqlSMhSoUeRBNdZZEprvnxYHltyFSGME3DGQuQLgMyerLk5X9j26M6DzVThQB8D'
    b'h6nC88/61DyY1/SKY7eOdGabbgp9904W3dKssOtFCKdpwsDr5EVrZcOVke5fwnAKr5V1N0K4'
    b'1G0KQ2+/5ubM9aS+sDotlN6Xjt3IpxCZ0Crydvh/EapWfNWxY7+FcK7tN/MNXZm3eVboB6MA'
    b'AAAldEVYdGRhdGU6Y3JlYXRlADIwMTctMTAtMDlUMDM6MzQ6MDUrMDI6MDByThmOAAAAJXRF'
    b'WHRkYXRlOm1vZGlmeQAyMDE3LTEwLTA5VDAzOjM0OjA1KzAyOjAwAxOhMgAAABl0RVh0U29m'
    b'dHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAAASUVORK5CYII=')

wv_files = ['c','cpp','h','py','txt','png','jpg']

class InnoFileMgr(wx.Panel):

    def __init__(self, *args, **kwgs):
        wx.Panel.__init__(self, *args, **kwgs)

        # current file and folder
        self.currentFile = ''
        self.currentDir = os.getcwd()

        # book control
        self.book = wx.Simplebook(self)

        # directory control
        self.ftree = wx.GenericDirCtrl(self.book, style=wx.DIRCTRL_EDIT_LABELS)

        # webview: flie list mode
        self.flist = html2.WebView.New(self.book)

        # webview: flie view mode
        # TODO: this will be replaced by proper viewer
        self.fview = html2.WebView.New(self.book)

        # button bitmaps
        bmpFTree = peiFTree.GetBitmap()
        bmpFList = peiFList.GetBitmap()
        bmpFView = peiFView.GetBitmap()
        #
        self.btnFTree = wx.BitmapToggleButton(self, -1, bmpFTree,
                (20,20), (bmpFTree.GetWidth()+14, bmpFTree.GetHeight()+14))
        self.btnFList = wx.BitmapToggleButton(self, -1, bmpFList,
                (20,20), (bmpFList.GetWidth()+14, bmpFList.GetHeight()+14))
        self.btnFView = wx.BitmapToggleButton(self, -1, bmpFView,
                (20,20), (bmpFView.GetWidth()+14, bmpFView.GetHeight()+14))
        #
        self.pages = [
                {'name':'Tree', 'page':self.ftree, 'button':self.btnFTree},
                {'name':'List', 'page':self.flist, 'button':self.btnFList},
                {'name':'View', 'page':self.fview, 'button':self.btnFView}]

        # add pages to the book
        for idx, item in enumerate(self.pages):
            self.book.AddPage(item['page'], '')
            item['page no'] = idx


        # address bar
        self.cboAddr = wx.ComboBox(self, -1,
                choices=[
                    '>> Add to Favorite <<',
                    '>> Go to Parent <<',
                    '>> Select Directory <<'], style = wx.TE_PROCESS_ENTER)
                
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(self.btnFTree, 0, wx.ALL, 2)
        sizer_h.Add(self.btnFList, 0, wx.ALL, 2)
        sizer_h.Add(self.btnFView, 0, wx.ALL, 2)
        sizer_h.Add(self.cboAddr, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.book, 1, wx.ALL|wx.EXPAND, 4)
        sizer.Add(sizer_h, 0, wx.ALL|wx.EXPAND, 0)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)

        # event from DIRCTRL
        self.Bind(wx.EVT_DIRCTRL_SELECTIONCHANGED, self.OnDirSelChanged,
                self.ftree)
        self.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.OnFileActivated,
                self.ftree)

        # event from WEBVIEW
        self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATED, self.OnWebNavigated,
                self.flist)
        self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.OnWebLoaded,
                self.flist)

        # event from TOGGLEBUTTON
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnPageChange, self.btnFTree)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnPageChange, self.btnFList)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnPageChange, self.btnFView)

        # event from COMBOBOX
        self.Bind(wx.EVT_COMBOBOX, self.OnAddressSelect, self.cboAddr)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnAddressEnter, self.cboAddr)

        # set initial page
        self.btnFTree.SetValue(1)
        self.SetCurrentPage('Tree')


    def OnWebNavigated(self, evt):
        # do nothing for now
        pass

    def OnWebLoaded(self, evt):
        # do nothing for now
        pass
    
    def OnPageChange(self, evt):
        # which button?
        for item in self.pages:
            if item['button'] == evt.GetEventObject():
                item['button'].SetValue(1)
                self.SetCurrentPage(item['name'])
            else:
                item['button'].SetValue(0)


    def OnFileActivated(self, evt):
        # double click in the directory mode
        self.Run(self.ftree.GetPath())

    def OnDirSelChanged(self, evt):
        self.SetCurrentPath(self.ftree.GetPath())

    def OnAddressSelect(self, evt):
        sel = self.cboAddr.GetValue()
        if 'Add to' in sel:
            pass
        elif 'Go to' in sel:
            pass
        elif 'Select' in sel:
            pass
        


    def OnAddressEnter(self, evt):
        if self.cboAddr.GetValue() == '':
            return

        if self.GetCurrentPage() == 'List':
            self.flist.LoadURL(self.cboAddr.GetValue())


    def SetCurrentPath(self, path):
        # write current path on the address bar
        self.cboAddr.SetValue(path)

        # set current file and current directory
        if os.path.isfile(path):
            self.currentDir = os.path.dirname(path)
            self.currentFile = path
        else:
            self.currentDir = path
            self.currentFile = ''

        # update page display
        self.UpdatePage()


    def SetCurrentPage(self, page):

        for item in self.pages:
            if item['name'] == page:
                page_no = item['page no']
                break

        if page == 'Tree':
            self.ftree.ExpandPath(self.currentDir)
        elif page == 'List':
            self.flist.LoadURL('file:///' + self.currentDir)
        elif page == 'View':
            if self.IsViewable(self.currentFile):
                self.fview.LoadURL('file:///' + self.currentFile)
            else:
                self.fview.SetPage("<html><body>Hello</body></html>","")

        self.book.SetSelection(page_no)


    def IsViewable(self, fpath):
        ext = fpath[fpath.rfind('.')+1:]
        if ext in wv_files:
            return True
        else:
            return False


    def GetCurrentPage(self):
        page = self.book.GetCurrentPage()

        for item in self.pages:
            if page == item['page']:
                return item['name']


    def UpdatePage(self):
        pass


    def Run(self, fpath):
        '''
        This allows to run MIME in directory mode
        '''
        if fpath == '':
            return

        ext = fpath[fpath.rfind('.')+1:]
        ftype = wx.TheMimeTypesManager.GetFileTypeFromExtension(ext)

        if ftype:
            params = wx.FileType.MessageParameters(fpath,
                    ftype.GetMimeType())
            cmd = ftype.GetOpenCommand(params)
            if cmd != '':
                subprocess.call(cmd)



if __name__=="__main__":

    class MyFrame(wx.Frame):

        def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title=title)

            # toolbar
            self.toolbar = wx.ToolBar(self)
            self.toolbar.Realize()

            # spliter window
            self.spw = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)

            # panel
            self.pnlFM1 = InnoFileMgr(self.spw)
            self.pnlFM2 = InnoFileMgr(self.spw)

            self.spw.SetMinimumPaneSize(200)
            self.spw.SplitVertically(self.pnlFM1, self.pnlFM2, 0)

            # event binding
            self.Bind(wx.EVT_CLOSE, self.OnClose)

            # sizer
            sizer_h = wx.BoxSizer(wx.HORIZONTAL)
            sizer_h.Add(self.spw, 1, wx.EXPAND)

            sizer_v = wx.BoxSizer(wx.VERTICAL)
            sizer_v.Add(self.toolbar, 0, wx.ALL|wx.EXPAND, 4)
            sizer_v.Add(sizer_h,1, wx.EXPAND)

            self.SetSizer(sizer_v)
            self.SetAutoLayout(1)
            #sizer.Fit(self)
            self.SetSize((1200,800))
            self.Show()


        def OnClose(self, evt):
            # destroy self
            self.Destroy()

    app = wx.App()
    frame = MyFrame(None, "file manager demo")

    app.MainLoop()
