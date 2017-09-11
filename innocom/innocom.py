#!/usr/bin/env python3

import binascii
import os
import pickle
import serial
import time
import _thread
import wx
import wx.lib.newevent

# serial port object
ser = serial.Serial()

# new event class for packet thread
(UpdateComData, EVT_UPDATE_COMDATA) = wx.lib.newevent.NewEvent()

# state machine variable
PKT_ST_HDRF = 0         # first header byte: 0xFF
PKT_ST_HDR5 = 1         # second header byte: 0x55
PKT_ST_SIZE = 2         # packet body size excluding checksum
PKT_ST_BODY = 3         # packet body
PKT_ST_CSUM = 4         # checksum

# 2 byte packet header
HDR_BYTE_FF = 0xFF
HDR_BYTE_55 = 0x55

# default data file name
data_file = 'innocom.dat'

##
# \brief    Return (default) monospace font face name depending on the OS.
#
def GetMonoFont():
    # do not consider the case of osx
    if os.name == 'posix':
        # fc-match will give default monospace font name
        a = os.popen('fc-match "Monospace"').read()
        # face name is burried in the middle
        l = a.find('"')
        r = a.find('"',l+1)
        return a[l+1:r]

    # Windows has only a couple of monospace fonts
    elif os.name == 'nt':
        return 'Consolas'

    # unknown OS
    else:
        return None

##
# \brielf   COM port listening thread.
# \details  Make sure that this thead starts after the port is open and
#           stops before the port is closed. Also the timeout value of
#           the port should be set preferably with small value.
#
class ComThread:

    def __init__(self, win):
        self.win = win
        self.running = False

    def Start(self):
        self.keepGoing = True
        self.running = True
        _thread.start_new_thread(self.Run, ())

    def Stop(self):
        # giving signal for nice termination
        self.keepGoing = False

    def Run(self):
        while self.keepGoing:
            # read a byte until timeout
            byte = ser.read()
            # valid byte received
            if len(byte):
                # create an event with the byte
                evt = UpdateComData(byte = byte)
                # post the event
                wx.PostEvent(self.win, evt)

        # end of loop
        self.running = False

    def IsRunning(self):
        return self.running

