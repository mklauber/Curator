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
## Class MyFrame1
###########################################################################

class PhotoOrganizerFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1178,866 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.FileMenu = wx.Menu()
		self.AddFileButton = wx.MenuItem( self.FileMenu, wx.ID_ANY, u"Add File"+ u"\t" + u"ctrl-A", wx.EmptyString, wx.ITEM_NORMAL )
		self.FileMenu.AppendItem( self.AddFileButton )
		
		self.AddFolderButton = wx.MenuItem( self.FileMenu, wx.ID_ANY, u"Add Folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.FileMenu.AppendItem( self.AddFolderButton )
		
		self.FileMenu.AppendSeparator()
		
		self.ExitButton = wx.MenuItem( self.FileMenu, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.FileMenu.AppendItem( self.ExitButton )
		
		self.m_menubar1.Append( self.FileMenu, u"File" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter8 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter8.Bind( wx.EVT_IDLE, self.m_splitter8OnIdle )
		
		self.m_panel6 = wx.Panel( self.m_splitter8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter10 = wx.SplitterWindow( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter10.Bind( wx.EVT_IDLE, self.m_splitter10OnIdle )
		
		self.m_panel9 = wx.Panel( self.m_splitter10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.TagTree = wx.TreeCtrl( self.m_panel9, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		bSizer16.Add( self.TagTree, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel9.SetSizer( bSizer16 )
		self.m_panel9.Layout()
		bSizer16.Fit( self.m_panel9 )
		self.m_panel11 = wx.Panel( self.m_splitter10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.DetailsLabel = wx.StaticText( self.m_panel11, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0|wx.RAISED_BORDER )
		self.DetailsLabel.Wrap( -1 )
		bSizer18.Add( self.DetailsLabel, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel11.SetSizer( bSizer18 )
		self.m_panel11.Layout()
		bSizer18.Fit( self.m_panel11 )
		self.m_splitter10.SplitHorizontally( self.m_panel9, self.m_panel11, 467 )
		bSizer7.Add( self.m_splitter10, 1, wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer7 )
		self.m_panel6.Layout()
		bSizer7.Fit( self.m_panel6 )
		self.m_panel5 = wx.Panel( self.m_splitter8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		FilterBoxChoices = []
		self.FilterBox = wx.ComboBox( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, FilterBoxChoices, 0 )
		bSizer15.Add( self.FilterBox, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.FilterButton = wx.Button( self.m_panel5, wx.ID_ANY, u"Filter", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.FilterButton, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		self.thumbPreviewSplitter = wx.SplitterWindow( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.thumbPreviewSplitter.Bind( wx.EVT_IDLE, self.m_splitter9OnIdle )
		
		self.m_panel7 = wx.Panel( self.thumbPreviewSplitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ThumnailsSizer = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panel7.SetSizer( ThumnailsSizer )
		self.m_panel7.Layout()
		ThumnailsSizer.Fit( self.m_panel7 )
		self.m_panel8 = wx.Panel( self.thumbPreviewSplitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Preview = wx.StaticBitmap( self.m_panel8, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.Preview, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		self.m_panel8.SetSizer( bSizer9 )
		self.m_panel8.Layout()
		bSizer9.Fit( self.m_panel8 )
		self.thumbPreviewSplitter.SplitVertically( self.m_panel7, self.m_panel8, 546 )
		bSizer6.Add( self.thumbPreviewSplitter, 1, wx.EXPAND, 5 )
		
		
		self.m_panel5.SetSizer( bSizer6 )
		self.m_panel5.Layout()
		bSizer6.Fit( self.m_panel5 )
		self.m_splitter8.SplitVertically( self.m_panel6, self.m_panel5, 202 )
		bSizer2.Add( self.m_splitter8, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.AddFileButtonOnMenuSelection, id = self.AddFileButton.GetId() )
		self.Bind( wx.EVT_MENU, self.AddFolderButtonOnMenuSelection, id = self.AddFolderButton.GetId() )
		self.Bind( wx.EVT_MENU, self.ExitButtonOnMenuSelection, id = self.ExitButton.GetId() )
		self.TagTree.Bind( wx.EVT_TREE_SEL_CHANGED, self.TagTreeOnTreeSelChanged )
		self.FilterButton.Bind( wx.EVT_BUTTON, self.FilterButtonOnButtonClick )
		self.Preview.Bind( wx.EVT_SIZE, self.PreviewOnSize )
	
	def __del__( self ):
		pass
	
	
	
	def AddFileButtonOnMenuSelection( self, event ):
		pass
	
	def AddFolderButtonOnMenuSelection( self, event ):
		pass
	
	def ExitButtonOnMenuSelection( self, event ):
		pass
	
	def TagTreeOnTreeSelChanged( self, event ):
		pass
	
	def FilterButtonOnButtonClick( self, event ):
		pass

	def PreviewOnSize(self, event):
		pass
		
	def m_splitter8OnIdle( self, event ):
		self.m_splitter8.SetSashPosition( 202 )
		self.m_splitter8.Unbind( wx.EVT_IDLE )
	
	def m_splitter10OnIdle( self, event ):
		self.m_splitter10.SetSashPosition( 467 )
		self.m_splitter10.Unbind( wx.EVT_IDLE )
	
	def m_splitter9OnIdle( self, event ):
		self.thumbPreviewSplitter.SetSashPosition( 546 )
		self.thumbPreviewSplitter.Unbind( wx.EVT_IDLE )
		self.thumbPreviewSplitter.SetSashGravity(1)
	

