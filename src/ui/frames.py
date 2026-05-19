import webbrowser
import wx

from . import panels

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.panel = panels.MainPanel(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(self.panel, 1, wx.CENTER | wx.ALL, 10)

        self.SetSizer(sizer)
        self.SetBackgroundColour(wx.Colour('#FAFAFA'))
        self.MakeMenuBar()
        self.Layout()
        self.Fit()
        self.Centre()

    def MakeMenuBar(self):
        file_menu = wx.Menu()
        help_menu = wx.Menu()

        exit_item  = wx.MenuItem(file_menu, wx.ID_ANY, '&Quit\tCtrl-Q')
        github_link_item = wx.MenuItem(help_menu, wx.ID_ANY, 'Link to GitHub')
        buy_coffee_link_item = wx.MenuItem(help_menu, wx.ID_ANY, 'Support me')

        self.Bind(wx.EVT_MENU, self.OnExit, exit_item)
        self.Bind(wx.EVT_MENU, self.OnGithubLink, github_link_item)
        self.Bind(wx.EVT_MENU, self.OnBuyCoffeeLink, buy_coffee_link_item)
 
        file_menu.Append(exit_item)

        help_menu.Append(github_link_item)
        help_menu.Append(buy_coffee_link_item)

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(help_menu, '&Help')

        self.SetMenuBar(menu_bar)

    def OnExit(self, _):
        self.Close(True)

    def OnGithubLink(self, _):
        webbrowser.open('https://github.com/dododo25/renpy-cracken', new=0, autoraise=True)

    def OnBuyCoffeeLink(self, _):
        webbrowser.open('https://ko-fi.com/dododo25', new=0, autoraise=True)
