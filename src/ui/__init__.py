from __future__ import division

import json
import os
from StringIO import StringIO

import wx
import peewee
from send2trash import send2trash

from ui.generated import PhotoOrganizerFrame
from ui.helpers import scale_bitmap
from models import File, Metadata
import query

import logging
from os import path
from peewee import IntegrityError
from _collections import defaultdict
from datetime import datetime
logger = logging.getLogger(__name__)


class PhotoOrganizerWindow( PhotoOrganizerFrame ):
    def __init__(self, parent):
        super(type(self),self).__init__(parent)
        self.add_dir = "~/Pictures"
        self._preview = None    # Track the currently selected image, by md5.
        self._filter = ""       # Track the current Filter
        self.filters = []       # Track previous Filters.

        # Only update the preview when we stop changing the list selection
        self.list_change_timer = wx.Timer(self)
        
        # Load the Grid
        self.thumbnail_index = {}
        self.thumbnails = wx.ImageList()
        self.thumbnailGrid.SetImageList(self.thumbnails, wx.IMAGE_LIST_NORMAL)
        for f in File.select():
            self.thumbnail_index[f.md5] = self.thumbnails.Add(f.as_bitmap())
        self.update_thumbnails()
        self.SetStatusText("Matching Images: %s" % self.thumbnailGrid.ItemCount)
        self.update_tags()

    @property
    def filter(self):
        return self._filter
    
    @filter.setter
    def filter(self, value):
        self._filter = value
        
        if value.strip() != "":
            self.update_filters(value)
        self.FilterBox.SetValue(str(self.filter))
        self.update_thumbnails()
        self.SetStatusText("Matching Images: %s" % self.thumbnailGrid.ItemCount)

    @property
    def preview(self):
        return self._preview

    @preview.setter
    def preview(self, value):
        self._preview = value
        self.update_metadata(File.get(md5=value).get_metadata())
        self.update_preview()

    def AddFileButtonOnMenuSelection(self, event):
        selectDialog = wx.FileDialog(self, "Add File(s)", self.add_dir, "", style=wx.FD_OPEN|wx.FD_MULTIPLE)
        if selectDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        self.add_dir = path.dirname(selectDialog.GetPaths()[0])
        self.import_files(selectDialog.GetPaths())

    def AddFolderButtonOnMenuSelection(self, event):
        selectDialog = wx.DirDialog(self, "Choose Image Directory", "", wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST)
        if selectDialog.ShowModal() == wx.ID_CANCEL:
            return
        
        # Add files.
        new_files = []
        for root, subFolders, files in os.walk(selectDialog.GetPath()):
            for file in files:
                new_files.append(os.path.join(root, file))
        self.import_files(new_files)

    def DebugMenuItemOnMenuSelection(self, event):
        import pdb
        pdb.set_trace()

    def ExitButtonOnMenuSelection( self, event ):
        self.Close()

    def PreviewOnSize(self, event):
        self.update_preview()

    def thumbnailGridOnChar(self, event):
        if event.GetKeyCode() in [ord(i) for i in ['t', 'T']]:
            self.handle_T_key()
        elif event.GetKeyCode() == wx.WXK_DELETE and event.shiftDown == False:
            self.handle_backspace_key()
        elif event.GetKeyCode() == wx.WXK_DELETE and event.shiftDown == True:
            self.handle_delete_key()
        else:
            event.Skip(True)

    def handle_T_key(self):
                # Get the File objects corresponding to the selected thumbnails
        files = File.select().where(File.md5 << [item.Text for item in self.get_selected_thumbs()])
        
        # Determine the existing tags for these files.
        old_tags = Metadata.filter(Metadata.file << files, Metadata.field.not_in(['import-time']))
        old_tags = sorted(list(set(['%s:"%s"' % (t.field, t.value) for t in old_tags])))
        
        dialog = wx.TextEntryDialog(None, "Tags:", "Modifiy Tags", value=", ".join(old_tags))
        if dialog.ShowModal() == wx.ID_OK:
            
            # Determine the new tags for these files.
            new_tags = dialog.GetValue()
            new_tags = [t.strip() for t in new_tags.split(",")]
            
            # Add any new tags that have been added.
            for token in set(new_tags) - set(old_tags):
                # Determine the actual field and tags
                if ':' in token:
                    field, value = token.split(':', 1)
                else:
                    field, value = 'tag', token
                # Create records for all selected files.
                for file in files:
                    try:
                        Metadata(file=file, field=field, value=value).save()
                    except IntegrityError:
                        pass
            
            # Remove any tags that were removed.
            removed_tags = list(set(old_tags) - set(new_tags))
            query = Metadata.delete().where(Metadata.file << files, 
                                    Metadata.field == "tag", 
                                    Metadata.value << removed_tags).execute()
        # Repaint the tag list.
        self.update_tags()

    def handle_backspace_key(self):
        confirmDialog = wx.MessageDialog(self, 
                                         "Remove %s Files?" % self.thumbnailGrid.SelectedItemCount, 
                                         "Remove Files?", 
                                         style=wx.OK|wx.CANCEL)
        confirmDialog.SetOKLabel("Delete")
        if confirmDialog.ShowModal() == wx.ID_OK:
            files = File.select().where(File.md5 << [item.Text for item in self.get_selected_thumbs()])
            for file in files:
                file.delete_instance(recursive=True)
            # Repaint the tag list.
            self.update_tags()
            self.update_thumbnails()
            self.preview = None

    def handle_delete_key(self):
        confirmDialog = wx.MessageDialog(self, 
                                         "Delete %s Files?" % self.thumbnailGrid.SelectedItemCount, 
                                         "Delete Files?", 
                                         style=wx.OK|wx.CANCEL)
        confirmDialog.SetOKLabel("Delete")
        if confirmDialog.ShowModal() == wx.ID_OK:
            files = File.select().where(File.md5 << [item.Text for item in self.get_selected_thumbs()])
            for file in files:
                send2trash(file.path)
                file.delete_instance(recursive=True)
            # Repaint the tag list.
            self.update_tags()
            self.update_thumbnails()
            self.preview = None

    def thumbnailGridOnListItemSelected(self, event):
        item = event.Item
        def change_selection(_):
            if item.Text == self.thumbnailGrid.GetItem(self.thumbnailGrid.GetFocusedItem()).Text:
                self.preview = item.Text

        self.Unbind(wx.EVT_TIMER)
        self.Bind(wx.EVT_TIMER, change_selection, self.list_change_timer)
        self.list_change_timer.StartOnce(100)

    def FilterBoxOnTextEnter( self, event ):
        """On filter box enter update the internal filter and update the thumbnails"""
        self.filter = self.FilterBox.GetValue()

    def FilterButtonOnButtonClick( self, event ):
        """On filter button click update the internal filter and update the thumbnails"""
        self.filter = self.FilterBox.GetValue()

    def TagTreeOnTreeSelChanged(self, event):
        """On tag selection update the internal filter and filter box text and update the thumbnails"""
        if event.Item == self.TagTree.GetRootItem():
            self.filter = ""
        elif self.TagTree.GetItemParent(event.Item) == self.TagTree.GetRootItem():
            self.filter = "has \"%s\"" % self.TagTree.GetItemText(event.Item)
        else:
            field = self.TagTree.GetItemText(self.TagTree.GetItemParent(event.Item))
            tag   = self.TagTree.GetItemText(event.Item)
            self.filter = "%s:\"%s\"" % (field, tag)

    def DetailsWindowOnHtmlLinkClicked( self, event ):
        self.filter = event.GetLinkInfo().Href

    def import_files(self, files):
        # Create the new files, and update the thumnail_index with any new files
        import_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_files = filter(None, (File.create_from_file(path) for path in files))
        for f in new_files:
            self.thumbnail_index[f.md5] = self.thumbnails.Add(f.as_bitmap())
        
        # If there are any new files we need to re layout the thumbnailGrid
        if len(new_files) > 0:
            self.update_thumbnails()
            self.update_tags()
            self.preview = new_files[0].md5
        
        return new_files

    def update_thumbnails(self):
        self.thumbnailGrid.ClearAll()
        data = query.parse(self.filter)
        for i, f in enumerate(data):
            item = wx.ListItem()
            # Set image
            item.SetImage(self.thumbnail_index[f.md5])
            item.SetId(i)
            item.SetText(f.md5)
            
            self.thumbnailGrid.InsertItem(item)

    def update_tags(self):
        self.TagTree.DeleteAllItems()
        root = self.TagTree.RootItem
        root = self.TagTree.AppendItem(root, "root")
        for item in Metadata.select(Metadata.field).distinct().order_by(Metadata.field):
            field = self.TagTree.AppendItem(root, item.field)
            results = Metadata.select(Metadata.value).distinct().order_by(Metadata.value)
            results = results.where(Metadata.field==item.field)
            for record in results:
                self.TagTree.AppendItem(field, record.value)
            self.TagTree.Expand(field)

    def update_preview(self):
        if self.preview == None:
            return
        
        # The logic for creating a accurate image as large as can be seen
        preview = wx.Image()
        preview.LoadFile(File.get(md5=self.preview).path)
        
        width, height = self.PreviewPanel.GetSize()
        hRatio = height / preview.Height
        wRatio = width / preview.Width 
        ratio = min(hRatio, wRatio)
        image = preview.Scale(preview.Width * ratio, preview.Height * ratio, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        # set the Result.
        self.Preview.SetBitmap(result)

    def update_filters(self, item):
        if item in self.filters:
            self.filters.remove(item)
        self.filters.insert(0, item)
        if len(self.filters) > 10:
            self.filters = self.filters[:10]
        self.FilterBox.Clear()
        self.FilterBox.AppendItems(self.filters)

    def update_metadata(self, metadata):
        # Handle Static markup
        markup = ""
        markup += "<b>Name:</b> %s<br />" % metadata['name']
        markup += "<b>Path:</b> %s<br />" % metadata['path']
        markup += "<b>md5:</b> %s<br />" % metadata['md5']
        markup += "<b>Width:</b> %s<br />" % metadata['width']
        markup += "<b>Height:</b> %s<br />" % metadata['height']
        markup += "<b>Type:</b> %s<br />" % metadata['type']
        markup += "<b>size:</b> %s<br />" % metadata['size']
        
        # Handle dynamic Markup
        fields = defaultdict(set)
        for m in metadata['metadata']:
            fields[m.field].add(m.value)
        
        for field, values in fields.items():
            links = ["<a href='%s:\"%s\"'>%s</a>" % (field, value, value) for value in values]
            markup += "<b>%s:</b> %s<br />" % (field, ", ".join(links))
        
        self.DetailsWindow.SetPage(markup)

    def get_selected_thumbs(self):
        selection = [self.thumbnailGrid.GetFirstSelected()]
        while len(selection) < self.thumbnailGrid.SelectedItemCount:
            selection.append(self.thumbnailGrid.GetNextSelected(selection[-1]))
        return [self.thumbnailGrid.GetItem(i) for i in selection] 
