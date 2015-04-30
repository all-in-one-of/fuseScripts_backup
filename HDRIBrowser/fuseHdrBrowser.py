# -- Fuse Hdr Browser Tool 
# -- written by Andy Lewis and Michael Kirylo
# -- 2014
#===============================================================================
# # imports
#===============================================================================
import os
import re
import shutil
import getpass
import time
from PySide import QtCore, QtGui, QtUiTools
from PySide.QtCore import *
from PySide.QtGui import *
#===============================================================================
# # global variables
#===============================================================================
def findApp():
    try:
        import MaxPlus
        app         =               "max"
    except:
        pass
    try:
        import maya.cmds as cmds
        app         =               "maya"
    except :
        pass
    try:
        import nuke
        app         =               "nuke"
    except:
        pass
    try:
        import hou
        app         =               'houdini'
    except:
        pass
    # finally:
    return app
app             =   findApp()
THUMBNAIL_SIZE  =   160
ThumbNailW      =   128
ThumbNailH      =   256
SPACING         =    0
if app == "nuke":
    IMAGES_PER_ROW  =   2
else:
    IMAGES_PER_ROW  =   3
qtFilePath      =    "S:/outfit/shared/pythonPipeline/HDRIBrowser/alHDRBrowserUI_002.ui"
# Log user
user = getpass.getuser()
CDate = time.strftime("%m/%d/%Y")
Ctime= time.strftime("%H:%M:%S")
f = open('S:/outfit/shared/pythonPipeline/HDRIBrowser/log/users.txt','a')
f.write(user+' '+CDate+' '+Ctime+'\n') # python will convert \n to os.linesep
f.close() # you can omit in most cases as the destructor will call if
#===============================================================================
# # main class
#===============================================================================
class PlayblastTool(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.checkInstances()
#===============================================================================
# # UI FILE LOAD
#===============================================================================
        self.loader         =           QtUiTools.QUiLoader()
        uifile              =           QFile(qtFilePath)
        uifile.open(QFile.ReadOnly)
        self.ui             =           self.loader.load(uifile)
        uifile.close()
        self.layout         =           QGridLayout()
        self.layout.addWidget(self.ui)
        self.setLayout(self.layout)
#===============================================================================
# #  UI adjustments per app 
#===============================================================================
        if app == "nuke":
            self.ui.setMinimumSize(256, 100)
        else:
            self.ui.setMinimumSize(785, 512)
        if app == "max":
            self.ui.searchBox.setReadOnly(True)
            self.ui.searchButton.setEnabled(1)
            
            
        else:
            self.ui.searchBox.setEnabled(1)
            self.ui.searchButton.setDisabled(1)
#===============================================================================
# # INITIAL SETUP
#===============================================================================
        self.ui.images_tableWidget.setIconSize(QSize(ThumbNailH,ThumbNailW))
        self.ui.images_tableWidget.setColumnCount(IMAGES_PER_ROW)
        self.ui.images_tableWidget.setGridStyle(Qt.NoPen)
        self.ui.images_tableWidget.verticalHeader().setDefaultSectionSize(ThumbNailW)
        self.ui.images_tableWidget.verticalHeader().hide()
        self.ui.images_tableWidget.horizontalHeader().setDefaultSectionSize(ThumbNailH)
        self.ui.images_tableWidget.horizontalHeader().hide()
        self.ui.images_tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.getPictureList()
#===============================================================================
# # CONNECTIONS
#===============================================================================
        self.ui.create_btn.clicked.connect(self.loadHdr)
        self.ui.copy_pathBtn.clicked.connect(self.copyClipboard)
        self.ui.images_tableWidget.doubleClicked.connect(self.loadHdr)
        self.ui.images_tableWidget.currentItemChanged.connect(self.updateSelection)
        if app == "max":
            self.ui.searchButton.clicked.connect( self.maxSearch )
            self.ui.searchBox.textChanged.connect( self.getPictureList )
        else:
            self.ui.searchBox.editingFinished.connect( self.getPictureList )
#===============================================================================
# # set parent window
#===============================================================================
        if app == "maya":
            from maya import OpenMayaUI as omui 
            from shiboken import wrapInstance 
            mayaMainWindowPtr = omui.MQtUtil.mainWindow()
            mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget) 
            self.setParent(mayaMainWindow)
            self.setWindowFlags(Qt.Window) 
        if app == "nuke":
            import nuke
            from nukescripts import panels
            panels.registerWidgetAsPanel( 'HDRIBrowser.PlayblastTool', 'Fuse Hdr Browser ','uk.co.thefoundry.hdrBrowser',True)
