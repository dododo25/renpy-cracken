import logging
import os
import sys
import wx

from ui import frames

log_filename = 'logs/cracken.log'

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)4s - %(filename)s:%(lineno)s - %(message)s')

if __name__ == '__main__':
    app = wx.App()

    frame = frames.MainFrame(None, title='Ren\'Py Cracken')

    logo_directory = None

    if hasattr(sys, '_MEIPASS:'):
        logo_directory = sys._MEIPASS
    else:
        logo_directory = os.path.split(__file__)[0]

    icon = wx.Icon(wx.Bitmap(os.path.join(logo_directory, 'resources', 'logo.png'), wx.BITMAP_TYPE_PNG))

    frame.SetIcon(icon)
    frame.Show()

    app.MainLoop()
