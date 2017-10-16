#!/usr/bin/env python3

import os
import wx

#----------------------------------------------------------------------

#----------------------------------------------------------------------
# This class is used to provide an interface between a ComboCtrl and the
# ListCtrl that is used as the popoup for the combo widget.


class FavoriteCombo(wx.ComboPopup):

    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.lc = None
        self.max_items = 4
        self.initial_p = 10
        self.itemdata = 0


    def AddItem(self, addr):
        # check if the same address exists already
        match = -1
        for i in range(self.lc.GetItemCount()):
            if self.lc.GetItemText(i, 1) == addr:
                match = i
                break

        if match > 0:
            # match found: upvote instead of adding
            self.UpVote(match)
            return

        # alias at the first column
        index = self.lc.InsertItem(self.lc.GetItemCount(), self.GetAlias(addr))
        # address at the second column
        self.lc.SetItem(index, 1, addr)
        # initial polularity
        self.lc.SetItem(index, 2, str(self.initial_p))
        # finally set item data (unique number)
        self.lc.SetItemData(index, self.itemdata)
        self.itemdata = self.itemdata + 1

        # too many occupant?
        if self.lc.GetItemCount() > self.max_items:
            # find out who is the looser
            looser = (-1, self.initial_p)
            for i in range(self.lc.GetItemCount()):
                # retrieve the popularity
                p = int(self.lc.GetItemText(i,2))
                # the least popular guy is the looser of course
                if p < looser[1]:
                    looser = (i, p)

            # get rid of the looser
            self.DeleteItem(looser[0])


    def DeleteItem(self, index):
        '''
        Delete an item from the list control without changing the average
        popularity
        '''

        # populaty to be deleted along with the item
        delete_p = int(self.lc.GetItemText(index, 2))
        # o.k. to delete the item now
        self.lc.DeleteItem(index)

        # total item count left
        n = self.lc.GetItemCount()
        # difference to be adjusted for each item
        diff_p = int((self.initial_p - delete_p) / n + 0.5)
        # and remainder
        rem_p = (self.initial_p - delete_p) - diff_p * (n - 1)

        for i in range(n):
            p = int(self.lc.GetItemText(i, 2))

            if i == 0:
                # (un)lucky guy should take care of the remainder
                self.lc.SetItem(i, 2, str(p - rem_p))
            else:
                self.lc.SetItem(i, 2, str(p - diff_p))


    def OnMotion(self, evt):
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0 and item != self.focused:
            self.lc.Select(item)
            self.focused = item


    def OnLeftDown(self, evt):
        self.selected = self.focused
        self.Dismiss()

    def GetAlias(self, addr):

        if os.name == 'nt':
            delimiter = '\\'
        else:
            delimiter = '/'

        return addr[addr.rfind(delimiter)+1:]

    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.

    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.selected = -1
        self.focused = -1


    def OnListSort(self, evt):
        self.sortcol = evt.GetColumn()
        self.lc.SortItems(self.ListCompare)


    def ListCompare(self, item1, item2):

        for i in range(self.lc.GetItemCount()):
            if self.lc.GetItemData(i) == item1:
                index1 = i
            elif self.lc.GetItemData(i) == item2:
                index2 = i

        if self.sortcol == 0 or self.sortcol == 1:
            # string comparison
            cmp1 = self.lc.GetItemText(index1, self.sortcol)
            cmp2 = self.lc.GetItemText(index2, self.sortcol)
            # sort up
            if cmp1 > cmp2:
                return 1
            elif cmp1 < cmp2:
                return -1
            else:
                return 0

        elif self.sortcol == 2:
            # integer comparison
            cmp1 = int(self.lc.GetItemText(index1, self.sortcol))
            cmp2 = int(self.lc.GetItemText(index2, self.sortcol))
            # sort down
            if cmp1 > cmp2:
                return -1
            elif cmp1 < cmp2:
                return 1
            else:
                return 0



    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        # create a listcontrol with report type
        self.lc = wx.ListCtrl(parent, -1, style=wx.LC_REPORT|
                wx.LC_SINGLE_SEL|wx.LC_HRULES|wx.LC_VRULES)

        # prepare 3 columns
        self.lc.InsertColumn(0, 'Alias')
        self.lc.InsertColumn(1, 'Address')
        self.lc.InsertColumn(2, 'Popularity')

        # bind events
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.lc.Bind(wx.EVT_LIST_COL_CLICK, self.OnListSort, self.lc)

        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.lc

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.selected >= 0:
            # get address
            addr = self.lc.GetItemText(self.selected, 1)
            # TODO recompute polularity
            self.UpVote(self.selected)
            # return the address (the second colum)
            return addr
        return ""


    def UpVote(self, index):
        # get the number of items
        n = self.lc.GetItemCount()
        # those who has zero popularity
        forgotten = []

        for i in range(n):
            # retrieve the popularity
            p = int(self.lc.GetItemText(i,2))

            # voting
            if index == i:
                # upvote: take one from each 
                p = p + (n - 1)
            else:
                # downvote: give one
                p = p - 1

            self.lc.SetItem(i, 2, str(p))

            # find who has to go
            if p == 0:
                forgotten.append(i)


        # deal with the forgotten
        for i in reversed(forgotten):
            self.DeleteItem(i)



    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        wx.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        return wx.ComboPopup.LazyCreate(self)

#----------------------------------------------------------------------




if __name__=="__main__":

    class MyFrame(wx.Frame):

        def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title=title)

            self.comboCtrl = wx.ComboCtrl(self, wx.ID_ANY, "", (20,20))
            self.popupCtrl = FavoriteCombo()
            self.myButton = wx.Button(self, -1, "Add one more")

            # It is important to call SetPopupControl() as soon as possible
            self.comboCtrl.SetPopupControl(self.popupCtrl)

            # Populate using wx.ListView methods
            self.popupCtrl.AddItem('c:\\Users\\sungjune\\Personal')
            self.popupCtrl.AddItem('c:\\Users\\sungjune\\Personal\\Documents')
            self.popupCtrl.AddItem('c:\\Users\\sungjune\\Personal\\Projects')
            self.popupCtrl.AddItem('c:\\Users\\sungjune\\Personal\\Downloads')

            sizer_v = wx.BoxSizer(wx.VERTICAL)
            sizer_v.Add(self.comboCtrl, 0, wx.EXPAND)
            sizer_v.Add(self.myButton, 0, wx.EXPAND)
            sizer_v.Add((20,20), 1, wx.EXPAND)

            self.Bind(wx.EVT_BUTTON, self.OnAddMore, self.myButton)

            self.SetSizer(sizer_v)
            self.SetAutoLayout(1)
            self.SetSize((1000,300))
            self.Show()

        def OnAddMore(self, evt):
            self.popupCtrl.AddItem('c:\\Users\\sungjune\\Personal\\EvenMore')

    app = wx.App()
    frame = MyFrame(None, "file manager demo")

    app.MainLoop()
#----------------------------------------------------------------------
