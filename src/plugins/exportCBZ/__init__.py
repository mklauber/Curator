
import query
from types import MethodType
import wx
import zipfile


def ExportCBZOnMenuSelection(self, event):
    saveFileDialog = wx.FileDialog(self, "Choose CBZ file", "", "",
                                   "CBZ files (*.cbz)|*.cbz", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

    if saveFileDialog.ShowModal() == wx.ID_CANCEL:
        return     # the user changed idea...

    zf = zipfile.ZipFile(saveFileDialog.GetPath(), 'w')

    files = query.parse(self.filter)
    for file in files:
        zf.write(file.path)
    zf.close()


def apply(window):
    pos = window.FileMenu.MenuItemCount - 1

    # Create interface elements
    window.ExportCBZ = wx.MenuItem(window.FileMenu, wx.ID_ANY, u"Export to CBZ...", wx.EmptyString, wx.ITEM_NORMAL)
    window.FileMenu.Insert(pos, window.ExportCBZ)

    window.FileMenu.InsertSeparator(pos+1)

    # Create event handlers
    window.ExportCBZOnMenuSelection = MethodType(ExportCBZOnMenuSelection, window)

    # Bind handlers to elements
    window.Bind(wx.EVT_MENU, window.ExportCBZOnMenuSelection, id=window.ExportCBZ.GetId())
