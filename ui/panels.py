import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.split(__file__)[0], '..')))

import cracken
import dialogs
import threading
import wx
import wx.lib.scrolledpanel

class FilePanel(wx.Panel):

    def __init__(self, parent, id, label):
        super(FilePanel, self).__init__(parent, id, style = wx.EXPAND | wx.ALL)

        if sys._MEIPASS:
            close_image_bitmap = wx.Bitmap(os.path.join(sys._MEIPASS, 'close.png'), wx.BITMAP_TYPE_PNG)
        else:
            close_image_bitmap = wx.Bitmap(os.path.join(os.path.split(__file__)[0], 'close.png'), wx.BITMAP_TYPE_PNG)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.delete_image_bitmap = wx.StaticBitmap(self, wx.ID_ANY, close_image_bitmap)
        self.delete_image_bitmap.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        sizer.Add(wx.StaticText(self, wx.ID_ANY, label=label), 0)
        sizer.AddStretchSpacer()
        sizer.Add(self.delete_image_bitmap, 0)

        self.SetSizer(sizer)

class ControlPanel(wx.Panel):

    def __init__(self, *args, **kw):
        def add_file_button_clicked(_):
            with wx.FileDialog(self, 'Select a file', wildcard='RenPy files (*.rpyc;*.rpymc;*.rpa)|*.rpyc;*.rpymc;*.rpa',
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
                if fileDialog.ShowModal() != wx.ID_CANCEL:
                    self.append(fileDialog.GetPath())

        def add_folder_button_clicked(_):
            with wx.DirDialog(self, 'Select a folder',
                              style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dirDialog:
                if dirDialog.ShowModal() != wx.ID_CANCEL:
                    self.append(dirDialog.GetPath())

        def confirm_button_clicked(_):
            logs_dlg = dialogs.LogsDialog(self)

            def collect_all_files(regular_files: list[str], archive_files: list[str], event: threading.Event):
                def prepare_file(path):
                    if event.is_set():
                        return

                    if cracken.is_file(path):
                        regular_files.append(path)
                        logs_dlg.main_log_ctrl.AppendText('Found new file: %s\n' % path)
                    elif cracken.is_archive(path):
                        archive_files.append(path)
                        logs_dlg.main_log_ctrl.AppendText('Found new archive file: %s\n' % path)

                logs_dlg.label.SetLabel('Collecting files')

                files_panel_children = self.selected_files_panel.GetChildren()

                for i, child in enumerate(files_panel_children):
                    cracken.collect_files(child.GetChildren()[1].GetLabelText(), prepare_file)
                    logs_dlg.progress_bar.SetValue(int((i + 1) * 25 / len(files_panel_children)))

                logs_dlg.progress_bar.SetValue(25)

            def process_archive_files(regular_files: list[str], archive_files: list[str], recursive: bool, event: threading.Event):
                def prepare_file(path):
                    if event.is_set():
                        return

                    if cracken.is_file(path):
                        regular_files.append(path)
                        logs_dlg.main_log_ctrl.AppendText('Found new file: %s\n' % path)
                    elif cracken.is_archive(path):
                        archive_files.append(path)
                        logs_dlg.main_log_ctrl.AppendText('Found new archive file: %s\n' % path)

                logs_dlg.label.SetLabel('Processing .rpa files')

                index = 0

                while archive_files:
                    path = archive_files[index]

                    logs_dlg.main_log_ctrl.AppendText('%s - trying to process\n' % path)

                    cracken.process_archive_file(path, recursive, prepare_file)

                    logs_dlg.main_log_ctrl.AppendText('%s - processed\n' % path)
                    logs_dlg.progress_bar.SetValue(25 + int((index + 1) * 25 / len(archive_files)))

                    index += 1

                logs_dlg.progress_bar.SetValue(50)

            def process_regular_files(files: list[str], prettify: bool):
                logs_dlg.label.SetLabel('Processing .rpyc files')

                for index, path in enumerate(files):
                    logs_dlg.main_log_ctrl.AppendText('%s - trying to process\n' % path)

                    cracken.process_file(path, prettify)

                    logs_dlg.main_log_ctrl.AppendText('%s - processed\n' % path)
                    logs_dlg.progress_bar.SetValue(50 + int((index + 1) * 25 / len(files)))

                logs_dlg.progress_bar.SetValue(75)

            def remove_old_files(files: list[str]):
                logs_dlg.label.SetLabel('Remove old files')

                for i, path in enumerate(files):
                    logs_dlg.main_log_ctrl.AppendText('%s - trying to delete\n' % path)

                    os.remove(path)

                    logs_dlg.main_log_ctrl.AppendText('%s - deleted\n' % path)
                    logs_dlg.progress_bar.SetValue(75 + int((i + 1) * 25 / len(files)))

                logs_dlg.progress_bar.SetValue(100)

            def process_data(event):
                try:
                    regular_files = []
                    archive_files = []

                    recursive   = recursive_search_checkbox.GetValue()
                    clean_after = clear_after_search_checkbox.GetValue()
                    prettify    = prettify_code_checkbox.GetValue()

                    collect_all_files(regular_files, archive_files, event)
                    process_archive_files(regular_files, archive_files, recursive, event)
                    process_regular_files(regular_files, prettify)

                    if clean_after:
                        remove_old_files(archive_files)

                    logs_dlg.progress_bar.SetValue(100)
                    logs_dlg.label.SetLabel('Done')
                except (ModuleNotFoundError, AttributeError) as e:
                    logs_dlg.label.SetLabel('Error - check out logs')
                    logs_dlg.progress_bar.SetValue(0)
                    logs_dlg.main_log_ctrl.AppendText('Error %s: %s' % (e.__class__.__name__, e))
                except RuntimeError:
                    pass

            thread_event = threading.Event()
            thread = threading.Thread(target=process_data, args=(thread_event, ), daemon=True)

            def stop_thread(_):
                thread_event.set()
                logs_dlg.Destroy()
                self.Enable()

            logs_dlg.Bind(wx.EVT_CLOSE, stop_thread)
            logs_dlg.SetSize((600, 375))
            logs_dlg.SetMinSize((600, 375))
            logs_dlg.Center()

            self.Disable()
            logs_dlg.Show()
            thread.start()

        super(ControlPanel, self).__init__(*args, **kw)

        welcome_label     = wx.StaticText(self, label='Welcome to Ren\'Py Craken')
        description_label = wx.StaticText(self, label='In just three steps this app will decompile your .rpyc \\ .rpa files')
        step1_label       = wx.StaticText(self, label='Step 1')
        step2_label       = wx.StaticText(self, label='Step 2')
        step3_label       = wx.StaticText(self, label='Step 3')
        or_label          = wx.StaticText(self, label='or')

        add_file_button   = wx.Button(self, label='Add a file')
        add_folder_button = wx.Button(self, label='Add a folder')

        recursive_search_checkbox   = wx.CheckBox(self, label='Additional search inside of .rpa files')
        clear_after_search_checkbox = wx.CheckBox(self, label='Delete .rpa files after that all files are processed')
        prettify_code_checkbox      = wx.CheckBox(self, label='Try to make code more pretty')

        self.confirm_button = wx.Button(self, label='Start')
        self.selected_files_panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(500, 100), style=wx.NO_BORDER)
        self.files_sizer = wx.BoxSizer(wx.VERTICAL)

        s0   = wx.BoxSizer(wx.VERTICAL)
        s0_1 = wx.BoxSizer(wx.HORIZONTAL)
        s1   = wx.BoxSizer(wx.VERTICAL)
        s1_1 = wx.BoxSizer(wx.HORIZONTAL)
        s2   = wx.BoxSizer(wx.VERTICAL)
        s3   = wx.BoxSizer(wx.VERTICAL)

        welcome_label.SetFont(wx.Font(wx.FontInfo(20).Bold()))
        description_label.SetFont(wx.Font(wx.FontInfo(10)))
        step1_label.SetFont(wx.Font(wx.FontInfo(12).Bold()))
        step2_label.SetFont(wx.Font(wx.FontInfo(12).Bold()))
        step3_label.SetFont(wx.Font(wx.FontInfo(12).Bold()))

        add_file_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.Bind(wx.EVT_BUTTON, add_file_button_clicked, add_file_button)

        add_folder_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.Bind(wx.EVT_BUTTON, add_folder_button_clicked, add_folder_button)

        recursive_search_checkbox.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        clear_after_search_checkbox.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        prettify_code_checkbox.SetCursor(wx.Cursor(wx.CURSOR_HAND))

        self.confirm_button.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.confirm_button.Disable()
        self.Bind(wx.EVT_BUTTON, confirm_button_clicked, self.confirm_button)

        self.selected_files_panel.SetSizer(self.files_sizer)
        self.selected_files_panel.SetupScrolling()

        self.files_sizer.Fit(self.selected_files_panel)

        s1_1.Add(add_file_button)
        s1_1.AddSpacer(4)
        s1_1.Add(or_label, 0, wx.ALIGN_CENTER_VERTICAL)
        s1_1.AddSpacer(4)
        s1_1.Add(add_folder_button)

        s1.AddSpacer(64)
        s1.Add(step1_label, 0, wx.CENTER)
        s1.AddSpacer(8)
        s1.Add(s1_1, 0, wx.CENTER)

        s2.AddSpacer(64)
        s2.Add(step2_label, 0, wx.CENTER)
        s2.AddSpacer(8)
        s2.Add(recursive_search_checkbox, 0)
        s2.Add(clear_after_search_checkbox, 0)
        s2.Add(prettify_code_checkbox, 0)

        s3.AddSpacer(64)
        s3.Add(step3_label, 0, wx.CENTER)
        s3.AddSpacer(8)
        s3.Add(self.confirm_button, 0, wx.CENTER)

        s0_1.Add(s1, 1, wx.TOP, 5)
        s0_1.AddSpacer(8)
        s0_1.Add(wx.StaticLine(self, style=wx.LI_VERTICAL, size=(1, 200)), 0, wx.CENTER)
        s0_1.AddSpacer(16)
        s0_1.Add(s2, 1, wx.TOP, 5)
        s0_1.AddSpacer(8)
        s0_1.Add(wx.StaticLine(self, style=wx.LI_VERTICAL, size=(1, 200)), 0, wx.CENTER)
        s0_1.AddSpacer(4)
        s0_1.Add(s3, 1, wx.TOP, 5)

        s0.AddSpacer(12)
        s0.Add(welcome_label, 0, wx.CENTER)
        s0.AddSpacer(8)
        s0.Add(description_label, 1, wx.CENTER)
        s0.AddSpacer(8)
        s0.AddStretchSpacer()
        s0.AddSpacer(8)
        s0.Add(s0_1, 1, wx.CENTER)
        s0.AddSpacer(20)
        s0.AddStretchSpacer()
        s0.Add(self.selected_files_panel, 1, wx.ALIGN_CENTER)
        s0.AddSpacer(16)

        self.SetSizer(s0)

    def append(self, path: str):
        for child in self.selected_files_panel.GetChildren():
            label = child.GetChildren()[0].GetLabelText()

            if path == label:
                return

        p = FilePanel(self.selected_files_panel, wx.ID_ANY, path)
        p.delete_image_bitmap.Bind(wx.EVT_LEFT_DOWN, lambda _: self._delete_panel(p))

        self.files_sizer.Add(p, 0, wx.EXPAND)
        self.files_sizer.Layout()
        self.confirm_button.Enable()

    def _delete_panel(self, panel: wx.Panel):
        panel.Hide()
        panel.Destroy()

        if len(self.selected_files_panel.GetChildren()) == 0:
            self.confirm_button.Disable()
        else:
            self.confirm_button.Enable()

        self.files_sizer.Layout()
