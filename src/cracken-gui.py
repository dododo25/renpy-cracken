import cracken
import logging
import os
import sys
import threading
import wx

from ui import dialogs, events, frames

log_filename = 'logs/cracken.log'

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)4s - %(filename)s:%(lineno)s - %(message)s')

def collect_all_files(logs_dlg, regular_files: list[str], archive_files: list[str], files: list[str], event: threading.Event):
    def prepare_file(path):
        if event.is_set():
                return

        if cracken.is_file(path):
            regular_files.append(path)
            wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, 'Found new file: %s\n' % path)
        elif cracken.is_archive(path):
            archive_files.append(path)
            wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, 'Found new archive file: %s\n' % path)

    logs_dlg.label.SetLabel('Collecting files')

    for i, child in enumerate(files):
        cracken.collect_files(child, prepare_file)
        logs_dlg.progress_bar.SetValue(int((i + 1) * 25 / len(files)))

    logs_dlg.progress_bar.SetValue(25)

def process_archive_files(logs_dlg, regular_files: list[str], archive_files: list[str], recursive: bool, event: threading.Event):
    def prepare_file(path):
        if event.is_set():
            return

        if cracken.is_file(path):
            regular_files.append(path)
            wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, 'Found new file: %s\n' % path)
        elif cracken.is_archive(path):
            archive_files.append(path)
            wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, 'Found new archive file: %s\n' % path)

    logs_dlg.label.SetLabel('Processing .rpa files')

    index = 0

    while archive_files:
        path = archive_files[index]

        wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, '%s - trying to process\n' % path)
        cracken.process_archive_file(path, recursive, prepare_file)
        wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, '%s - processed\n' % path)
        logs_dlg.progress_bar.SetValue(25 + int((index + 1) * 25 / len(archive_files)))

        index += 1

    logs_dlg.progress_bar.SetValue(50)

def process_regular_files(logs_dlg, files: list[str], prettify: bool):
    logs_dlg.label.SetLabel('Processing .rpyc files')

    for index, path in enumerate(files):
        wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, '%s - trying to process\n' % path)
        cracken.process_file(path, prettify)
        wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, '%s - processed\n' % path)
        logs_dlg.progress_bar.SetValue(50 + int((index + 1) * 25 / len(files)))

    logs_dlg.progress_bar.SetValue(75)

def remove_old_files(logs_dlg, files: list[str]):
    logs_dlg.label.SetLabel('Remove old files')

    for i, path in enumerate(files):
        wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, '%s - trying to delete\n' % path)
        os.remove(path)
        wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, '%s - deleted\n' % path)
        logs_dlg.progress_bar.SetValue(75 + int((i + 1) * 25 / len(files)))

    logs_dlg.progress_bar.SetValue(100)

def process_data(logs_dlg, files, recursive_search, clear_after_search, prettify, thread_event):
    try:
        regular_files = []
        archive_files = []

        collect_all_files(logs_dlg, regular_files, archive_files, files, thread_event)
        process_archive_files(logs_dlg, regular_files, archive_files, recursive_search, thread_event)
        process_regular_files(logs_dlg, regular_files, prettify)

        if clear_after_search:
            remove_old_files(logs_dlg, archive_files)

        logs_dlg.progress_bar.SetValue(100)
        logs_dlg.label.SetLabel('Done')
        wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, '\nAll done.')
    except (ModuleNotFoundError, AttributeError, TypeError) as e:
        logs_dlg.label.SetLabel('Error - check out log file to find out why')
        logs_dlg.progress_bar.SetValue(0)
        wx.CallAfter(logs_dlg.main_log_ctrl.AppendText, 'Error %s: %s' % (e.__class__.__name__, e))
    except RuntimeError:
        pass

def new_process_started(evt, frame):
    def stop_thread(_):
        thread_event.set()
        logs_dlg.Destroy()

        frame.panel.removeAllPaths()

        frame.Layout()
        frame.Refresh()
        frame.Enable()

    logs_dlg = dialogs.LogsDialog(frame)

    thread_event = threading.Event()
    thread = threading.Thread(target=process_data, args=(
        logs_dlg, 
        evt.files, 
        evt.recursive_search, 
        evt.clear_after_search, 
        evt.prettify, 
        thread_event)
    )

    logs_dlg.Bind(wx.EVT_CLOSE, stop_thread)
    logs_dlg.SetSize((600, 375))
    logs_dlg.SetMinSize((600, 375))
    logs_dlg.Center()

    frame.Disable()
    logs_dlg.Show()
    thread.start()


if __name__ == '__main__':
    app = wx.App()

    frame = frames.MainFrame(None, title='Ren\'Py Cracken')

    logo_directory = None

    if hasattr(sys, '_MEIPASS:'):
        logo_directory = sys._MEIPASS
    else:
        logo_directory = os.path.split(__file__)[0]

    icon = wx.Icon(wx.Bitmap(os.path.join(logo_directory, 'images', 'logo.png'), wx.BITMAP_TYPE_PNG))

    frame.Bind(events.EVT_START_NEW_PROCESS_COMMAND, lambda evt: new_process_started(evt, frame))
    frame.SetIcon(icon)
    frame.Show()

    app.MainLoop()
