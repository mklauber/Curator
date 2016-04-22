# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class PhotoOrganizerFrame
###########################################################################

class PhotoOrganizerFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1178,866 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.FileMenu = wx.Menu()
		self.AddFileButton = wx.MenuItem( self.FileMenu, wx.ID_ANY, u"Add File"+ u"\t" + u"ctrl-A", wx.EmptyString, wx.ITEM_NORMAL )
		self.FileMenu.Append( self.AddFileButton )
		
		self.AddFolderButton = wx.MenuItem( self.FileMenu, wx.ID_ANY, u"Add Folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.FileMenu.Append( self.AddFolderButton )
		
		self.FileMenu.AppendSeparator()
		
		self.ExitButton = wx.MenuItem( self.FileMenu, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.FileMenu.Append( self.ExitButton )
		
		self.m_menubar1.Append( self.FileMenu, u"File" ) 
		
		self.HelpMenu = wx.Menu()
		self.DebugMenuItem = wx.MenuItem( self.HelpMenu, wx.ID_ANY, u"Debug", wx.EmptyString, wx.ITEM_NORMAL )
		self.HelpMenu.Append( self.DebugMenuItem )
		
		self.m_menubar1.Append( self.HelpMenu, u"Help" ) 
				
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
		self.FilterBox = wx.ComboBox( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, FilterBoxChoices, wx.TE_PROCESS_ENTER )
		bSizer15.Add( self.FilterBox, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.FilterButton = wx.Button( self.m_panel5, wx.ID_ANY, u"Filter", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.FilterButton, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		self.thumbPreviewSplitter = wx.SplitterWindow( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.thumbPreviewSplitter.Bind( wx.EVT_IDLE, self.thumbPreviewSplitterOnIdle )
		
		self.ThumbnailScroller = wx.ScrolledWindow( self.thumbPreviewSplitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.ThumbnailScroller.SetScrollRate( 5, 5 )
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.thumbnailGrid = wx.ListCtrl( self.ThumbnailScroller, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_EDIT_LABELS|wx.LC_ICON|wx.LC_NO_HEADER)
		bSizer21.Add( self.thumbnailGrid, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.ThumbnailScroller.SetSizer( bSizer21 )
		self.ThumbnailScroller.Layout()
		bSizer21.Fit( self.ThumbnailScroller )
		self.PreviewPanel = wx.Panel( self.thumbPreviewSplitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Preview = wx.StaticBitmap( self.PreviewPanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.Preview, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		self.PreviewPanel.SetSizer( bSizer9 )
		self.PreviewPanel.Layout()
		bSizer9.Fit( self.PreviewPanel )
		self.thumbPreviewSplitter.SplitVertically( self.ThumbnailScroller, self.PreviewPanel, 546 )
		bSizer6.Add( self.thumbPreviewSplitter, 1, wx.EXPAND, 5 )
		
		
		self.m_panel5.SetSizer( bSizer6 )
		self.m_panel5.Layout()
		bSizer6.Fit( self.m_panel5 )
		self.m_splitter8.SplitVertically( self.m_panel6, self.m_panel5, 202 )
		bSizer2.Add( self.m_splitter8, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		self.m_statusBar3 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.AddFileButtonOnMenuSelection, id = self.AddFileButton.GetId() )
		self.Bind( wx.EVT_MENU, self.AddFolderButtonOnMenuSelection, id = self.AddFolderButton.GetId() )
		self.Bind( wx.EVT_MENU, self.ExitButtonOnMenuSelection, id = self.ExitButton.GetId() )
		self.Bind( wx.EVT_MENU, self.DebugMenuItemOnMenuSelection, id = self.DebugMenuItem.GetId() )
		self.FilterBox.Bind( wx.EVT_TEXT_ENTER, self.FilterBoxOnTextEnter )
		self.TagTree.Bind( wx.EVT_TREE_SEL_CHANGED, self.TagTreeOnTreeSelChanged )
		self.FilterButton.Bind( wx.EVT_BUTTON, self.FilterButtonOnButtonClick )
		self.thumbnailGrid.Bind( wx.EVT_LIST_ITEM_SELECTED, self.thumbnailGridOnListItemSelected )
		self.thumbnailGrid.Bind( wx.EVT_LIST_KEY_DOWN, self.thumbnailGridOnListKeyDown )
		self.PreviewPanel.Bind( wx.EVT_SIZE, self.PreviewPanelOnSize )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class

	def AddFileButtonOnMenuSelection( self, event ):
		pass
	
	def AddFolderButtonOnMenuSelection( self, event ):
		pass
	
	def ExitButtonOnMenuSelection( self, event ):
		pass
	
	def DebugMenuItemOnMenuSelection( self, event ):
		pass
	
	def TagTreeOnTreeSelChanged( self, event ):
		pass
	
	def FilterBoxOnTextEnter( self, event ):
		pass
	
	def FilterButtonOnButtonClick( self, event ):
		pass
	
	def thumbPreviewSplitterOnSplitterSashPosChanged( self, event ):
		pass
	
	
	def thumbnailGridOnListItemSelected(self, event):
		pass
	
	def thumbnailGridOnListKeyDown(self, event):
		pass
	
	def PreviewPanelOnSize( self, event ):
		pass
	
	def m_splitter8OnIdle( self, event ):
		self.m_splitter8.SetSashPosition( 202 )
		self.m_splitter8.Unbind( wx.EVT_IDLE )
	
	def m_splitter10OnIdle( self, event ):
		self.m_splitter10.SetSashPosition( 467 )
		self.m_splitter10.Unbind( wx.EVT_IDLE )
	
	def thumbPreviewSplitterOnIdle( self, event ):
		self.thumbPreviewSplitter.SetSashPosition( 546 )
		self.thumbPreviewSplitter.Unbind( wx.EVT_IDLE )
	

