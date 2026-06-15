import cracken as cracken
import os
import platform
import sys
import wx
import wx.lib.scrolledpanel

from . import events

close_image_filepath = None

if hasattr(sys, '_MEIPASS:'):
    close_image_filepath = sys._MEIPASS
else:
    close_image_filepath = os.path.split(__file__)[0]

close_image_filepath = os.path.join(close_image_filepath, 'images', 'close.png')

spaces_modifier = 0.7 if platform.system() == 'Windows' else 1

class FilePanel(wx.Panel):

    def __init__(self, parent, id, path):
        super(FilePanel, self).__init__(parent, id, style = wx.EXPAND | wx.ALL)

        self.path = path

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        close_image_bitmap = wx.Bitmap(close_image_filepath, wx.BITMAP_TYPE_PNG)
        self.delete_image_bitmap = wx.StaticBitmap(self, wx.ID_ANY, close_image_bitmap)
        self.delete_image_bitmap.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        sizer.Add(wx.StaticText(self, wx.ID_ANY, label=path, size=wx.Size(460, 20), style=wx.ST_ELLIPSIZE_START), 0)
        sizer.AddStretchSpacer()
        sizer.Add(self.delete_image_bitmap, 0)

        self.SetSizer(sizer)

class TitlePanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(TitlePanel, self).__init__(*args, **kw)

        sizer = wx.BoxSizer(wx.VERTICAL)

        title_label       = wx.StaticText(self, label='Welcome to Ren\'Py Craken')
        description_label = wx.StaticText(self, label='In just three steps this app will decompile your .rpyc \\ .rpa files')

        title_label.SetFont(wx.Font(wx.FontInfo(20).Bold()))
        description_label.SetFont(wx.Font(wx.FontInfo(12)))

        sizer.Add(title_label, 0, wx.CENTER)
        sizer.AddSpacer(8)
        sizer.Add(description_label, 0, wx.CENTER)

        self.SetSizer(sizer)

class StepsPanel(wx.Panel):

    class Step1ActionsPanel(wx.Panel):

        def __init__(self, *args, **kw):
            def add_file_button_clicked(_):
                with wx.FileDialog(self, 'Select a file', wildcard='RenPy files (*.rpyc;*.rpymc;*.rpa)|*.rpyc;*.rpymc;*.rpa',
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                    if fileDialog.ShowModal() == wx.ID_CANCEL:
                        return

                    wx.PostEvent(self, events.NewFileReceivedEvent(id=wx.ID_ANY, path=fileDialog.GetPath()))

            def add_folder_button_clicked(_):
                with wx.DirDialog(self, 'Select a folder',
                                style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dirDialog:
                    if dirDialog.ShowModal() == wx.ID_CANCEL:
                        return

                    wx.PostEvent(self, events.NewFileReceivedEvent(id=wx.ID_ANY, path=dirDialog.GetPath()))

            super(StepsPanel.Step1ActionsPanel, self).__init__(*args)

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(self, label='or')

            self.add_file_button   = wx.Button(self, label='Add a file')
            self.add_folder_button = wx.Button(self, label='Add a folder')

            self.add_file_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.add_folder_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))

            self.Bind(wx.EVT_BUTTON, add_file_button_clicked, self.add_file_button)
            self.Bind(wx.EVT_BUTTON, add_folder_button_clicked, self.add_folder_button)

            sizer.Add(self.add_file_button)
            sizer.AddSpacer(4)
            sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL)
            sizer.AddSpacer(4)
            sizer.Add(self.add_folder_button)

            self.SetSizer(sizer)

    class Step1Panel(wx.Panel):

        def __init__(self, *args, **kw):
            super(StepsPanel.Step1Panel, self).__init__(*args)

            sizer = wx.BoxSizer(wx.VERTICAL)
            label = wx.StaticText(self, label='Step 1')

            self.actions = StepsPanel.Step1ActionsPanel(self, data=kw.get('data'))

            label.SetFont(wx.Font(wx.FontInfo(12).Bold()))

            sizer.Add(label, 0, wx.CENTER)
            sizer.AddSpacer(8)
            sizer.Add(self.actions, 0, wx.CENTER)

            self.SetSizer(sizer)

    class Step2Panel(wx.Panel):

        def __init__(self, *args, **kw):
            super(StepsPanel.Step2Panel, self).__init__(*args)

            sizer = wx.BoxSizer(wx.VERTICAL)
            label = wx.StaticText(self, label='Step 2')

            self.recursive_search_checkbox   = wx.CheckBox(self, label='Additional search inside of .rpa files')
            self.clear_after_search_checkbox = wx.CheckBox(self, label='Delete .rpa files after that all files are processed')
            self.prettify_code_checkbox      = wx.CheckBox(self, label='Try to make code more pretty')
            self.skip_on_error_checkbox      = wx.CheckBox(self, label='Don\'t interrupt a process if an error happens')

            label.SetFont(wx.Font(wx.FontInfo(12).Bold()))

            self.recursive_search_checkbox.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.clear_after_search_checkbox.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.prettify_code_checkbox.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.skip_on_error_checkbox.SetCursor(wx.Cursor(wx.CURSOR_HAND))

            self.Bind(wx.EVT_CHECKBOX, lambda evt: kw['data'].update({'recursive_search': evt.IsChecked()}), self.recursive_search_checkbox)
            self.Bind(wx.EVT_CHECKBOX, lambda evt: kw['data'].update({'clear_after_search': evt.IsChecked()}), self.clear_after_search_checkbox)
            self.Bind(wx.EVT_CHECKBOX, lambda evt: kw['data'].update({'prettify': evt.IsChecked()}), self.prettify_code_checkbox)
            self.Bind(wx.EVT_CHECKBOX, lambda evt: kw['data'].update({'skip_error': evt.IsChecked()}), self.skip_on_error_checkbox)

            sizer.Add(label, 0, wx.CENTER)
            sizer.AddSpacer(8)
            sizer.Add(self.recursive_search_checkbox, 0)
            sizer.AddSpacer(2)
            sizer.Add(self.clear_after_search_checkbox, 0)
            sizer.AddSpacer(2)
            sizer.Add(self.prettify_code_checkbox, 0)
            sizer.AddSpacer(2)
            sizer.Add(self.skip_on_error_checkbox, 0)

            self.SetSizer(sizer)

    class Step3Panel(wx.Panel):

        def __init__(self, *args, **kw):
            def send_start_process_event(_):
                wx.PostEvent(self, events.StartNewProcessCommandEvent(id=wx.ID_ANY, **kw['data']))

            super(StepsPanel.Step3Panel, self).__init__(*args)

            sizer = wx.BoxSizer(wx.VERTICAL)
            label = wx.StaticText(self, label='Step 3')

            self.confirm_button = wx.Button(self, label='Start')

            label.SetFont(wx.Font(wx.FontInfo(12).Bold()))

            self.Bind(wx.EVT_BUTTON, send_start_process_event, self.confirm_button)
            self.confirm_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.confirm_button.Disable()

            sizer.Add(label, 0, wx.CENTER)
            sizer.AddSpacer(8)
            sizer.Add(self.confirm_button, 0, wx.CENTER)

            self.SetSizer(sizer)

    def __init__(self, *args, **kw):
        super(StepsPanel, self).__init__(*args)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.step1_panel = StepsPanel.Step1Panel(self, data=kw.get('data'))
        self.step2_panel = StepsPanel.Step2Panel(self, data=kw.get('data'))
        self.step3_panel = StepsPanel.Step3Panel(self, data=kw.get('data'))

        sizer.Add(self.step1_panel, 1, wx.CENTER)
        sizer.AddSpacer(8)
        sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL, size=wx.Size(1, 200)), 0, wx.CENTER)
        sizer.AddSpacer(24)
        sizer.Add(self.step2_panel, 1, wx.CENTER)
        sizer.AddSpacer(24)
        sizer.Add(wx.StaticLine(self, style=wx.LI_VERTICAL, size=wx.Size(1, 200)), 0, wx.CENTER)
        sizer.AddSpacer(8)
        sizer.Add(self.step3_panel, 1, wx.CENTER)

        self.SetSizer(sizer)

class MainPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(MainPanel, self).__init__(*args, **kw)

        self.data = {'files': [], 'recursive_search' : False, 'clear_after_search': False, 'prettify': False, 'skip_error': False}

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.steps_panel = StepsPanel(self, data=self.data)

        self.selected_files_panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=wx.Size(500, 100), style=wx.NO_BORDER)
        self.selected_files_sizer = wx.BoxSizer(wx.VERTICAL)

        self.selected_files_panel.SetSizer(self.selected_files_sizer)
        self.selected_files_panel.SetupScrolling()
        self.selected_files_panel.SetMaxSize((500, 100))

        self.selected_files_sizer.Fit(self.selected_files_panel)
        self.Bind(events.EVT_NEW_FILE_RECEIVED, lambda evt: self.appendPath(evt.path))

        sizer.Add(TitlePanel(self), 0, wx.CENTER)
        sizer.AddSpacer(int(32 * spaces_modifier))
        sizer.Add(self.steps_panel, 0, wx.CENTER)
        sizer.AddSpacer(int(16 * spaces_modifier))
        sizer.Add(self.selected_files_panel, 0, wx.ALIGN_CENTER)
        sizer.AddSpacer(int(32 * spaces_modifier))

        self.SetSizer(sizer)

    def appendPath(self, path: str):
        for child in self.selected_files_panel.GetChildren():
            label = child.GetChildren()[0].GetLabelText()

            if path == label:
                return

        self.data['files'].append(path)

        p = FilePanel(self.selected_files_panel, wx.ID_ANY, path)
        p.delete_image_bitmap.Bind(wx.EVT_LEFT_DOWN, lambda _: self._delete_panel(p))

        self.selected_files_sizer.Add(p, 0, wx.EXPAND)
        self.selected_files_sizer.Layout()
        self.steps_panel.step3_panel.confirm_button.Enable()

        self.Layout()
        self.Refresh()

    def removePath(self, path: str):
        for child in self.selected_files_panel.GetChildren():
            label = child.GetChildren()[0].GetLabelText()

            if path == label:
                self._delete_panel(child)
                break

    def removeAllPaths(self):
        self.data['files'].clear()

        self.selected_files_sizer.Clear(delete_windows=True)
        self.steps_panel.step3_panel.confirm_button.Disable()

    def _delete_panel(self, panel: wx.Panel):
        self.data['files'].remove(panel.path)

        panel.Hide()
        panel.Destroy()

        if len(self.selected_files_panel.GetChildren()) == 0:
            self.steps_panel.step3_panel.confirm_button.Disable()

        self.selected_files_sizer.Layout()
