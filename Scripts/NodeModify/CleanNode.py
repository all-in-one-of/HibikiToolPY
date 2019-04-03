import hou
from Scripts.BasicTools.BasicFunc import BasicFunc

class CleanNode(object):

    @staticmethod
    def clean_and_lock_attr(node, cleanAttr = True, cleanGroup = True):
        if not cleanAttr and not cleanGroup:
            print 'meaningless!'
            return
        else:
            print 'cleanAttr:', cleanAttr, ' cleanGroup:', cleanGroup
        node.setHardLocked(True)
        geo = node.geometry().freeze()
        if cleanAttr:
            for ptAttr in geo.pointAttribs():
                if ptAttr.name() == "P" or ptAttr.name() == "Pw":
                    continue
                ptAttr.destroy()
            for primAttr in geo.primAttribs():
                primAttr.destroy()
            for vertAttr in geo.vertexAttribs():
                vertAttr.destroy()
            for globalAttr in geo.globalAttribs():
                globalAttr.destroy()
        if cleanGroup:
            for pointGrp in geo.pointGroups():
                pointGrp.destroy()
            for edgeGrp in geo.edgeGroups():
                edgeGrp.destroy()
            for primGrp in geo.primGroups():
                primGrp.destroy()

    @staticmethod
    def delete_primitives_and_lock(node):
        node.setHardLocked(True)
        geo = node.geometry().freeze()
        geo.deletePrims(geo.prims(), True)

    @staticmethod
    def scale_positions(node, scaleFactor):
        node.setHardLocked(True)
        geo = node.geometry().freeze()
        positions = geo.pointFloatAttribValues('P')
        pList = list(positions)
        for i in range(len(pList)):
            pList[i] *= scaleFactor
        geo.setPointFloatAttribValues('P', tuple(pList))

    @staticmethod
    def scale_bones(node, scaleFactor, hierachy = True):
        if hierachy:
            stack = []
            stack.append(node)
            while len(stack) > 0:
                currentNode = stack.pop()
                outputs = currentNode.outputs()
                if outputs:
                    for child in outputs:
                        stack.append(child)
                if currentNode.type().name() == 'bone':
                    print 'set for ',currentNode
                    currentValue = currentNode.parm('length').eval()
                    currentNode.parm('length').set(currentValue * scaleFactor)
        else:
            print 'set single for ',node
            if node.type().name() == 'bone':
                currentValue = node.parm('length').eval()
                node.parm('length').set(currentValue * scaleFactor)



    @staticmethod
    def bake_for_nodes(dealNode, targetNodes):
        for targetNode in targetNodes:
            #lock
            targetNode.setHardLocked(True)
            dealNode.setHardLocked(False)
            BasicFunc.connect_node(targetNode, dealNode)
            dealNode.setHardLocked(True)
            BasicFunc.connect_node(dealNode,targetNode)
            targetNode.setHardLocked(False)
            targetNode.setHardLocked(True)

