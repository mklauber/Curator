import wx
from types import MethodType


def DebugMenuItemOnMenuSelection(self, event):
    import pdb
    pdb.set_trace()


def apply(window):
    # Create interface elements
    window.DebugMenuItem = wx.MenuItem(window.HelpMenu, wx.ID_ANY, u"Debug", wx.EmptyString, wx.ITEM_NORMAL)
    window.HelpMenu.Append(window.DebugMenuItem)

    # Create event handlers
    window.DebugMenuItemOnMenuSelection = MethodType(DebugMenuItemOnMenuSelection, window)

    # Bind handlers to elements
    window.Bind(wx.EVT_MENU, window.DebugMenuItemOnMenuSelection, id=window.DebugMenuItem.GetId())
