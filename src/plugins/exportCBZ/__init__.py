import math
from os import path
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
    offset = int(math.log10(len(files))+.5) # Round up
    for i, file in enumerate(files):
        name = '%s-%s' % (str(i).zfill(offset), path.basename(file.path))
        zf.write(file.path, name)
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
