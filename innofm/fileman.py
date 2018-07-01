#!/usr/bin/env python3

import os
import subprocess
import wx
import wx.html2 as html2

from prioritycombo import PriorityCombo
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

peiBMark = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAQAAABKfvVzAAAABGdBTUEAALGPC/xhBQAAACBj'
    b'SFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIA'
    b'AAAJcEhZcwAADdcAAA3XAUIom3gAAAAHdElNRQfhCgwEHR2KyW2HAAABhklEQVQ4y43TMUtb'
    b'YRSH8d+1iogWBCuIUoSSRALtJ/ADCG5SOhQc3ZwFv0BXZxcXQRRKXTI5CQ6COKg0kdqQbkIk'
    b'AYe4SCOnQ5M0prdNzju9//M891wOvIm0GvEeX/w0YG0LYXtQPO/JnTtP8oMJe8KGDWFvEDyn'
    b'qWbcuJqmXH9hV9gEm8JuPzyjqW4CTKhryjwHhvHKO1lZOVlvvLDlATzY8knRD2XflZV9VWfd'
    b'o+icqv3W93/P2Fft6j5aT1RN2/dNWVlZI+U3X8rKysj7qMaxcGC47zKGHQjHzKsIh0b+i484'
    b'FCrmYc6NUDD6T3xUQbgx1w5mlIQjY6n4mCOhZKY7nHYp7KQKO8Kl6d54QThNFU6FhfZlqBO/'
    b'xnWqcN3q9ghvUUoVSq1ua7vdQrGzxA/43HpxxW7hT50JsxiyqiKEilVDmBXOevFEw73EiqIQ'
    b'CgpCKFqRuNeQPBcmhVvnQjixCBadCOHcrTDZO+FKCBeWn+XLLoRw1TuBKWuW/o4llqyZal9/'
    b'AcS7i3NaIjAhAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDE3LTEwLTEyVDA0OjI5OjI5KzAyOjAw'
    b'Y7XGUQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxNy0xMC0xMlQwNDoyOToyOSswMjowMBLofu0A'
    b'AAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC')


wview_flist = ['c','cpp','h','py','txt','png','jpg']



