fn herp =
	(
	
				st = @"
from PySide import QtCore, QtGui, QtUiTools
from PySide.QtCore import *
from PySide.QtGui import *
import MaxPlus
sys.path.append('S:/outfit/shared/pythonPipeline')
import HDRIBrowser.fuseHdrBrowser_001 as HDRIBrowser
reload(HDRIBrowser)
		
	
app = QtGui.QApplication.instance()
if not app:
	app = QtGui.QApplication([])
	
	
ui = HDRIBrowser.PlayblastTool()
#ui.setWindowTitle('%s'%(filename))
ui.show()


"
	
python.execute st

)
herp()


