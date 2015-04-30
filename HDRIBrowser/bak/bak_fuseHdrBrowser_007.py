# -- Hdr browser
# -- written by Michael Kirylo
# -- 2014
# ----------------imports-----------------
import sys
import os
import shutil
import getpass
import maya.cmds as cmds
from maya import OpenMayaUI as omui
from shiboken import wrapInstance 
from PySide import QtCore, QtGui, QtUiTools
from PySide.QtCore import *
from PySide.QtGui import *
from pprint import pprint
import HDRIBrowser.mayaTools.MayaHdr as MayaHdr

reload(MayaHdr)
# ----------Paths--------------
UI_PATH = 'S:/outfit/shared/pythonPipeline/HDRIBrowser/fuseHdrBrowserUI.ui'
HDR_DOME_PATH = "S:/3D_Resources/Maps/HDRI/dome"
HDR_RECT_PATH = "S:/3D_Resources/Maps/HDRI/rect"
# -------------------------------
mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
mayaMainWindow= wrapInstance(long(mayaMainWindowPtr), QWidget) 
# ------------Load UI ------------
def loadUi(path, parent=None):
	loader = QtUiTools.QUiLoader()
	file = QtCore.QFile(path)
	file.open(QtCore.QFile.ReadOnly)
	widget = loader.load(file, parent)
	file.close()
	return widget
# ---------------class-----------------
class fuseHdr(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		hdrBrowserPath = UI_PATH
		self.ui = loadUi(hdrBrowserPath, self)
		print self.ui
		# Connections to UI
		self.connect(self.ui.imageList,		QtCore.SIGNAL("currentIndexChanged(int)"),	self.UpdatePreviewImage )
		self.connect(self.ui.CreateButton,		QtCore.SIGNAL("clicked()"),					self.CreatefuseDomeLight )
		self.imageList = self.ui.imageList
		self.preview = self.ui.preview
		#General Update
		self.UpdateUI()
	def UpdateUI( self ):
		self.UpdatePreviewImage()
		self.UpdateImageListUI()
	def UpdateImageListUI( self ):
		uiFileList = []
		FileList = self.UpdateImageList()
		for x in FileList:
			uiFileList.append(x['display'])
		self.imageList.addItems( uiFileList )
	def UpdatePreviewImage( self ):
		currentSelection = str(self.imageList.currentText())
		fileInfo = self.UpdateImageList()
		for entry in fileInfo:
			if (entry['display'] == currentSelection):
				previewImage = (entry['path']+ '/' + currentSelection + '.jpg')
				pixmap = QPixmap(previewImage)
				self.preview.setPixmap(pixmap)
	def LightCheck( self , guiButton ):
		fileInfo = self.UpdateImageList()
		for entry in fileInfo:
			if (entry['display'] == guiButton):
				if (entry['type'] == 'dome'):
					lightsInScene = MayaHdr.checkDome()
					version = []
					if (len(lightsInScene) != 0):
						for x in lightsInScene:
							x=x.split("_")
							version.append(int(x[1]))
						newVersion = version[-1] + 1
						newVersion = str(newVersion).zfill ( 3 )
					else:
						newVersion = '001'
				if (entry['type'] == 'rect'):
					lightsInScene = MayaHdr.checkRec()
					version = []
					if (len(lightsInScene) != 0):
						for x in lightsInScene:
							x=x.split("_")
							version.append(int(x[1]))
						newVersion = version[-1] + 1
						newVersion = str(newVersion).zfill ( 3 )
					else:
						newVersion = '001'
		return newVersion
	def CreatefuseDomeLight( self ):
		currRenderer = MayaHdr.checkRenderer()
		if (currRenderer == "vray"):
			guiButton = str(self.imageList.currentText())
			srcHdrFile = self.SrcHDRFile( guiButton )
			imagePath = srcHdrFile
			suffux = self.LightCheck( guiButton )
			createLight = self.CreateDomeLight( suffux , imagePath )
		else:
			MayaHdr.mayaWarning()
	def SrcHDRFile( self, guiButton ):
		fileInfo = self.UpdateImageList()
		for entry in fileInfo:
			if (entry['display'] == guiButton):
				hdrPath = (entry['path'] + '/' + guiButton + '.hdr')
		return hdrPath
	def UpdateImageList( self ):
		hdrPathDome = HDR_DOME_PATH
		hdrPathRect = HDR_RECT_PATH
		libraryFilesDome = os.listdir( hdrPathDome )
		libraryFilesRect = os.listdir( hdrPathRect )
		uiFileList = []
		FileList = []
		
		if (len(libraryFilesDome) != None):
			libraryFilesDome.sort()
			for a in libraryFilesDome:
				ext = a.split (".")
				if (ext[1] == 'hdr'):
					FileList.append({'display':ext[0],'path':hdrPathDome, 'type':'dome'})
		if (len(libraryFilesRect) != None):
			libraryFilesRect.sort()
			for b in libraryFilesRect:
				ext = b.split (".")
				if (ext[1] == 'hdr'):
					FileList.append({'display':ext[0],'path':hdrPathRect, 'type':'rect'})
		return ( FileList )
	def CreateDomeLight( self, suffux , imagePath ):
		currentSelection = str(self.imageList.currentText())
		fileInfo = self.UpdateImageList()
		vrayEnv = self.ui.vrayEnvCheckbox.isChecked()
		for entry in fileInfo:
			if (entry['display'] == currentSelection):
				if (entry['type'] == 'dome'): 
					if (vrayEnv == False):
						print 'use dome'
						MayaHdr.createDomeMaya(suffux, imagePath)	
					if (vrayEnv == True):
						print 'Use Env'
						MayaHdr.createEnvMaya(suffux, imagePath)
				if (entry['type'] == 'rect'):
					MayaHdr.createRectMaya(suffux, imagePath)
def launchUIMaya():
	if (cmds.window('fuseHdrBrowser', exists=True) == True):
		cmds.deleteUI('fuseHdrBrowser')
	app = fuseHdr(parent=mayaMainWindow)

	cmds.showWindow( 'fuseHdrBrowser' )

	return app

if __name__ == '__main__':
    launchUIMaya()

