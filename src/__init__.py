#!/usr/bin/python
import wx

from ui import PhotoOrganizerWindow



class PhotoOrganizer(wx.App):
    def OnInit(self):
        frame = PhotoOrganizerWindow(None)
        frame.Show()
        self.SetTopWindow(frame)
        return True
 
# 
# Run the program
if __name__ == '__main__':
    app = PhotoOrganizer()
#     import wx.lib.inspection
#     wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
