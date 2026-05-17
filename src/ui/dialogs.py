import wx

class LogsDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.label = wx.StaticText(self, wx.ID_ANY)
        self.progress_bar = wx.Gauge(self, wx.ID_ANY)

        s0   = wx.BoxSizer(wx.HORIZONTAL)
        s1   = wx.BoxSizer(wx.VERTICAL)
        s1_1 = wx.BoxSizer(wx.HORIZONTAL)
        s1_2 = wx.BoxSizer(wx.HORIZONTAL)

        self.main_log_ctrl = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.main_log_ctrl.SetBackgroundColour(wx.Colour('#FAFAFA'))

        s1_1.Add(self.progress_bar, 1, wx.EXPAND | wx.ALL)
        s1_1.SetMinSize((0, 24))

        s1_2.AddSpacer(32)
        s1_2.Add(self.main_log_ctrl, 1, wx.EXPAND)
        s1_2.AddSpacer(32)

        s1.AddSpacer(32)
        s1.Add(self.label, 0)
        s1.AddSpacer(4)
        s1.Add(s1_1, 0, wx.EXPAND)
        s1.AddSpacer(24)
        s1.Add(s1_2, 1, wx.EXPAND | wx.ALL)
        s1.AddSpacer(32)

        s0.AddSpacer(32)
        s0.Add(s1, 1, wx.EXPAND | wx.ALL)
        s0.AddSpacer(32)

        self.SetLabel('Ren\'Py Craken - logs')
        self.SetSizer(s0)
