from peewee import *
from os import path
import hashlib

import wx
from StringIO import StringIO

import logging
logger = logging.getLogger(__name__)

database = SqliteDatabase("metadata.db")

class BaseModel(Model):
    class Meta:
        database = database

class File(BaseModel):
    md5 = CharField(unique=True, index=True)
    path = CharField()
    thumbnail = BlobField()
    
    def as_bitmap(self):
        img = wx.Image()
        img.LoadFile(StringIO(self.thumbnail))
        return img.ConvertToBitmap()
    
    @classmethod
    def create_from_file(cls, path):
        """Handles all the logic about creating a File record from a file on the filesystem."""
        logger.debug("Parsing file at %s", path)
        f = cls()
        f.path = path
        
        # Calculate the md5
        with open(path, 'r') as img:
            m = hashlib.md5()
            m.update(img.read())
        f.md5 = m.hexdigest()
        
        # Create the thumbnail
        thumb = wx.Image()
        thumb.LoadFile(path)
        if thumb.IsOk() == False:
            return None
        s = StringIO()
        thumb.Scale(144,144, wx.IMAGE_QUALITY_NORMAL).SaveFile(s, 'image/png')
        s.seek(0)
        f.thumbnail = s.read()
        
        # Returns a new File instance if one was created, otherwise None
        try:
            f.save()
            return f
        except IntegrityError:
            print "Unable to import %s" % path
            return None
        
    


class Metadata(BaseModel):
    file = ForeignKeyField(File)
    field = CharField(index=True)
    value = CharField(index=True) 
    
    class Meta:
        database = database
        indexes = (
            (('file', 'field', 'value'), True),
        )


def create_database():
    database.connect()
    database.create_tables([File, Metadata])

if path.exists("metadata.db") == False:
    create_database()