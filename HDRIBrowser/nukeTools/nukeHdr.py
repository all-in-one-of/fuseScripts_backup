import nuke as nuke
import os

def fileInfo():
	fileName		= nuke.root().knob('name').value()
	print fileName
	if fileName == "":
		raise ValueError, 'Please save your file '
	else:
		fileName		=		fileName.split('/')
		fileName		=		"/".join(fileName[0:4])
		hdrPath		=		fileName + "/assets/hdri"
		print hdrPath
		if not os.path.exists(hdrPath):
			os.makedirs(hdrPath)
		return hdrPath
def createRead(path):
	nuke.nodes.Read(file = path)