# #===============================================================================
# # functions
#===============================================================================
    def updateSelection(self):
        hdrPath     =       self.getHdrPath()
        hdrName     =       self.assetHdrName(hdrPath)
        self.ui.hdrName.setText(hdrName)
    def addPictures(self, row, col, picturePath):
        item             =              QTableWidgetItem()
        qimage = QImage(picturePath)
        if qimage.isNull():
            print "cannot open image"
        else:
            p           =               QPixmap.fromImage(qimage)
            if p.height()>p.width(): 
                p       =               p.scaledToWidth(ThumbNailH)
            else: 
                p       =               p.scaledToHeight(ThumbNailW)
            p           =               p.copy(0,0,ThumbNailH,ThumbNailW)
            item.setIcon(QIcon(p))
            item.text   =               str(picturePath)
            self.ui.images_tableWidget.setItem(row,col,item)
    def getPictureList(self):
        picturesPath    =               'S:/3D_Resources/Maps/HDRI/dome'
        pictureDir      =               QDir('S:/3D_Resources/Maps/HDRI/dome')
        pictures        =               pictureDir.entryList(['*.png'])
        searchText      =               self.ui.searchBox.text()
        if searchText == "":
            pass
        else:
            search = []
            pics    =   [element.lower() for element in pictures]
            for i, d in enumerate(pics):
                if searchText.lower() in d:
                    search.append(d)
            pictures = search
        rowCount        =               len(pictures)//IMAGES_PER_ROW
        if len(pictures)%IMAGES_PER_ROW: rowCount+=1
        self.ui.images_tableWidget.setRowCount(rowCount)
        row=-1
        for i,picture in enumerate(pictures):
            col         =                i%IMAGES_PER_ROW
            if not col: row+=1
            self.addPictures(row, col, picturesPath+"/"+picture)  
    def getHdrPath(self):
        item = self.ui.images_tableWidget.currentItem()
        imgPath = item.text
        hdrPath= imgPath.replace(".png",".hdr")
        return hdrPath
    def sendToCip(self):
            hdrPath= self.getHdrPath()
            # hdrName     =    self.assetHdrName(hdrPath)
            # newPAth     =    path+"/"+hdrName
            command = 'echo ' + hdrPath.strip() + '| clip'
            os.system(command)
            # if app == "nuke":
            #     command = 'echo ' + hdrPath.strip() + '| clip'
            #     os.system(command)
            # else:
            #     if not os.path.exists(newPAth):
            #         shutil.copy2(hdrPath, newPAth)
            #     else:
            #         print "file already exists"
            #     command = 'echo ' + newPAth.strip() + '| clip'
            #     os.system(command)
    def copyClipboard(self):
        self.sendToCip()
        # if app == "max":
            # import HDRIBrowser.maxTools.maxHdrCmds as maxHdrCmds
            # reload(maxHdrCmds)
            # fileInfo    =    maxHdrCmds.getFileInfo()
        #     self.sendToCip()
        # if app == "maya":
            # import HDRIBrowser.mayaTools.MayaHdr as MayaHdr
            # reload(MayaHdr)
            # mayaFileInfo    =   MayaHdr.fileInfo()
        #     self.sendToCip()
        # if app == "nuke":
            # import HDRIBrowser.nukeTools.nukeHdr as nukeHdr
            # reload(nukeHdr)
            # nukeFileInfo    =   nukeHdr.fileInfo()
            # self.sendToCip()
    def copyToProject(self,path):
        hdrPath= self.getHdrPath()
        hdrName     =    self.assetHdrName(hdrPath)
        newPAth     =    path+"/"+hdrName
            shutil.copy2(hdrPath, newPAth)
        else:
            print "file already exists"
        return newPAth
    def assetHdrName(self,path):
        path    =   path.split("/")
        imageName   =   path[-1]
        return imageName
    def loadHdr(self):
        if app == "max":
            import HDRIBrowser.maxTools.maxHdrCmds as maxHdrCmds
            reload(maxHdrCmds)
            fileInfo    =    maxHdrCmds.getFileInfo()
            imagePath     =   self.copyToProject(fileInfo)
            maxHdrCmds.createDomeLight(imagePath)
        if app =="maya":
            import HDRIBrowser.mayaTools.MayaHdr as MayaHdr
            reload(MayaHdr)
            currRenderer = MayaHdr.checkRenderer()
            if (currRenderer == "vray"):
                mayaFileInfo    =   MayaHdr.fileInfo()
                imagePath     =   self.copyToProject(mayaFileInfo)
                MayaHdr.createDomeMaya(imagePath)
            else:
                MayaHdr.mayaWarning()
        if app == "nuke":
            import HDRIBrowser.nukeTools.nukeHdr as nukeHdr
            reload(nukeHdr)
            hdrPath= self.getHdrPath()
            nukeHdr.createRead(hdrPath)
        if app == "houdini":
            import HDRIBrowser.houdiniTools.houHdr as houHdr
            reload(houHdr)
            fileInfo        =       houHdr.getFileInfo()
            if fileInfo == "none":
                print "save your file"
            else:
                imagePath       =       self.copyToProject(fileInfo)
                houHdr.creatHdr(imagePath)
    def maxSearch(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Search Dialog', 'Enter text:')
        if ok:
            # self.le.setText(str(text))
            self.ui.searchBox.setText(str(text))
#==========================================================================
# ATTEMPTING TO DELETE ANY OTHER INSTANCE OF THE SOFTWARE IN PARENT APP
#==========================================================================
    def checkInstances(self):
        for widget in QApplication.allWidgets():
            if type(widget) == type(self):
                p = widget.parentWidget()
                while p:
                    if p.parent() and isinstance(p.parent(), QStackedWidget):
                        p.parent().removeWidget(p)
                        p = None
                    else:
                        p = p.parentWidget()