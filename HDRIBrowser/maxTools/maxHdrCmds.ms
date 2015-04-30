enter function creteDome path = 
(
	domeLight = VRayLight()
	domeLight.type = 1
	domeLight.invisible = on
	domeLight.texmap_on = on
	domeLight.multiplier = 1
	domeLight.dome_spherical = on
	hdrMap = VRayHDRI ()
	hdrMap.maptype = 2
	hdrMap.HDRIMapName = path
	domeLight.texmap = hdrMap
)

