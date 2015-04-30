# -- Process Hdr tool 
# -- written Michael Kirylo
# -- 2014
#===============================================================================
# # imports
#===============================================================================
import os
import re
import shutil
import getpass
import time
from fnmatch import fnmatch

#===============================================================================
# # main class
#===============================================================================
class findHdr(object):
	def __init__(self,imgPath):
		self.hdrList 		=		 []
		self.hdrExistList 	=		 []
		self.hdrPath 		= 		imgPath
		self.pattern		=		"*.hdr"
		self.hdrLibpath		=		"C:\TEMP\hdrLib\\"
#===============================================================================
# # find hdr images 
#===============================================================================
		for path, subdirs, files in os.walk(self.hdrPath):
		    for name in files:
		        if fnmatch(name, self.pattern):
		            fullpath = os.path.join(path, name)
		            self.hdrList.append(fullpath)
#===============================================================================
# # class functions
#===============================================================================
   	def processHdr(self,entry,batfile):
   		bat				=		[]
   		nukeCmd			=		'C:\Progra~1\Nuke9.0v4\Nuke9.0.exe -x  C:\TEMP\hdrTest\\nukeProcessHdr.py %s.hdr %s.png 1,1'%(entry,entry)
   		bat.append (nukeCmd)
   		batFile			=		open(batfile, 'w')
   		for entry in bat:
			batFile.write(entry + '\n')
		batFile.close()
		cmd					=		batfile
		os.system( cmd )
	def copyfiles(self,hPath,newPAth):
		shutil.copy2(hPath, newPAth)

#===============================================================================
# # execute
#===============================================================================
if __name__ == "__main__":
	hdrFiles = findHdr("C:\TEMP\hdrTest")
	for entry in hdrFiles.hdrList:
		os.rename(entry, entry.replace(" ", "_"))
		entry = entry.replace(" ", "_")
		hdrName 	= entry.split(".")
		Hname 		= hdrName[0].replace('\\',"/")
		hdrFiles.processHdr(Hname,'S:\outfit\shared\pythonPipeline\HDRIBrowser\process.bat')
		HdrFileName = Hname.split("/")
		HdrFileName = HdrFileName[-1]
		newPreview 	= entry.replace(".hdr",".png")
		Lib 		= hdrFiles.hdrLibpath+HdrFileName+".hdr"
		LibPreview	= hdrFiles.hdrLibpath+HdrFileName+".png"
		print LibPreview
		if not os.path.exists(Lib):
			hdrFiles.copyfiles(entry,Lib)
		else:
			print "file already in library"
		if not os.path.exists(LibPreview):
			hdrFiles.copyfiles(newPreview,LibPreview)
		else:
			print "file already in library"
		