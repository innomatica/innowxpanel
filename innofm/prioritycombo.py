#!/usr/bin/env python3
import os
import wx

class PriorityPopup(wx.ComboPopup):
    ''' 
    ComboPupup automatically maintains its items based on the priority.

    The popup object is wx.ListCtrl. For each item in the list, priority value
    is assigned, which is updated on every click.
    '''

    def __init__(self):
        wx.ComboPopup.__init__(self)
        # popup object: wx.ListCtrl
        self.lc = None


    def AddItem(self, item):
        '''
        Add new item to the list

        Parameters
        ----------
        item: text that is to be added
        '''
        # check if the same item exists already
        match = -1
        for i in range(self.lc.GetItemCount()):
            if self.lc.GetItemText(i, 1) == item:
                match = i
                break

        if match > 0:
            # match found: upvote it instead of addition
            self.UpVote(match)
            return

        # alias at the first column
        if os.name == 'nt':
            delimiter = '\\'
        else:
            delimiter = '/'
        alias = item[item.rfind(delimiter)+1:]
        index = self.lc.InsertItem(self.lc.GetItemCount(), alias)
                
        # item text at the second column
        self.lc.SetItem(index, 1, item)
        self.lc.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        # set the priority: default
        self.lc.SetItem(index, 2, str(self.default_p))

        # finally set item data (unique number)
        self.lc.SetItemData(index, self.itemdata)
        self.itemdata = self.itemdata + 1

        # too many occupants?
        if self.lc.GetItemCount() > self.max_items:
            # find out who is the looser
            looser = (-1, self.default_p)
            for i in range(self.lc.GetItemCount()):
                # retrieve the priority
                p = int(self.lc.GetItemText(i,2))
                # the least popular guy is the looser of course
                if p < looser[1]:
                    looser = (i, p)

            # get rid of the looser
            self.DeleteItem(looser[0])


    def OnMotion(self, evt):
        '''
        Track the focused item in respond to the mouse move
        '''
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0 and item != self.focused:
            # change the color of the focused row
            self.lc.Select(item)
            # save the item as focused
            self.focused = item


    def OnLeftDown(self, evt):
        '''
        Convert focused to selected
        '''
        self.selected = self.focused
        self.Dismiss()


    def SetMaxItems(self, max_items):
        '''
        Set maximum number of items it maintains
        '''
        self.max_items = max_items


    def SetDefaultPriority(self, default_p):
        '''
        Set the default priority value that will be assigned to every new member
        '''
        self.default_p = default_p


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.

    def Init(self):
        '''
        This is called immediately after construction finishes.  You can
        use self.GetCombo if needed to get to the ComboCtrl instance.
        '''
        self.selected = -1
        self.focused = -1


    def Create(self, parent):
        '''
        Create the popup child control.  Return true for success.
        '''

        # create a listcontrol with report type without header
        self.lc = wx.ListCtrl(parent, -1, style=wx.LC_REPORT|
                wx.LC_SINGLE_SEL|wx.LC_HRULES)

        # prepare 3 columns
        self.lc.InsertColumn(0, 'Alias')
        self.lc.InsertColumn(1, 'Item')
        self.lc.InsertColumn(2, 'Priority')
        # hide the last column
        self.lc.SetColumnWidth(2, 0)
        # TODO: set alternate row colour for virtual list
        #self.lc.EnableAlternateRowColours()

        # events from wx.ComboPopup
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        # events from wx.ListCtrl
        self.lc.Bind(wx.EVT_LIST_COL_CLICK, self.OnListColClick, self.lc)
        self.lc.Bind(wx.EVT_SIZE, self.OnListSize, self.lc)
        # note that wx.EVT_LIST_ITEM_SELECTED is abused by OnMotion()
        #self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected, self.lc)

        # set virtual item count
        #self.lc.SetItemCount(0)
        # maximum number of items
        self.SetMaxItems(10);
        # default priority value
        self.SetDefaultPriority(10)
        # item data as an identifier
        self.itemdata = 0

        return True


    def GetControl(self):
        '''
        Return the widget that is to be used for the popup
        '''
        return self.lc

    def SetStringValue(self, val):
        '''
        Called just prior to displaying the popup, you can use it to
        'select' the current item.
        '''
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    def GetStringValue(self):
        '''
        Return a string representation of the current item.
        '''

        if self.selected >= 0:
            # get item
            item = self.lc.GetItemText(self.selected, 1)
            # TODO recompute priority
            self.UpVote(self.selected)
            # return the item (the second colum)
            return item
        return ""

    def OnPopup(self):
        '''
        Called immediately after the popup is shown
        '''
        wx.ComboPopup.OnPopup(self)

    def OnDismiss(self):
        '''
        Called when popup is dismissed
        '''
        wx.ComboPopup.OnDismiss(self)

    def PaintComboControl(self, dc, rect):
        '''
        This is called to custom paint in the combo control itself
        (ie. not the popup).  Default implementation draws value as string.
        '''
        wx.ComboPopup.PaintComboControl(self, dc, rect)

    def OnComboKeyEvent(self, event):
        '''
        Receives key events from the parent ComboCtrl.  Events not
        handled should be skipped, as usual.
        '''
        wx.ComboPopup.OnComboKeyEvent(self, event)

    def OnComboDoubleClick(self):
        '''
        Implement if you need to support special action when user
        double-clicks on the parent wxComboCtrl.
        '''
        wx.ComboPopup.OnComboDoubleClick(self)


    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        '''
        Called on every popup, just prior to OnPopup.

        Parmeters
        ---------
        minWidth: int
            preferred minimum width for window
        prefHeight: int
            preferred height. Only applies if > 0,
        maxHeight: int
            max height for window, as limited by screen size and should only
            be rounded down, if necessary.

        Returns
        -------
        wx.Size: final size of popup

        '''
        return wx.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)


    def LazyCreate(self):
        '''
        Delay the creation of the popup.

        It is more efficient, but note that it is more convenient to have
        the control created immediately.

        Returns
        -------
        bool
            True if you want delay the call to Create until popup is shown
            for the first time, False otherwise
        '''
        return wx.ComboPopup.LazyCreate(self)


    def DeleteItem(self, index):
        '''
        Delete an item from the list control without changing the average
        priority
        '''

        # priority to be deleted along with the item
        delete_p = int(self.lc.GetItemText(index, 2))
        # o.k. to delete the item now
        self.lc.DeleteItem(index)

        # total item count left
        n = self.lc.GetItemCount()
        # difference to be adjusted for each item
        diff_p = int((self.default_p - delete_p) / n + 0.5)
        # and remainder
        rem_p = (self.default_p - delete_p) - diff_p * (n - 1)

        for i in range(n):
            p = int(self.lc.GetItemText(i, 2))

            if i == 0:
                # (un)lucky guy should take care of the remainder
                self.lc.SetItem(i, 2, str(p - rem_p))
            else:
                self.lc.SetItem(i, 2, str(p - diff_p))

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


    def OnListSize(self, evt):
        # adjust the second column accordingly
        self.lc.SetColumnWidth(1,
                self.lc.GetSize()[0] - self.lc.GetColumnWidth(0))


    def OnListColClick(self, evt):
        self.sortcol = evt.GetColumn()
        self.lc.SortItems(self.ListCompare)


    def UpVote(self, index):
        # get the number of items
        n = self.lc.GetItemCount()
        # those who has zero priority
        forgotten = []

        for i in range(n):
            # retrieve the priority
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



