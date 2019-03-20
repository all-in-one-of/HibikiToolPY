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
from NodeModify.CleanNode import CleanNode


def excute_command(argv):
    cmdType = int(argv[1])
    cmdIndex = int(argv[2])
    testCmdSwitcher = {
        -1: reloadPlugin,
        0: printNodes,
        1: printParms,
        2: printInputs,
        3: printOutputs
    }
    rsCmdSwitcher = {
        0: fbx2rs
        1: fbx2principle
    }

    nodeCleanCmdSwitcher = {
        0: cleanAndFreezeNodes,
        1: deletePrimitives,
        2: bakeNodesWithFirst
    }

    fbxImportDealSwitcher = {
        0: scalePositionsDown,
        1: scalePositionsUp
    }


    #total switch
    cmdSwitcher = {
        0: testCmdSwitcher,
        1: rsCmdSwitcher,
        2: nodeCleanCmdSwitcher,
        3: fbxImportDealSwitcher
    }

    targetFunc = cmdSwitcher.get(cmdType).get(cmdIndex)
    if targetFunc is not None:
        targetFunc()
    else:
        print 'None command'

def reloadPlugin():
    reload(FBXToRS)
    reload(BasicFunc)

def printNodes():
    BasicFunc.print_nodes(hou.selectedNodes())

def printParms():
    BasicFunc.print_parms(hou.selectedNodes()[0])

def printInputs():
    BasicFunc.print_inputs(hou.selectedNodes()[0])

def printOutputs():
    BasicFunc.print_outputs(hou.selectedNodes()[0])


def fbx2rs():
    FBXToRS.convert_selected_fbx2rs()

def fbx2principle():
    for node in hou.selectedNodes():
        FBXToRS.convert_fbx2principle(node)

def cleanAndFreezeNodes():
    for node in hou.selectedNodes():
        CleanNode.clean_and_lock_attr(node)

def deletePrimitives():
    for node in hou.selectedNodes():
        CleanNode.delete_primitives_and_lock(node)

def scalePositionsDown():
    for node in hou.selectedNodes():
        CleanNode.scale_positions(node, 0.01)

def scalePositionsUp():
    for node in hou.selectedNodes():
        CleanNode.scale_positions(node, 100)

def bakeNodesWithFirst():
    nodesSelected = hou.selectedNodes()
    CleanNode.bake_for_nodes(nodesSelected[0], nodesSelected[1:])


excute_command(sys.argv)


