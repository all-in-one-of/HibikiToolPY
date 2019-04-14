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
    def IsNodeJoint(node):
        nodeOutputs = node.outputs()
        if nodeOutputs is not None and len(nodeOutputs) > 0:
            for outNode in nodeOutputs:
                if outNode.type().name() == 'bone':
                    return True;
        return False

    @staticmethod
    def ConvertJointsToBones(fbxNode):
        #print 'begin convert fbxNode', fbxNode.name()
        newNodes = []
        parentNullNodes = []
        destroyList = []
        geoList = []
        for child in fbxNode.children():
            childTypeName = child.type().name()
            if childTypeName == 'bone':
                childInputs = child.inputs()
                if childInputs is not None and len(childInputs) > 0:

                    jointParentNode = child.inputs()[0]
                    parentNullNodes.append(jointParentNode)
                    jointParentNode.parm('keeppos').set(True)
                    #jointParentName = jointParentNode.name()
                    #jointRealName = jointParentName.split('_')[-1]

                    #print child.name(), '->' , child.inputs()
                    realBoneNode = fbxNode.createNode('bone')#,'bone_'+jointRealName)
                    realBoneNode.parm('length').set(child.parm('length').eval())
                    realBoneNode.setColor(hou.Color(1,0,0))
                    #realBoneNode.setInput(0,None,0)
                    newNodes.append(realBoneNode)
                    BasicFunc.connect_node(child, realBoneNode)
                    BasicFunc.alignWorldPos(realBoneNode, jointParentNode)
                    realBoneNode.parm('keeppos').set(True)
                    BasicFunc.adjustLayout(realBoneNode)
                    child.setDisplayFlag(False)
                    destroyList.append(child)
            elif childTypeName == 'geo':
                geoList.append(child)

            elif childTypeName == 'null':
                if len(child.outputs()) == 0:
                    childInputs = child.inputs()
                    if childInputs is not None and len(childInputs)>0:
                        if JointsToBones.IsNodeJoint(childInputs[0]):
                            # this is the end joint
                            child.parm('keeppos').set(True)
                            endBone = fbxNode.createNode('bone')
                            endBone.parm('length').set(0)
                            BasicFunc.connect_node(child,endBone)
                            endBone.parm('keeppos').set(True)
                            BasicFunc.adjustLayout(endBone)
                            newNodes.append(endBone)
                            parentNullNodes.append(child)


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
        targetNames = []
        for i in range(len(newNodes)):
            try:
                targetName = parentNullNodes[i].name()
                #parentNullNodes[i].destroy()
                if not parentNullNodes[i] in destroyList:
                    destroyList.append(parentNullNodes[i])
                targetNames.append(targetName)
                # newNodes[i].setName(targetName)
            except:
                print 'exception on:', newNodes[i]
        for dn in destroyList:
            dn.destroy()
        for i in range(len(newNodes)):
            newNodes[i].setName(targetNames[i],True)

        for geoNode in geoList:
            # find bone capture node
            currentRenderNode = geoNode.renderNode()
            captureNode = None
            for insideNode in geoNode.children():
                # print insideNode
                if insideNode.type().name() == 'capture':
                    captureNode = insideNode
                    break
            if captureNode:
                print 'capture node:', captureNode
                cpNode = hou.copyNodesTo((captureNode,), geoNode)[0]
                cpNode.setHardLocked(False)
                attrCopyNode = geoNode.createNode('attribcopy')
                BasicFunc.connect_node(cpNode, attrCopyNode,0,0)
                BasicFunc.connect_node(captureNode, attrCopyNode,0,1)
                attrCopyNode.parm('attribname').set('*')
                BasicFunc.connect_node(attrCopyNode, currentRenderNode)
                # print 'regions:', captureNode.parm('extraregions').eval()

    @staticmethod
    def ConvertJointsToBones_Hierachy(rootNode):
        #print 'parent:', rootNode.parent()
        #rootNode.parent().createNode('null','testnull')
        destroyList = []
        stack = []
        realBoneList = []
        newNames = []
        firstAuthority = []
        subnet = rootNode.parent()
        stack.append(rootNode)
        BasicFunc.set_transform_keeppos(rootNode)
        while len(stack) > 0:
            nullNode = stack.pop()
            # print nullNode
            nodeInputs = nullNode.inputs()
            hierachyParent = None
            if nodeInputs is not None and len(nodeInputs) > 0:
                hierachyParent = nodeInputs[0]

            destroyList.append(nullNode)
            firstFlag = True
            nullNodeOutputs = nullNode.outputs()
            if nullNodeOutputs is not None and len(nullNodeOutputs) > 0:
                for child in nullNode.outputs():
                    BasicFunc.set_transform_keeppos(child)
                    childTypeName = child.type().name()
                    # print childTypeName
                    if childTypeName == 'null':
                        #print 'append', child
                        stack.append(child)
                    elif childTypeName == 'bone':
                        #child 是替代骨骼
                        nodeLookAt = child.node(child.parm('lookatpath').eval())
                        BasicFunc.set_transform_keeppos(nodeLookAt)
                        # create bone node and parent to origin parent
                        realBoneNode = subnet.createNode('bone')
                        realBoneList.append(realBoneNode)
                        #append !!!!!
                        newNames.append(nullNode.name())
                        if firstFlag:
                            firstFlag = False
                            firstAuthority.append(True)
                        else:
                            firstAuthority.append(False)
                        realBoneNode.parm('length').set(child.parm('length').eval())
                        realBoneNode.setColor(hou.Color(1, 0, 0))
                        BasicFunc.connect_node(child, realBoneNode)
                        BasicFunc.alignWorldPos(realBoneNode, nullNode)
                        realBoneNode.parm('keeppos').set(True)
                        BasicFunc.adjustLayout(realBoneNode)
                        if hierachyParent:
                            BasicFunc.connect_node(hierachyParent, realBoneNode)
                        else:
                            realBoneNode.setInput(0, None, 0)
                        BasicFunc.connect_node(realBoneNode,nodeLookAt)
                        destroyList.append(child)
            else:
                endBoneNode = subnet.createNode('bone')
                BasicFunc.connect_node(nullNode, endBoneNode)
                endBoneNode.parm('length').set(0)
                BasicFunc.adjustLayout(endBoneNode)
                BasicFunc.alignWorldPos(endBoneNode, nullNode)
                endBoneNode.parm('keeppos').set(True)
                realBoneList.append(endBoneNode)
                newNames.append(nullNode.name())
                firstAuthority.append(True)
        for deadNode in destroyList:
            deadNode.destroy()
        for i in range(len(realBoneList)):
            if firstAuthority[i]:
                realBoneList[i].setName(newNames[i],True)
            else:
                realBoneList[i].setName(newNames[i]+'_00', True)
        for geoNode in subnet.children():
            if geoNode.type().name() == 'geo':
                # find bone capture node
                currentRenderNode = geoNode.renderNode()
                captureNode = None
                for insideNode in geoNode.children():
                    # print insideNode
                    if insideNode.type().name() == 'capture':
                        captureNode = insideNode
                        break
                if captureNode:
                    print 'capture node:', captureNode
                    cpNode = hou.copyNodesTo((captureNode,), geoNode)[0]
                    cpNode.setHardLocked(False)
                    attrCopyNode = geoNode.createNode('attribcopy')
                    BasicFunc.connect_node(cpNode, attrCopyNode,0,0)
                    BasicFunc.connect_node(captureNode, attrCopyNode,0,1)
                    attrCopyNode.parm('attribname').set('*')
                    BasicFunc.connect_node(attrCopyNode, currentRenderNode)


    @staticmethod
    def SelectEndJointsInHierachy(rootBone):
        stack = []
        endBones = []
        stack.append(rootBone)
        while len(stack) > 0:
            currentNode = stack.pop()
            nodeOutputs = currentNode.outputs()
            if nodeOutputs is not None and len(nodeOutputs) > 0:
                for child in nodeOutputs:
                    stack.append(child)
            else:
                endBones.append(currentNode)
        #hou.Node.setSelected(endBones,True,True)
        #hou.SceneViewer.setCurrentGeometrySelection('bone', endBones)

        for i in range(len(endBones)):
            endBones[i].setSelected(True, i == 0, False)



def execute_command(argv):
    cmdType = argv[1]
    #print 'cdmType:', cmdType
    selected = hou.selectedNodes()
    if cmdType == 'jtb':
        # for fbxNode in selected:
        #    JointsToBones.ConvertJointsToBones(fbxNode)
        for rootNode in selected:
            JointsToBones.ConvertJointsToBones_Hierachy(rootNode)
    elif cmdType == 'seb':
        JointsToBones.SelectEndJointsInHierachy(selected[0])


if __name__ == '__main__' or  __name__ == '__builtin__':
    execute_command(sys.argv)
else:
    print __name__