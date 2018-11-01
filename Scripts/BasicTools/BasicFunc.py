import hou

class BasicFunc(object):


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