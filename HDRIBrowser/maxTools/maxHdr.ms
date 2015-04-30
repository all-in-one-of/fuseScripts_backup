(----------------hdr browser written by Michael Kirylo 2014--------------
-------------------------------------------------------------------------
-----------------------------------------------
--  functions 
-----------------------------------------------
function creteDome path = 
(
-- 	if envBox != true do
-- 	(
	domeLight = VRayLight()
	domeLight.type = 1
	domeLight.invisible = on
	domeLight.texmap_on = on
	hdrMap = VRayHDRI ()
	hdrMap.maptype = 2
	hdrMap.HDRIMapName = path
	domeLight.texmap = hdrMap
-- 	)
)
function FileList ppath =
(
	files = getfiles ppath
)

-- function setCurrentSelectedBitmap image =
-- (
-- 	bmp = openBitMap (image)
-- 	SetDialogBitmap hdrBrowser bmp
-- )
-----------------------------------------------
-- image List 
-----------------------------------------------
imgPath = "S:/3D_Resources/Maps/HDRI/dome/*.jpg "
imgList = FileList imgPath
-----------------------------------------------
-- ui
-----------------------------------------------
Try(DestroyDialog hdrBrowser)catch()
rollout hdrBrowser " fuseFX hdr broweser"
	(
		dropdownlist hdrSelection "hdr image"\
		items:(imgList) height:4
		button import "Import" width:60 height:40 align:#center offset:[0,280]
		on hdrSelection selected i do
		(
			hdrImage = hdrSelection.items[hdrSelection.selection]
			bmp = openBitMap (hdrImage)
			SetDialogBitmap hdrBrowser bmp
		)
		on import pressed do
		(
			selection = hdrSelection.items[hdrSelection.selection]
		    result = substituteString selection ".jpg" ".hdr"
		    creteDome result 
	    )
		on hdrBrowser open do
		(
			hdrImage = hdrSelection.items[hdrSelection.selection]
			bmp = openBitMap (hdrImage)
			SetDialogBitmap hdrBrowser bmp
		)

	)

createDialog hdrBrowser width:560 height:390


)