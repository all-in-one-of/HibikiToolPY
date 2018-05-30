import sys
import os
import hou

pyFileFolderPath = os.path.dirname(os.path.dirname(sys.argv[0]))
if pyFileFolderPath not in sys.path:
    sys.path.append(pyFileFolderPath)
else:
    pass
    #print 'exist:', pyFileFolderPath

from RSConvert.FBXToRS import FBXToRS
from BasicTools.BasicFunc import BasicFunc


def excute_command(argv):
    cmdIndex = int(argv[1])
    cmdSwitcher = {
        0: test,
        1: fbx2rs

    }
    targetFunc = cmdSwitcher.get(cmdIndex)
    if targetFunc is not None:
        targetFunc()
    else:
        print 'None command'


def test():
    BasicFunc.print_nodes(hou.selectedNodes())


def fbx2rs():
    FBXToRS.convert_selected_fbx2rs()


excute_command(sys.argv)


