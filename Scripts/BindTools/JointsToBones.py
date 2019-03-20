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

class JointsToBones(object):
    @staticmethod
    def ConvertJointsToBones(fbxNode):
        #print 'begin convert fbxNode', fbxNode.name()
        newNodes = []
        parentNullNodes = []
        for child in fbxNode.children():
            if child.type().name() == 'bone':
                childInputs = child.inputs()
                if childInputs is not None and len(childInputs) > 0:

                    jointParentNode = child.inputs()[0]
                    parentNullNodes.append(jointParentNode)
                    jointParentNode.parm('keeppos').set(True)
                    jointParentName = jointParentNode.name()
                    jointRealName = jointParentName.split('_')[-1]

                    #print child.name(), '->' , child.inputs()
                    realBoneNode = fbxNode.createNode('bone','bone_'+jointRealName)
                    realBoneNode.parm('length').set(child.parm('length').eval())
                    realBoneNode.setColor(hou.Color(1,0,0))
                    #realBoneNode.setInput(0,None,0)
                    newNodes.append(realBoneNode)
                    BasicFunc.connect_node(child, realBoneNode)
                    BasicFunc.alignWorldPos(realBoneNode, jointParentNode)
                    realBoneNode.parm('keeppos').set(True)
                    BasicFunc.adjustLayout(realBoneNode)
                    child.setDisplayFlag(False)
                    child.destroy()

        #BasicFunc.layoutChildren(fbxNode, newNodes, 0, 1)
        for i in range(len(newNodes)):
            mother = parentNullNodes[i]
            motherInputs = mother.inputs()
            if motherInputs is not None and len(motherInputs)>0:
                grandma = motherInputs[0]
                if grandma in parentNullNodes:
                    father = newNodes[parentNullNodes.index(grandma)]
                    BasicFunc.connect_node(father, newNodes[i])
            else:
                newNodes[i].setInput(0,None,0)
        for i in range(len(newNodes)):
            targetName = parentNullNodes[i].name()
            parentNullNodes[i].destroy()
            newNodes[i].setName(targetName)


def execute_command(argv):
    cmdType = argv[1]
    #print 'cdmType:', cmdType
    selected = hou.selectedNodes()
    for fbxNode in selected:
        JointsToBones.ConvertJointsToBones(fbxNode)


if __name__ == '__main__' or  __name__ == '__builtin__':
    execute_command(sys.argv)
else:
    print __name__