class InnoFileMgr(wx.Panel):

    def __init__(self, *args, **kwgs):
        wx.Panel.__init__(self, *args, **kwgs)

        # current file and folder
        self.currentFile = ''
        self.currentDir = os.getcwd()

        # book control
        self.book = wx.Simplebook(self)

        # directory control without files
        self.dirctrl1 = wx.GenericDirCtrl(self.book, style=wx.DIRCTRL_DIR_ONLY)

        # directory control with files
        self.dirctrl2 = wx.GenericDirCtrl(self.book)

        # webview: flie list mode
        self.webview = html2.WebView.New(self.book)

        # webview: flie view mode
        # TODO: this will be replaced by proper viewer
        # wx.lib.ClickableHtmlWindow
        # wx.lib.docview
        # wx.lib.iewin
        # wx.lib.imagebrowser
        # wx.lib.imagebrowser.ImagePanel
        # wx.lib.pdfviewer
        # wx.lib.pdfwin
        # wx.lib.pydocview
        # textviewer
        # texteditor
        self.viewer = html2.WebView.New(self.book)

        self.pages = [
                {'name':'Dir1', 'page':self.dirctrl1},
                {'name':'Dir2', 'page':self.dirctrl2},
                {'name':'List', 'page':self.webview},
                {'name':'View', 'page':self.viewer}]

        # add pages to the book
        for idx, item in enumerate(self.pages):
            self.book.AddPage(item['page'], '')
            item['page no'] = idx

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.book, 1, wx.ALL|wx.EXPAND, 4)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)

        # event from DIRCTRL
        self.Bind(wx.EVT_DIRCTRL_SELECTIONCHANGED, self.OnDirSelChanged,
                self.dirctrl1)
        self.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.OnFileActivated,
                self.dirctrl2)
        # event from WEBVIEW
        self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATED, self.OnWebNavigated,
                self.webview)
        self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.OnWebLoaded,
                self.webview)

        # set initial page
        self.SetCurrentPage('Dir1')


    def OnWebNavigated(self, evt):
        # do nothing for now
        pass

    def OnWebLoaded(self, evt):
        # do nothing for now
        pass
    

    def TogglePage(self):
        if self.GetCurrentPage() == 'Dir1':
            self.SetCurrentPage('List')
        elif self.GetCurrentPage() == 'List':
            self.SetCurrentPage('Dir1')


    def OnFileActivated(self, evt):
        # double click in the directory mode
        self.Run(self.dirctrl2.GetPath())


    def OnDirSelChanged(self, evt):
        self.SetCurrentPath(self.dirctrl1.GetPath())


    def SetCurrentPath(self, path):

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

        if page == 'Dir1':
            self.dirctrl1.ExpandPath(self.currentDir)
        elif page == 'List':
            self.webview.LoadURL('file:///' + self.currentDir)
        elif page == 'View':
            if self.IsViewable(self.currentFile):
                self.viewer.LoadURL('file:///' + self.currentFile)
            else:
                self.viewer.SetPage("<html><body>Hello</body></html>","")

        self.book.SetSelection(page_no)


    def IsViewable(self, fpath):
        ext = fpath[fpath.rfind('.')+1:]
        if ext in wview_flist:
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

            # tool panel
            self.pnlTool = wx.Panel(self)

            # controls
            # button bitmaps
            bmpFTree = peiFTree.GetBitmap()
            bmpFList = peiFList.GetBitmap()
            bmpFView = peiFView.GetBitmap()
            #
            self.btnFTree = wx.BitmapToggleButton(self.pnlTool, -1, bmpFTree,
                    (20,20), (bmpFTree.GetWidth()+8, bmpFTree.GetHeight()+8))
            self.btnFList = wx.BitmapToggleButton(self.pnlTool, -1, bmpFList,
                    (20,20), (bmpFList.GetWidth()+8, bmpFList.GetHeight()+8))
            self.btnFView = wx.BitmapToggleButton(self.pnlTool, -1, bmpFView,
                    (20,20), (bmpFView.GetWidth()+8, bmpFView.GetHeight()+8))
            self.cboAddr = PriorityCombo(self.pnlTool, size=(-1,28))
            self.cboAddr.AddItem("\\usr\\sjlee\\blahblah")

            # sizer
            sizer_x = wx.BoxSizer(wx.HORIZONTAL)
            sizer_x.Add(self.btnFTree, 0, wx.EXPAND|wx.TOP|wx.LEFT, 4)
            sizer_x.Add(self.btnFList, 0, wx.EXPAND|wx.TOP|wx.LEFT, 4)
            sizer_x.Add(self.btnFView, 0, wx.EXPAND|wx.TOP|wx.LEFT, 4)
            sizer_x.Add(self.cboAddr, 1,
                    wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT|wx.RIGHT, 4)
            self.pnlTool.SetSizer(sizer_x)

            # spliter window
            self.spw = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
            self.spw.SetMinimumPaneSize(200)

            # main panel
            self.pnlFM1 = InnoFileMgr(self.spw)
            self.pnlFM2 = InnoFileMgr(self.spw)

            self.spw.SplitVertically(self.pnlFM1, self.pnlFM2, 0)

            # sizer
            sizer_y = wx.BoxSizer(wx.HORIZONTAL)
            sizer_y.Add(self.spw, 1, wx.EXPAND)

            # event binding
            self.Bind(wx.EVT_CLOSE, self.OnClose)
            self.Bind(wx.EVT_TOGGLEBUTTON, self.OnChangeView, self.btnFTree)
            self.Bind(wx.EVT_TOGGLEBUTTON, self.OnChangeView, self.btnFList)
            self.Bind(wx.EVT_TOGGLEBUTTON, self.OnChangeView, self.btnFView)
            self.pnlFM1.Bind(wx.EVT_CHAR_HOOK, self.OnCharFM1)
            self.pnlFM2.Bind(wx.EVT_CHAR_HOOK, self.OnCharFM2)

            sizer_z = wx.BoxSizer(wx.VERTICAL)
            sizer_z.Add(self.pnlTool, 0, wx.EXPAND)
            sizer_z.Add(sizer_y, 1, wx.EXPAND)

            self.SetSizer(sizer_z)
            self.SetAutoLayout(1)
            #sizer.Fit(self)
            self.SetSize((1200,800))
            self.Show()

        def OnChangeView(self, evt):
            if evt.GetEventObject() == self.btnFTree:
                self.btnFList.SetValue(0)
                self.btnFView.SetValue(0)
                # change view to Tree mode
                self.pnlFM1.SetCurrentPage('Dir1')
                self.pnlFM2.SetCurrentPage('List')
                self.spw.SetSashPosition(self.spw.GetClientSize()[0] * 0.25)

            elif evt.GetEventObject() == self.btnFList:
                self.btnFTree.SetValue(0)
                self.btnFView.SetValue(0)
                # change view to File List mode
                self.pnlFM1.SetCurrentPage('List')
                self.pnlFM2.SetCurrentPage('List')
                self.spw.SetSashPosition(self.spw.GetClientSize()[0] * 0.5)

            elif evt.GetEventObject() == self.btnFView:
                self.btnFTree.SetValue(0)
                self.btnFList.SetValue(0)
                # change view to File View mode
                self.pnlFM1.SetCurrentPage('Dir2')
                self.pnlFM2.SetCurrentPage('View')
                self.spw.SetSashPosition(self.spw.GetClientSize()[0] * 0.25)

        def OnCharFM1(self, evt):
            # space key
            if evt.GetKeyCode() == 0x20:
                self.pnlFM1.TogglePage()
            # tab key
            elif evt.GetKeyCode() == 0x09:
                pass
                #self.OnChar(evt)
            else:
                evt.Skip()

        def OnCharFM2(self, evt):
            # space key
            if evt.GetKeyCode() == 0x20:
                self.pnlFM2.TogglePage()
            # tab key
            elif evt.GetKeyCode() == 0x09:
                pass
                #self.OnChar(evt)
            else:
                evt.Skip()


        def OnClose(self, evt):
            # destroy self
            self.Destroy()

    app = wx.App()
    frame = MyFrame(None, "file manager demo")

    app.MainLoop()