class PriorityCombo(wx.ComboCtrl):
    '''
    ComboCtrl hosts PriorityPopup
    '''

    def __init__(self, *args, **kwgs):
        wx.ComboCtrl.__init__(self, *args, **kwgs)
        # popup element
        self.popup = PriorityPopup()
        self.SetPopupControl(self.popup)
        # events
        self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)

    def AddItem(self, item):
        # calls popup method
        self.popup.AddItem(item)

    def DeleteItem(self, item):
        # calls popup method
        self.popup.DeleteItem(item)

    def OnTextEnter(self, evt):
        # handles wx.EVT_TEXT_ENTER event
        self.popup.AddItem(self.GetValue())


if __name__=="__main__":

    class MyFrame(wx.Frame):

        def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title=title)

            # priority combo control
            self.ComboCtrl = PriorityCombo(self, -1, "", (20,20))
            # add some items
            self.ComboCtrl.AddItem('c:\\Users\\sungjune\\Personal')
            self.ComboCtrl.AddItem('c:\\Users\\sungjune\\Personal\\Documents')
            self.ComboCtrl.AddItem('c:\\Users\\sungjune\\Personal\\Projects')
            self.ComboCtrl.AddItem('c:\\Users\\sungjune\\Personal\\Downloads')

            sizer_v = wx.BoxSizer(wx.VERTICAL)
            sizer_v.Add(self.ComboCtrl, 0, wx.EXPAND)
            sizer_v.Add((20,20), 1, wx.EXPAND)

            self.SetSizer(sizer_v)
            self.SetAutoLayout(1)
            self.SetSize((600,100))
            self.Show()


    app = wx.App()
    frame = MyFrame(None, "PriorityCombo demo")

    app.MainLoop()
#----------------------------------------------------------------------
