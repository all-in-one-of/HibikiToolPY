import hou

class BasicFunc(object):

    @staticmethod
    def setWorldPos(objNode, x, y, z, fail_on_locked_parms = False):
        worldTrans = objNode.worldTransform()
        worldTrans.setAt(3, 0, x)
        worldTrans.setAt(3, 1, y)
        worldTrans.setAt(3, 2, z)
        objNode.setWorldTransform(worldTrans, fail_on_locked_parms)

    @staticmethod
    def alignWorldPos(node, target, fail_on_locked_parms = False):
        worldTrans = node.worldTransform()
        targetWorldTrans = target.worldTransform()
        worldTrans.setAt(3,0,targetWorldTrans.at(3,0))
        worldTrans.setAt(3,1,targetWorldTrans.at(3,1))
        worldTrans.setAt(3,2,targetWorldTrans.at(3,2))
        node.setWorldTransform(worldTrans, fail_on_locked_parms)

    @staticmethod
    def create_deleteAttr_after(node, pointAttr = '*', vertAttr='*', primAttr='*',detailAttr='*'):
        # type : (hou.Node, str, str,str,str)->hou.Node
        # node = hou.Node()
        deleteAttrNode = BasicFunc.create_node_after(node, 'attribdelete')
        #deleteAttrNode.parm('pt')
        return deleteAttrNode

    @staticmethod
    def create_node_after(sourceNode, newNodeTypeName, sourceOutputIndex = 0, newNodeInputIndex = 0, newNodeOutputIndex = 0):
        # type : (hou.Node,str,int,int,int)->hou.Node
        sourceOutputName = sourceNode.outputNames()[sourceOutputIndex]
        newNode = sourceNode.parent().createNode(newNodeTypeName)
        inputName = newNode.inputNames()[newNodeInputIndex]
        newNode.setNamedInput(inputName, sourceNode,sourceOutputName)
        newNodeOutputName = newNode.outputNames()[newNodeOutputIndex]
        for targetConnection in newNode.outputConnections():
            targetConnection.inputNode().setNamedInput(targetConnection.inputName(), newNode, newNodeOutputName)
        return newNode

    @staticmethod
    def connect_node(sourceNode, targetNode, sourceOutputIndex = 0, targetNodeInputIndex = 0):
        sourceOutputName = sourceNode.outputNames()[sourceOutputIndex]
        inputName = targetNode.inputNames()[targetNodeInputIndex]
        targetNode.setNamedInput(inputName, sourceNode, sourceOutputName)

    @staticmethod
    def get_nodes_in_children(node, nodeTypeName):
        result = []
        for child in node.children():
            if child.type().name() == nodeTypeName:
                result.append(child)
        return result

    @staticmethod
    def get_node_in_children(node, nodeTypeName):
        for child in node.children():
            if child.type().name() == nodeTypeName:
                return child

    @staticmethod
    def set_transform_keeppos(node, keeppos = True):
        kpParm = node.parm('keeppos')
        if kpParm:
            kpParm.set(keeppos)

    @staticmethod
    def print_node(node):
        print "path:", node.path(), " type:"+node.type().name()

    @staticmethod
    def print_nodes(nodes):
        for node in nodes:
            BasicFunc.print_node(node)

    @staticmethod
    def print_parms(node):
        for parm in node.parms():
            print parm

    @staticmethod
    def print_inputs(node):
        for inputName in node.inputNames():
            print '['+inputName+'] from ('
        # for input in node.inputs():
        #     print input

    @staticmethod
    def print_outputs(node):
        for outputName in node.outputNames():
            print outputName

    @staticmethod
    def adjustLayout(node,relative_to_inputs=True, move_inputs=False, move_outputs=True, move_unconnected=False):
        node.moveToGoodPosition(relative_to_inputs,move_inputs,move_outputs,move_unconnected)

    @staticmethod
    def layoutChildren(parentNode, childrenNodes = (),horizonOffset = -1,verticalOffset = -1):

        parentNode.layoutChildren(childrenNodes, horizonOffset, verticalOffset)
