#!/usr/bin/python
import wx

from ui import PhotoOrganizerWindow
from plugins import load_plugins

import logging


class PhotoOrganizer(wx.App):
    def OnInit(self):
        frame = PhotoOrganizerWindow(None)
        load_plugins(frame)

        frame.Show()
        self.SetTopWindow(frame)
        return True

#
# Run the program
if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    app = PhotoOrganizer()
#     import wx.lib.inspection
#     wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
