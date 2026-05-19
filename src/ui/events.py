import wx
import wx.lib.newevent

NewFileReceivedEvent, EVT_NEW_FILE_RECEIVED     = wx.lib.newevent.NewCommandEvent()
StartNewProcessCommandEvent, EVT_START_NEW_PROCESS_COMMAND = wx.lib.newevent.NewCommandEvent()
