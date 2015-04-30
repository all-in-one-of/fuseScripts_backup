import sys
import nuke
r = nuke.nodes.Read(file = sys.argv[1])
ref = nuke.nodes.Reformat(format="%s %s" % (512, 256),resize="none").setInput(0, r)
w = nuke.nodes.Write(file = sys.argv[2])
w.setInput(0, ref)

