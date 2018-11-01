import hou
from Scripts.BasicTools.BasicFunc import BasicFunc

class CleanNode(object):

    @staticmethod
    def clean_and_lock_attr(node):
        node.setHardLocked(True)
        geo = node.geometry().freeze()
        for ptAttr in geo.pointAttribs():
            if ptAttr.name() == "P" or ptAttr.name() == "Pw":
                continue
            ptAttr.destroy()
        for primAttr in geo.primAttribs():
            primAttr.detroy()
        for vertAttr in geo.vertexAttribs():
            vertAttr.destroy()
        for globalAttr in geo.globalAttribs():
            globalAttr.destroy()
