from __future__ import division

import wx
import peewee
from StringIO import StringIO
from ui.generated import PhotoOrganizerFrame
from ui.helpers import scale_bitmap


from models import File, Metadata
import query

import logging
from os import path
from peewee import IntegrityError
logger = logging.getLogger(__name__)


class PhotoOrganizerWindow( PhotoOrganizerFrame ):
    def __init__(self, parent):
        super(type(self),self).__init__(parent)
        self.add_dir = "~/Pictures"
        self._preview = None
        self.filter = ""

        # Only update the preview when we stop changing the list selection
        self.list_change_timer = wx.Timer(self)
        
        # Load the Grid
        self.thumbnail_index = {}
        self.thumbnails = wx.ImageList()
        self.thumbnailGrid.SetImageList(self.thumbnails, wx.IMAGE_LIST_NORMAL)
        for f in File.select():
            self.thumbnail_index[f.md5] = self.thumbnails.Add(f.as_bitmap())
        self.update_thumbnails()
        self.update_tags()
        

    @property
    def preview(self):
        return self._preview

    @preview.setter
    def preview(self, value):
        self._preview = value
        self.update_preview()

    def AddFileButtonOnMenuSelection(self, event):
        selectDialog = wx.FileDialog(self, "Add File(s)", self.add_dir, "", style=wx.FD_OPEN|wx.FD_MULTIPLE)
        if selectDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        self.add_dir = path.dirname(selectDialog.GetPaths()[0])
        self.preview = wx.Image(selectDialog.GetPaths()[0])
        
        # Create the new files, and update the thumnail_index with any new files
        new_files = filter(None, (File.create_from_file(path) for path in selectDialog.GetPaths()))
        for f in new_files:
            self.thumbnail_index[f.md5] = self.thumbnails.Add(f.as_bitmap())
        
        # If there are any new files we need to re layout the thumbnailGrid
        if len(new_files) > 0:
            self.update_thumbnails()

    def DebugMenuItemOnMenuSelection(self, event):
        import pdb
        pdb.set_trace()

    def ExitButtonOnMenuSelection( self, event ):
        self.Close()

    def PreviewPanelOnSize(self, event):
        self.update_preview()

    def thumbnailGridOnListKeyDown(self, event):
        if event.GetKeyCode() != 84:
            event.Skip(True)
            return
        
        # Get the File objects corresponding to the selected thumbnails
        files = File.select().where(File.md5 << [item.Text for item in self.get_selected_thumbs()])
        
        # Determine the existing tags for these files.
        old_tags = Metadata.filter(Metadata.file << files)
        old_tags = [t.value for t in old_tags]
        
        dialog = wx.TextEntryDialog(None, "Tags:", "Modifiy Tags", value=", ".join(old_tags))
        if dialog.ShowModal() == wx.ID_OK:
            
            # Determine the new tags for these files.
            new_tags = dialog.GetValue()
            new_tags = [t.strip() for t in new_tags.split(",")]
            
            # Add any new tags that have been added.
            for tag in set(new_tags) - set(old_tags):
                for file in files:
                    try:
                        Metadata(file=file, field="tag", value=tag).save()
                    except IntegrityError:
                        pass
            
            # Remove any tags that were removed.
            removed_tags = list(set(old_tags) - set(new_tags))
            query = Metadata.delete().where(Metadata.file << files, 
                                    Metadata.field == "tag", 
                                    Metadata.value << removed_tags).execute()
        # Repaint the tag list.
        self.update_tags()

    def thumbnailGridOnListItemSelected(self, event):
        item = event.Item
        def change_selection(_):
            if item.Text == self.thumbnailGrid.GetItem(self.thumbnailGrid.GetFocusedItem()).Text:
                file = File.get(md5=item.Text)
                image = wx.Image()
                image.LoadFile(file.path)
                self.preview = image

        self.Unbind(wx.EVT_TIMER)
        self.Bind(wx.EVT_TIMER, change_selection, self.list_change_timer)
        self.list_change_timer.StartOnce(100)

    def FilterBoxOnTextEnter( self, event ):
        """On filter box enter update the internal filter and update the thumbnails"""
        self.filter = self.FilterBox.GetValue()
        self.update_thumbnails()

    def FilterButtonOnButtonClick( self, event ):
        """On filter button click update the internal filter and update the thumbnails"""
        self.filter = self.FilterBox.GetValue()
        self.update_thumbnails()

    def TagTreeOnTreeSelChanged(self, event):
        """On tag selection update the internal filter and filter box text and update the thumbnails"""
        if event.Item == self.TagTree.GetRootItem():
            self.filter = ""
        else:
            self.filter = "tag:%s" % self.TagTree.GetItemText(event.Item)
        self.FilterBox.SetValue(str(self.filter))
        self.update_thumbnails()

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
        root = self.TagTree.AppendItem(root, "Tags")
        query = Metadata.select().where(Metadata.field=='tag')
        for tag in set(t.value for t in query):
            self.TagTree.AppendItem(root, tag)
        self.TagTree.Expand(root)

    def update_preview(self):
        if self.preview == None:
            return
        
        # The logic for creating a accurate image as large as can be seen
        width, height = self.PreviewPanel.GetSize()
        hRatio = height / self.preview.Height
        wRatio = width / self.preview.Width 
        ratio = min(1, hRatio, wRatio) # Don't blow up images.
        image = self.preview.Scale(self.preview.Width * ratio, self.preview.Height * ratio, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        # set the Result.
        self.Preview.SetBitmap(result)

    def get_selected_thumbs(self):
        selection = [self.thumbnailGrid.GetFirstSelected()]
        while len(selection) < self.thumbnailGrid.SelectedItemCount:
            selection.append(self.thumbnailGrid.GetNextSelected(selection[-1]))
        return [self.thumbnailGrid.GetItem(i) for i in selection] 
