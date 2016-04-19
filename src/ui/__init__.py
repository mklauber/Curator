import wx
import peewee
from ui.generated import PhotoOrganizerFrame
from ui.thumbnail import ThumbnailPanel
from ui.helpers import scale_bitmap

from hashlib import md5


from models import File

class ThumbnailPanel( ThumbnailPanel ):
    def __init__(self, parent, mainWindow, md5):
        super(type(self), self).__init__(parent)
        self.mainWindow = mainWindow
        
        file = File.get(md5=md5)
        self.preview = wx.Bitmap()
        self.preview.LoadFile(file.path)
        self.update_preview()

                
    def clicked(self, event):
        self.mainWindow.preview = self.preview

    def update_preview(self):
        bitmap = scale_bitmap(self.preview, *self.thumbnail.GetSize())
        self.thumbnail.SetBitmap(bitmap)

        

class PhotoOrganizerWindow( PhotoOrganizerFrame ):
    def __init__(self, parent):
        super(type(self),self).__init__(parent)
        self._preview = None
        self.thumbnails = [ThumbnailPanel(self.ThumbnailScroller, self, f.md5) for f in File.select()]
        self.layout_thumbnails()
        
        
        
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
        self.preview = wx.Bitmap(selectDialog.GetPaths()[0])
        
        
        redraw = False
        for path in selectDialog.GetPaths():
            with open(path, 'r') as f:
                m = md5()
                m.update(f.read())
            try:
                File(md5=m.hexdigest(), path=path).save()
                redraw=True
            except peewee.IntegrityError:
                pass
        if redraw == True:
            self.layout_thumbnails()
    
    def ExitButtonOnMenuSelection( self, event ):
        self.Close()

    def PreviewOnSize( self, event ):
        self.layout_thumbnails()
        self.update_preview()

    def layout_thumbnails(self):
        num_cols = self.ThumbnailScroller.Size[0] / 200
        self.thumbnailSizer.Cols = num_cols
        self.thumbnailSizer.Clear()
        for thumb in self.thumbnails:
            self.thumbnailSizer.Add( thumb, 1, wx.EXPAND |wx.ALL, 5 )

    def update_preview(self):
        bitmap = scale_bitmap(self._preview, *self.m_panel8.GetSize(), quality=wx.IMAGE_QUALITY_HIGH)
        self.Preview.SetBitmap(bitmap)
        

