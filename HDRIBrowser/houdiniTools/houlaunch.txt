import sys
import hou
from PySide import QtGui
try:

    sys.path.remove('S:/outfit/shared/pythonPipeline/CGPythonPipelineToolsMySQL/src/root/floatingMainInterface')
except:
    pass
   
sys.path.append('S:/outfit/shared/pythonPipeline/CGPythonPipelineToolsMySQL/src/root/floatingMainInterface')

try:
    sys.path.remove("S:/outfit/shared/hou/13/")
except:
    sys.path.append("S:/outfit/shared/hou/13/")   
import HDRIBrowser.fuseHdrBrowser_001 as HDRIBrowser
reload(HDRIBrowser)
#for iii in sys.path:print iii
from PyHoudini import pyqt_houdini
from mainMySQL import *

for widget in QtGui.QApplication.allWidgets():
    
    if str(widget.__str__()).__contains__("Hdr Browser"):
        print widget.close()


def openApp():

            
    def myExitHandler():
        table.dialog.settings.setValue('size', table.dialog.size())
        table.dialog.settings.setValue('pos', table.dialog.pos())
     
    app = QApplication.instance()
    #print "app",app
    if app == None: 
        app = QtGui.QApplication(['houdini'])
    ui = HDRIBrowser.PlayblastTool()
    ui.show()
    ui.setObjectName = 'mk.hdrBrowser'
    ui.raise_() 


    pyqt_houdini.exec_(app, ui)
openApp()