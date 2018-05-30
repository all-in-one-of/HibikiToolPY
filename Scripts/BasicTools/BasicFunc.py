import hou


class BasicFunc(object):

    @staticmethod
    def get_nodes_in_children(node, nodeTypeName):
        result = []
        for child in node.children():
            if child.type().name() == nodeTypeName:
                result.append(child)
        return result

    @staticmethod
    def print_node(node):
        print "path:", node.path(), " type:"+node.type().name()

    @staticmethod
    def print_nodes(nodes):
        for node in nodes:
            BasicFunc.print_node(node)



