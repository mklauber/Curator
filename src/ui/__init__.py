import wx
from ui.generated import PhotoOrganizerFrame
from ui.thumbnail import ThumbnailPanel
from ui.helpers import scale_bitmap

from hashlib import md5


from models import File

class ThumbnailPanel( ThumbnailPanel ):
    def __init__(self, parent, md5):
        super(type(self), self).__init__(parent)
        self.parent = parent
        
        file = File.get(md5=md5)
        self.preview = wx.Bitmap.LoadFile(file.path)

                
    def ThmbnailPanelOnLeftDown(self, event):
        self.parent.preview = self.preview
        
    @property
    def preview(self):
        return self._preview
    
    @preview.setter
    def preview(self, value):
        self._preview = value
        self.update_preview()

    def update_preview(self):
        bitmap = scale_bitmap(self.preview, *self.thumbnail.GetSize())
        self.thumbnail.SetBitmap(bitmap)

        

class PhotoOrganizerWindow( PhotoOrganizerFrame ):
    def __init__(self, parent):
        super(type(self),self).__init__(parent)
        self.current_selection = None
        self.thumbnails = [ThumbnailPanel(self, f.md5) for f in File.select()]
        
        
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
        for path in selectDialog.GetPaths():
            with open(path, 'r') as f:
                m = md5()
                m.update(f.read())
            File(md5=m.hexdigest(), path=path).save()
            
    
    def ExitButtonOnMenuSelection( self, event ):
        self.Close()

    def PreviewOnSize( self, event ):
        self.update_preview()

    def update_preview(self):
        bitmap = scale_bitmap(self.preview, *self.Preview.GetSize())
        self.Preview.SetBitmap(bitmap)
        

