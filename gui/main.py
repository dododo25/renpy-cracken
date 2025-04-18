import platform
import subprocess
import wx

from file_tree_ctrl import FileTreeCtrl

RENPY_FILES_PATTERN = r'.*\.(rpyc|rpymc|rpa|rpi)'

files_tree_view: FileTreeCtrl | None = None

class ControlPanel(wx.Panel):

    def __init__(self, *args, **kw):
        def add_file_button_clicked(_):
            with wx.FileDialog(self, 'Select a file', wildcard='RenPy files (*.rpyc;*.rpymc;*.rpa)|*.rpyc;*.rpymc;*.rpa',
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() != wx.ID_CANCEL:
                    files_tree_view.AppendFileItem(fileDialog.GetPath())

        def add_folder_button_clicked(_):
            with wx.DirDialog(self, 'Select a folder',
                              style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dirDialog:
                if dirDialog.ShowModal() != wx.ID_CANCEL:
                    files_tree_view.AppendDirSubItems(dirDialog.GetPath())

        def confirm_button_clicked(_):
            if platform.system() == 'Windows':
                si = subprocess.STARTUPINFO()
                si.dwFlags = subprocess.CREATE_NEW_PROCESS_GROUP

                p = subprocess.Popen(['ping', '8.8.8.8'],
                                     #startupinfo=si,
                                     stdout=subprocess.PIPE)

                output = p.stdout.readline()

                while output:
                    print(output)
                    output = p.stdout.readline()

                returncode = p.wait()
                print(p, returncode)

        super(ControlPanel, self).__init__(*args, **kw)

        add_file_button   = wx.Button(self, label='Add a file')
        add_folder_button = wx.Button(self, label='Add a folder')
        confirm_button    = wx.Button(self, label='Start')

        or_label = wx.StaticText(self, label='or')

        recursive_search_checkbox   = wx.CheckBox(self, label='Additional search inside of .rpa files')
        clear_after_search_checkbox = wx.CheckBox(self, label='Delete .rpa files after that all files are processed')
        prettify_code_checkbox      = wx.CheckBox(self, label='Try to make code more pretty')

        s2 = wx.BoxSizer(wx.VERTICAL)
        s3 = wx.BoxSizer(wx.HORIZONTAL)

        self.Bind(wx.EVT_BUTTON, add_file_button_clicked, add_file_button)
        self.Bind(wx.EVT_BUTTON, add_folder_button_clicked, add_folder_button)
        self.Bind(wx.EVT_BUTTON, confirm_button_clicked, confirm_button)

        s3.Add(add_file_button, 0)
        s3.AddSpacer(4)
        s3.Add(or_label, 0, wx.ALIGN_CENTER_VERTICAL)
        s3.AddSpacer(4)
        s3.Add(add_folder_button)

        s2.Add(s3, 0, wx.CENTER)
        s2.Add(recursive_search_checkbox, 0, wx.CENTER)
        s2.Add(clear_after_search_checkbox, 0, wx.CENTER)
        s2.Add(prettify_code_checkbox, 0, wx.CENTER)
        s2.Add(confirm_button, 0, wx.CENTER)

        self.SetSizer(s2)
        self.SetBackgroundColour(wx.RED)

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        global files_tree_view

        #super(MainFrame, self).__init__(*args, **kw, style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        super(MainFrame, self).__init__(*args, **kw)

        main_panel = wx.Panel(self)

        files_tree_view = FileTreeCtrl(main_panel, pattern=RENPY_FILES_PATTERN, style=wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        control_panel = ControlPanel(main_panel)

        files_tree_view.SetMinSize((300, 600))

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(files_tree_view, 0, wx.EXPAND)
        sizer.Add(control_panel, 1, wx.EXPAND)

        main_panel.SetSizer(sizer)

        self.MakeMenuBar()
        self.SetSize(1000, 600)
        self.SetMinSize((800, 400))
        self.Centre()

    def MakeMenuBar(self):
        fileMenu = wx.Menu()

        helloItem = fileMenu.Append(-1, '&Hello...\tCtrl-H',
                'Help string shown in status bar for this menu item')

        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()

        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(helpMenu, '&Help')

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)

    def OnHello(self, event):
        wx.MessageBox('Hello again from wxPython')

    def OnAbout(self, event):
        wx.MessageBox('This is a wxPython Hello World sample',
                      'About Hello World',
                      wx.OK|wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()

    frm = MainFrame(None, title='renpy-cracker')
    frm.Show()

    app.MainLoop()