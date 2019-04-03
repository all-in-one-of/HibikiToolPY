import sys
import hou
import os
hibikiPath = sys.argv[0]
basicToolsPath = os.path.abspath(os.path.join(hibikiPath,'../../BasicTools'))
#basicFuncPyPath = os.path.abspath('file')
#print 'bfp:', basicFuncPyPath
if basicToolsPath not in sys.path:
    #print 'not in'
    sys.path.append(basicToolsPath)
else:
    sys.path.remove(basicToolsPath)
    sys.path.append(basicToolsPath)
from BasicFunc import BasicFunc
#else:
    #print 'sys path has it:', basicFuncPyPath
#for sp in sys.path:
    #print sp,'\n'

class SplitMesh(object):

    @staticmethod
    def SubMeshesSplitToGeos(submeshNode):
        submeshNode.setHardLocked(True)
        nodeName = submeshNode.name()
        currentHomeNode = submeshNode.parent()
        outWorld = currentHomeNode.parent()
        newHomeNode = outWorld.createNode('geo')
        newHomeNode.setName(nodeName,True)
        currentHomeInputs = currentHomeNode.inputs()
        if currentHomeInputs and len(currentHomeInputs) > 0:
            BasicFunc.connect_node(currentHomeInputs[0], newHomeNode)
            BasicFunc.alignWorldPos(newHomeNode, currentHomeNode)
        BasicFunc.adjustLayout(newHomeNode)
        cpNode = hou.copyNodesTo((submeshNode,), newHomeNode)[0]
        submeshNode.setColor(hou.Color(1, 0, 0))






def execute_command(argv):
    cmdType = argv[1]
    #print 'cdmType:', cmdType
    selected = hou.selectedNodes()
    #for fbxNode in selected:
    #    JointsToBones.ConvertJointsToBones(fbxNode)
    for subMesh in selected:
        SplitMesh.SubMeshesSplitToGeos(subMesh)

if __name__ == '__main__' or  __name__ == '__builtin__':
    execute_command(sys.argv)
else:
    print __name__