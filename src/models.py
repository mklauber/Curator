from peewee import *

database = SqliteDatabase("metadata.db")

class BaseModel(Model):
    class Meta:
        database = database

class File(BaseModel):
    md5 = CharField(unique=True, index=True)
    path = CharField()
    

class Metadata(BaseModel):
    file = ForeignKeyField(File)
    category = CharField(index=True)
    value = CharField(index=True) 
    
    class Meta:
        database = database
        indexes = (
            (('file', 'category', 'value'), True),
        )
    


    