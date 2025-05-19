import os
import panels
import webbrowser
import wx

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        main_panel = wx.Panel(self)

        control_panel = panels.ControlPanel(main_panel)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(control_panel, 1, wx.ALIGN_CENTER)

        main_panel.SetSizer(sizer)

        self.SetBackgroundColour(wx.Colour('#FAFAFA'))
        self.MakeMenuBar()
        self.SetSize(800, 500)
        self.SetMinSize((800, 500))
        self.Centre()

    def MakeMenuBar(self):
        file_menu = wx.Menu()
        help_menu = wx.Menu()

        exit_item  = wx.MenuItem(file_menu, wx.ID_ANY, '&Quit\tCtrl-Q')
        github_link_item = wx.MenuItem(help_menu, wx.ID_ANY, 'GitHub')
        buy_coffee_link_item = wx.MenuItem(help_menu, wx.ID_ANY, 'Support this project')

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
        webbrowser.open('https://www.google.com/', new=0, autoraise=True)

if __name__ == '__main__':
    app = wx.App()

    frame = MainFrame(None, title='Ren\'Py Cracken')

    icon_bitmap = wx.Bitmap(os.path.join(os.path.split(__file__)[0], 'icon.ico'), wx.BITMAP_TYPE_ICO)
    icon = wx.Icon(icon_bitmap)

    frame.SetIcon(icon)
    frame.Show()

    app.MainLoop()