##
# \brief    COM terminal class as wx.Panel
#
class InnoCom(wx.Panel):

    def __init__(self, *args, hideControls = False, **kwags):
        wx.Panel.__init__(self, *args, **kwags)

        # terminal
        self.txtTerm = wx.TextCtrl(self, wx.ID_ANY, "", size=(500,350),
                style = wx.TE_MULTILINE|wx.TE_READONLY);
        self.txtTerm.SetForegroundColour('yellow')
        self.txtTerm.SetBackgroundColour('black')

        # monospace font is desirable
        fname = GetMonoFont()
        if fname:
            self.txtTerm.SetFont(wx.Font(11,75,90,90,faceName=fname))

        # panel for controls
        self.pnlControl = wx.Panel(self, wx.ID_ANY)

        # list of available COM ports
        from serial.tools import list_ports
        portlist = [port for port,desc,hwin in list_ports.comports()]

        # baudrate
        self.sttSpeed = wx.StaticText(self.pnlControl, -1, "Baudrate")
        self.cboSpeed = wx.Choice(self.pnlControl, -1,
                choices=['9600','19200','38400','57800','115200','230400'])
        self.cboSpeed.SetStringSelection('115200')
        # port
        self.sttCPort = wx.StaticText(self.pnlControl, -1, "COM Port")
        self.cboCPort = wx.Choice(self.pnlControl, -1, choices=portlist)
        # terminal mode
        self.sttTMode = wx.StaticText(self.pnlControl, -1, "Terminal Mode")
        self.cboTMode = wx.Choice(self.pnlControl, -1,
                choices=['ASCII','Binary','Protocol'])
        self.cboTMode.SetStringSelection('ASCII')
        # newline character
        self.sttNLine = wx.StaticText(self.pnlControl, -1, "Newline Char")
        self.cboNLine = wx.Choice(self.pnlControl, -1,
                choices=['LF(0x0A)','CR(0x0D)'])
        self.cboNLine.SetStringSelection('LF(0x0A)')
        # clear terminal
        self.sttClear = wx.StaticText(self.pnlControl, -1, "Clear Terminal")
        self.btnClear = wx.Button(self.pnlControl, -1, "Clear")
        # save raw data
        self.sttSave = wx.StaticText(self.pnlControl, -1, "Save Raw Data")
        self.btnSave = wx.Button(self.pnlControl, -1, "Save")

        if hideControls:
            self.pnlControl.Show(False)

        # thread
        self.thread = ComThread(self)

        # sizer
        sizer_g = wx.FlexGridSizer(6,2,4,4)
        sizer_g.Add(self.sttSpeed, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        sizer_g.Add(self.cboSpeed, 1, wx.EXPAND)
        sizer_g.Add(self.sttCPort, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        sizer_g.Add(self.cboCPort, 1, wx.EXPAND)
        sizer_g.Add(self.sttTMode, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        sizer_g.Add(self.cboTMode, 1, wx.EXPAND)
        sizer_g.Add(self.sttNLine, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        sizer_g.Add(self.cboNLine, 1, wx.EXPAND)
        sizer_g.Add(self.sttClear, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        sizer_g.Add(self.btnClear, 1, wx.EXPAND)
        sizer_g.Add(self.sttSave, 1, wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL)
        sizer_g.Add(self.btnSave, 1, wx.EXPAND)
        self.pnlControl.SetSizer(sizer_g)
        # sizer alignment
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h.Add(self.txtTerm, 1, wx.ALL|wx.EXPAND, 4)
        sizer_h.Add(self.pnlControl, 0, wx.ALL|wx.EXPAND, 4)
        self.SetSizer(sizer_h)
        sizer_h.Fit(self)

        # message binding
        self.Bind(wx.EVT_CHOICE, self.OnPortOpen, self.cboSpeed)
        self.Bind(wx.EVT_CHOICE, self.OnPortOpen, self.cboCPort)
        self.Bind(wx.EVT_CHOICE, self.OnTermType, self.cboTMode)
        self.Bind(wx.EVT_CHOICE, self.OnNewLine, self.cboNLine)
        self.Bind(wx.EVT_BUTTON, self.OnTermClear, self.btnClear)
        self.Bind(wx.EVT_BUTTON, self.OnFileSave, self.btnSave)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(EVT_UPDATE_COMDATA, self.OnUpdateComData)

        # packet state machine variables
        self.packet = []
        self.packet_count = 0
        self.packet_state = PKT_ST_HDRF
        # raw data
        self.rawdata = bytearray()
        # event list
        self.lstEvent = None
        # terminal type
        self.termType = self.cboTMode.GetStringSelection()
        # newline character
        if 'CR' in self.cboNLine.GetStringSelection():
            self.newLine = 0x0d
        else:
            self.newLine = 0x0a
        # counter for data alignment
        self.binCounter = 0

    ##
    # \brief Clear terminal. Note that the raw data is not changed.
    #
    def ClearTerminal(self):
        self.txtTerm.Clear()

    ##
    # \brief Put your packet decoding algorithm here
    #
    def DecodePacket(self, packet):
        pass

    ##
    # \brief Clear raw data. Terminal will be cleared as well.
    #
    def NewData(self):
        self.rawdata = bytearray()
        self.ClearTerminal()

    ##
    # \brief Open COM port
    #
    def OpenPort(self, port, speed):

        if ser.is_open:
            # terminate thread first
            if self.thread.IsRunning():
                self.thread.Stop()
            # join the thread
            while self.thread.IsRunning():
                time.sleep(0.1)
            # then close the port
            ser.close()

        # set port number and speed
        ser.port = port
        ser.baudrate = int(speed)
        # setting read timeout is crucial for the safe termination of thread
        ser.timeout = 1

        # open the serial port
        try:
            ser.open()
        except:
            return False
        else:
            pass

        if ser.is_open:
            # start thread
            self.thread.Start()
            return True
        else:
            return False

    ##
    # \brief Save received data
    #
    def SaveRawData(self, fname):
        f = open(fname, 'wb')
        f.write(self.rawdata)
        f.close()


    def SendData(self, data):
        ser.write(data)


    def SetNewLine(self, nl):
        if nl == 0x0d or nl == 0x0a:
            self.newLine = nl


    def SetTermType(self, termtype):
        if termtype != '':
            self.termType = termtype

        if self.termType == 'Binary':
            self.txtTerm.AppendText('\n')
            self.binCounter = 0

    def ShowControls(self, flag):
        self.pnlControl.Show(flag)
        self.Layout()

    def OnFileSave(self, evt):
        self.SaveRawData(data_file)


    def OnTermClear(self, evt):
        self.ClearTerminal()


    def OnTermType(self, evt):
        # terminal type
        self.SetTermType(self.cboTMode.GetStringSelection())


    def OnNewLine(self, evt):
        if 'CR' in self.cboNLine.GetStringSelection():
            self.SetNewLine(0x0d)
        else:
            self.SetNewLine(0x0a)


    def OnPortOpen(self, evt):
        port = self.cboCPort.GetStringSelection()
        speed = self.cboSpeed.GetStringSelection()

        # device is not selected
        if port == '':
            return

        # open the com port
        if self.OpenPort(port,speed):
            wx.MessageBox(port + ' is (re)open')
        else:
            wx.MessageBox('Failed to open: ' + port)


    def OnUpdateComData(self, evt):
        # append to the rawdata
        self.rawdata.append(evt.byte[0])

        if self.termType == 'Protocol':

            # Protocol decoding state machine
            if self.packet_state == PKT_ST_HDRF:

                if evt.byte[0] == HDR_BYTE_FF:
                    # first header detected: hunt for next
                    self.packet_state = PKT_ST_HDR5
                else:
                    # not a protocol stream
                    if evt.byte[0] > 0x1f and evt.byte[0] < 0x80:
                        # show byte as ASCII
                        self.txtTerm.AppendText(chr(evt.byte[0]))
                    elif evt.byte[0] == 0x0d:
                        # ignore CR
                        pass
                    elif evt.byte[0] == 0x0a:
                        # newline
                        self.txtTerm.AppendText('\n')
                    else:
                        # hex display
                        self.txtTerm.AppendText(evt.byte.hex())

            elif self.packet_state == PKT_ST_HDR5:

                if evt.byte[0] == HDR_BYTE_55:
                    # legit packet header found
                    self.packet_state = PKT_ST_SIZE
                else:
                    # false alarm: start all over
                    self.packet_state = PKT_ST_HDRF

            elif self.packet_state == PKT_ST_SIZE:
                # packet body size
                self.packet_size = evt.byte[0]
                if self.packet_size > 0:
                    # valid size: prepare for the boday
                    self.packet_count = 0
                    self.packet = []
                else:
                    # invalid size: start all over
                    self.packet_state = PKT_ST_HDRF

            elif self.packet_state == PKT_ST_BODY:
                # append the byte to the list
                self.packet.append(evt.byte[0])
                self.packet_count = self.packet_count + 1

                if self.packet_count == self.packet_size:
                    # end of body
                    self.packet_state = PKT_ST_CSUM

            elif self.packet_state == PKT_ST_CSUM:
                if self.ComputeCheckSum(self.packet) == evt.byte[0]:
                    # decode and display body
                    self.txtTerm.AppendText(self.DecodePacket(self.packet))
                else:
                    # checksum error
                    self.txtTerm.AppendText('Checksum Error\n')

        elif self.termType == 'Binary':
            self.txtTerm.AppendText('0x{:02X}'.format(evt.byte[0]))
            self.binCounter = self.binCounter + 1
            if self.binCounter == 8:
                self.txtTerm.AppendText(' - ')
            elif self.binCounter == 16:
                self.txtTerm.AppendText('\n')
                self.binCounter = 0
            else:
                self.txtTerm.AppendText('.')

        else:
            if evt.byte[0] == 0x0d or evt.byte[0] == 0x0a:
                if evt.byte[0] == self.newLine:
                    self.txtTerm.AppendText('\n')
                else:
                    pass
            else:
                self.txtTerm.AppendText(chr(evt.byte[0]))


    def OnClose(self, evt):
        # terminate the thread
        if self.thread.IsRunning():
            self.thread.Stop()
        # join the thread
        while self.thread.IsRunning():
            time.sleep(0.1)
        # close the port
        if ser.is_open:
            ser.close()
        # destroy self
        self.Destroy()


if __name__=="__main__":

    class MyFrame(wx.Frame):

        def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title=title)

            # menu id
            self.idShow = wx.NewId()
            self.idHide = wx.NewId()
            # menu
            menu = wx.Menu()
            mitemShow = menu.Append(self.idShow, "Show Controls", "")
            mitemHide = menu.Append(self.idHide, "Hide Controls", "")

            # menu bar
            menuBar = wx.MenuBar()
            menuBar.Append(menu, "Controls")
            self.SetMenuBar(menuBar)

            # panel
            self.pnlTerm = InnoCom(self, size=(1000,600))

            # event binding
            self.Bind(wx.EVT_CLOSE, self.OnClose)
            self.Bind(wx.EVT_MENU, self.OnShowControls, mitemShow)
            self.Bind(wx.EVT_MENU, self.OnShowControls, mitemHide)

            # sizer
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(self.pnlTerm,1, wx.EXPAND)

            self.SetSizer(self.sizer)
            self.SetAutoLayout(1)
            self.sizer.Fit(self)
            self.Show()

        def OnShowControls(self, evt):
            if evt.GetId() == self.idShow:
                self.pnlTerm.ShowControls(True)
            elif evt.GetId() == self.idHide:
                self.pnlTerm.ShowControls(False)

        def OnClose(self, evt):
            # destroy self
            self.Destroy()

    app = wx.App()
    frame = MyFrame(None, "innocom demo")

    app.MainLoop()
