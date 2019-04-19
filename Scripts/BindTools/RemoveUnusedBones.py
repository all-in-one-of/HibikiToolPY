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

class RemoveUnusedBones(object):

    @staticmethod
    def IsNodeJoint(node):
        nodeOutputs = node.outputs()
        if nodeOutputs is not None and len(nodeOutputs) > 0:
            for outNode in nodeOutputs:
                if outNode.type().name() == 'bone':
                    return True
        return False

    @staticmethod
    def GetCaptBoneNamesSet(node):
        resultSet = set()
        #print 'deal:',node
        boneDeformNodes = BasicFunc.get_nodes_in_children(node, 'bonedeform')
        for bdn in boneDeformNodes:
            for upNode in bdn.inputs():
                tempNode_unpack = node.createNode('captureattribunpack')
                BasicFunc.connect_node(upNode,tempNode_unpack)

                captPathAttr = tempNode_unpack.geometry().findGlobalAttrib('boneCapture_pCaptPath')
                if captPathAttr:
                    #print 'attrib exist:',captPathAttr.dataType(),' ',captPathAttr.name()
                    capPathStrArr = tempNode_unpack.geometry().stringListAttribValue('boneCapture_pCaptPath')
                    #print capPathStrArr
                    resultSet = resultSet.union(set(capPathStrArr))
                    #print 'union len:', len(resultSet)
                tempNode_unpack.destroy()
        #print 'deal ok:',node,' \tcount:',len(resultSet)
        return resultSet



    @staticmethod
    def RemoveUnused(boneNodes):
        if not boneNodes:
            return
        stageNode = boneNodes[0].parent()

        usedBoneSet = set()
        for node in stageNode.children():
            nodeTypeName = node.type().name()
            if nodeTypeName == 'geo':
                usedBoneSet = usedBoneSet.union(RemoveUnusedBones.GetCaptBoneNamesSet(node))


        print 'total set len:',len(usedBoneSet)
        for boneNode in boneNodes:
            boneCregionName = boneNode.name() + '/cregion 0'
            if boneCregionName not in usedBoneSet:
                print 'not in:', boneCregionName
                if boneNode.inputs():
                    useful = False
                    for outNode in boneNode.outputs():
                        if outNode.type().name() == 'geo':
                            print 'not used but is geo parent'
                            useful = True
                            break
                    if not useful:
                        RemoveUnusedBones.DeleteBoneButKeepChildren(boneNode)

    @staticmethod
    def DeleteBoneButKeepChildren(boneNode):
        BasicFunc.set_children_transform_keeppos(boneNode)
        boneNode.destroy()


    @staticmethod
    def PrintUsed(boneNode):
        if not boneNode:
            return
        stageNode = boneNode.parent()
        boneName = boneNode.name()
        boneCregionName = boneName + '/cregion 0'
        for node in stageNode.children():
            nodeTypeName = node.type().name()
            if nodeTypeName == 'geo':
                usedBoneSet = RemoveUnusedBones.GetCaptBoneNamesSet(node)
                if boneCregionName in usedBoneSet:
                    print boneName, ' used in ' ,node.name()



def execute_command(argv):
    cmdType = argv[1]
    #print 'cdmType:', cmdType
    selected = hou.selectedNodes()
    if cmdType == 'selected':
        # for fbxNode in selected:
        #    JointsToBones.ConvertJointsToBones(fbxNode)
        RemoveUnusedBones.RemoveUnused(selected)
    elif cmdType == 'printUsed':
        if selected:
            RemoveUnusedBones.PrintUsed(selected[0])


if __name__ == '__main__' or  __name__ == '__builtin__':
    execute_command(sys.argv)
else:
    print __name__