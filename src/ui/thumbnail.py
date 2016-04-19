# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class ThmubnailPanel
###########################################################################

class ThumbnailPanel ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 200,200 ), style = wx.TAB_TRAVERSAL )
        
        bSizer19 = wx.BoxSizer( wx.VERTICAL )
        
        self.thumbnail = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer19.Add( self.thumbnail, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.caption = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.caption.Wrap( -1 )
        bSizer19.Add( self.caption, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer19 )
        self.Layout()
        
        # Connect Events
        self.Bind( wx.EVT_LEFT_DOWN, self.ThmubnailPanelOnLeftDown )
        self.Bind( wx.EVT_SIZE, self.ThmubnailPanelOnSize )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def ThmubnailPanelOnLeftDown( self, event ):
        pass
    
    def ThmubnailPanelOnSize( self, event ):
        pass
    

