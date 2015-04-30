import MaxPlus
import os
def createDomeLight(path): 
	string = 'domeLight = VRayLight()\n\
	domeLight.type = 1\n\
	domeLight.invisible = on\n\
	domeLight.texmap_on = on\n\
	domeLight.multiplier = 1\n\
	domeLight.dome_spherical = on\n\
	hdrMap = VRayHDRI()\n\
	hdrMap.maptype = 2\n\
	domeLight.texmap = hdrMap\n\
	hdrMap.HDRIMapName =%s'%'"'+path+'"'
	MaxPlus.Core.EvalMAXScript(string)

def getFileInfo():
	fm = MaxPlus.FileManager
	fileName		=		fm.GetFileNameAndPath()
	promptDiag ='messagebox "Save your scene file"'
	if fileName == "":
		MaxPlus.Core.EvalMAXScript(promptDiag)
	else:
		fileName		=		fileName.split('\\')
		print fileName
		fileName		=		"/".join(fileName[0:4])
		hdrPath		=		fileName + "/assets/hdri"
		if not os.path.exists(hdrPath):
			os.makedirs(hdrPath)
	return hdrPath

# def getselectednodenames():
# 	name = MaxPlus.SelectionManager.GetNode(0)
# 	return name