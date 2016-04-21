from __future__ import division

import wx
import peewee
from StringIO import StringIO
from ui.generated import PhotoOrganizerFrame
from ui.helpers import scale_bitmap


from models import File, Metadata

import logging
logger = logging.getLogger(__name__)


class PhotoOrganizerWindow( PhotoOrganizerFrame ):
    def __init__(self, parent):
        super(type(self),self).__init__(parent)
        self._preview = None

        # Only update the preview when we stop changing the list selection
        self.list_change_timer = wx.Timer(self)
        
        # Load the Grid
        self.thumbnail_index = {}
        self.thumbnails = wx.ImageList()
        self.thumbnailGrid.SetImageList(self.thumbnails, wx.IMAGE_LIST_NORMAL)
        for f in File.select():
            self.thumbnail_index[f.md5] = self.thumbnails.Add(f.as_bitmap())
        self.refresh_thumbnails()
        

    @property
    def preview(self):
        return self._preview

    @preview.setter
    def preview(self, value):
        self._preview = value
        self.update_preview()

    def AddFileButtonOnMenuSelection(self, event):
        selectDialog = wx.FileDialog(self, "Add File(s)", "~/Images", "", style=wx.FD_OPEN|wx.FD_MULTIPLE)
        if selectDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        self.preview = wx.Image(selectDialog.GetPaths()[0])
        
        # Create the new files, and update the thumnail_index with any new files
        new_files = filter(None, (File.create_from_file(path) for path in selectDialog.GetPaths()))
        for f in new_files:
            self.thumbnail_index[f.md5] = self.thumbnails.Add(f.as_bitmap())
        
        # If there are any new files we need to re layout the thumbnailGrid
        if len(new_files) > 0:
            self.refresh_thumbnails()
        
    
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
        
        tags = Metadata.filter(file=File.get(md5=event.GetLabel()))
        tags = ", ".join([t.value for t in tags])
        
        dialog = wx.TextEntryDialog(None, "Tags:", "Modifiy Tags", value=tags)
        if dialog.ShowModal() == wx.ID_OK:
            tags = dialog.GetValue()
            tags = [t.strip() for t in tags.split(",")]
            for tag in tags:
                Metadata(file=file, category="tag", value=tag).save()
        
        
    def thumbnailGridOnListItemSelected(self, event):
        print "Item Selected"
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


    # Helper functions
    def refresh_thumbnails(self):
        
        self.thumbnailGrid.ClearAll()
        for i, f in enumerate(File.select()):
            item = wx.ListItem()
            # Set image
            item.SetImage(self.thumbnail_index[f.md5])
            item.SetId(i)
            item.SetText(f.md5)
            
            self.thumbnailGrid.InsertItem(item)

    def update_preview(self):
        logger.debug("Running update_preview")
        if self.preview == None:
            return
        width, height = self.PreviewPanel.GetSize()
        hRatio = height / self.preview.Height
        wRatio = width / self.preview.Width 
        ratio = min(hRatio, wRatio)
        image = self.preview.Scale(self.preview.Width * ratio, self.preview.Height * ratio, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        
        
        self.Preview.SetBitmap(result)
        

