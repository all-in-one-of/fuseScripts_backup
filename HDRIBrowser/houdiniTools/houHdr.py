import hou
import os

def creatHdr(path):
	g = hou.node('/obj').createNode('envlight')
	g.setParms({"env_map": path})
def getFileInfo():
	fileInfo 	=	hou.hipFile.path()
	if fileInfo == "U://untitled.hip":
		print "save your file"
		hdrPath		=		"none"
	else:
		fileInfo 	=	fileInfo.split("/")
		fileInfo		=		"/".join(fileInfo[0:4])
		hdrPath		=		fileInfo + "/assets/hdri"
		print hdrPath
		if not os.path.exists(hdrPath):
			os.makedirs(hdrPath)
	return hdrPath