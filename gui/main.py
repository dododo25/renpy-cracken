import wx

class ControlPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(ControlPanel, self).__init__(*args, **kw)

        confirm_button = wx.Button(self, label='Start')

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        panel = wx.Panel(self)

        control_panel = ControlPanel(panel)

        log_text_crtl = wx.TextCtrl(panel, size=(400, 600), style=wx.TE_MULTILINE)
        log_text_crtl.SetMinSize((400, 600))
        log_text_crtl.SetEditable(False)
        log_text_crtl.SetCanFocus(False)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(log_text_crtl, wx.SizerFlags().Border(wx.TOP|wx.BOTTOM, 0))
        sizer.Add(control_panel, wx.SizerFlags().Border(wx.TOP|wx.RIGHT|wx.BOTTOM, 0))

        panel.SetSizer(sizer)

        self.MakeMenuBar()

        #self.CreateStatusBar()
        #self.SetStatusText("Welcome to wxPython!")

        self.SetSize(1000, 600)
        self.Centre()

    def MakeMenuBar(self):
        fileMenu = wx.Menu()

        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")

        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()

        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)

    def OnHello(self, event):
        wx.MessageBox("Hello again from wxPython")

    def OnAbout(self, event):
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World",
                      wx.OK|wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()

    frm = MainFrame(None, title="Hello World")
    frm.Show()

    app.MainLoop()