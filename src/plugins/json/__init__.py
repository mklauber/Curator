import wx
from types import MethodType
from collections import defaultdict
import json
import peewee

from models import File, Metadata
import query

import logging
logger = logging.getLogger(__name__)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def ImportJsonOnMenuSelection(self, event):
    openFileDialog = wx.FileDialog(self, "Open MEtadat file", "", "",
                                   "JSON files (*.json)|*.json", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

    if openFileDialog.ShowModal() == wx.ID_CANCEL:
        return     # the user changed idea...

    # proceed loading the file chosen by the user
    # this can be done with e.g. wxPython input streams:
    data = None
    with open(openFileDialog.GetPath(), 'r') as f:
        data = json.load(f)

    for md5, metadata in data.items():
        try:
            f = File.get(File.md5 == md5)
        except Exception as e:
            logger.error("Unable to get file for md5:%s", md5)
            logger.exception(e)
            continue    # Don't do more work with this file
        for field, values in metadata.items():
            if field == 'import-time':
                return
            for value in values:
                try:
                    Metadata(file=f, field=field, value=value).save()
                except peewee.IntegrityError as e:
                    logger.info("Duplicate metadata ignored (%s, %s, %s)", md5, field, value)
                except Exception as e:
                    logger.error("Unable to save metadata (%s, %s, %s)", md5, field, value)
                    logger.exception(e)
    self.update_metadata()
    self.update_tags()


def ExportJsonOnMenuSelection(self, event):
    files = query.parse(self.filter)

    def to_json(f):
        d = defaultdict(set)
        for m in Metadata.select().where(Metadata.file == f):
            d[m.field].add(m.value)
        return d

    data = {f.md5: to_json(f) for f in files}

    saveFileDialog = wx.FileDialog(self, "Save Metadata for %s files?" % len(data), "", "",
                                   "json files (*.json)|*.json", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

    if saveFileDialog.ShowModal() == wx.ID_CANCEL:
        return     # the user changed idea...

    try:
        with open(saveFileDialog.GetPath(), 'w') as f:
            json.dump(data, f, indent=2, cls=SetEncoder)
    except Exception as e:
        logger.error("Error saving JSON")
        logger.exception(e)


def apply(window):
    pos = window.FileMenu.MenuItemCount - 1
    # Create interface elements
    window.ImportJson = wx.MenuItem(window.FileMenu, wx.ID_ANY, u"Import from JSON...", wx.EmptyString, wx.ITEM_NORMAL)
    window.FileMenu.Insert(pos, window.ImportJson)

    window.ExportJson = wx.MenuItem(window.FileMenu, wx.ID_ANY, u"Export from JSON...", wx.EmptyString, wx.ITEM_NORMAL)
    window.FileMenu.Insert(pos+1, window.ExportJson)

    window.FileMenu.InsertSeparator(pos+2)

    # Create event handlers
    window.ImportJsonOnMenuSelection = MethodType(ImportJsonOnMenuSelection, window)
    window.ExportJsonOnMenuSelection = MethodType(ExportJsonOnMenuSelection, window)

    # Bind handlers to elements
    window.Bind(wx.EVT_MENU, window.ImportJsonOnMenuSelection, id=window.ImportJson.GetId())
    window.Bind(wx.EVT_MENU, window.ExportJsonOnMenuSelection, id=window.ExportJson.GetId())
