# -- Hdr browser maya commands
# -- written by Michael Kirylo
# -- 2014
# ----------------imports-----------------
import maya.cmds as cmds
import maya.mel as mel
import os
# ----------------functions-----------------
def checkRenderer():
	renderer =	mel.eval('currentRenderer')
	return renderer
def mayaWarning():
	cmds.warning( "Please set the current renderer to Vray." )
def fileInfo():
	fileName		= cmds.file ( q = True, sceneName = True)
	if fileName == "":
		cmds.warning("save your file")
	else:
		fileName		=		fileName.split('/')
		fileName		=		"/".join(fileName[0:4])
		hdrPath		=		fileName + "/assets/hdri"
		if not os.path.exists(hdrPath):
			os.makedirs(hdrPath)
		return hdrPath

def createDomeMaya(imagePath):
	checkLight			=	cmds.ls(sl=True)
	if checkLight:
		checkLightShape		=	cmds.listRelatives( checkLight, s=True )
		Ltype = cmds.objectType( checkLightShape)
		test			=	Ltype
	else:
		test = "not vray"
	if test == "VRayLightDomeShape":
		HDRLight 		=	checkLight
	else:
		HDRLight			=	cmds.shadingNode('VRayLightDomeShape', asLight=True)
		HDRLight			=	cmds.rename(HDRLight, ('HDRLightDome_'))
	HDRLightShape		=	cmds.listRelatives( HDRLight, s=True )
	hdrFileNode			=	cmds.shadingNode('file', asTexture=True)
	hdrFileNode			=	cmds.rename(hdrFileNode, ('HDRLightDomeHDR_'))
	vrayPlacementText	=	cmds.shadingNode('VRayPlaceEnvTex', asUtility=True)
	vrayPlacementText	=	cmds.rename(vrayPlacementText, ('HDRLightDomeVrEnvTex_'))
	cmds.connectAttr( (vrayPlacementText + '.outUV'), (hdrFileNode + '.uvCoord'), force=True)
	cmds.connectAttr( (hdrFileNode + '.outColor'), (HDRLightShape[0] + '.domeTex'), force=True)
	cmds.setAttr ((HDRLightShape[0] + '.domeSpherical') , 1 )
	cmds.setAttr ((HDRLightShape[0] + '.useDomeTex') , 1 )
	cmds.setAttr((hdrFileNode + '.filterType'), 0 )
	cmds.setAttr( (hdrFileNode + '.fileTextureName'), imagePath , type = 'string')
	cmds.setAttr (vrayPlacementText+ '.mappingType', 2)
	return HDRLight
