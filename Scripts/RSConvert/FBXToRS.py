import hou


class FBXToRS(object):
    @staticmethod
    def convert_fbx2rs(fbxnode):
        for child in fbxnode.children():
            print(child.path()+', type:'+child.type().name())
            if child.type().name() == 'v_fbx':
                # print (child.type())
                # print child.params()
                mapFilePath = child.parm('map1').eval()
                # node.createNode('')
                rsArchiNode = fbxnode.createNode('rs_architectural')
                rsArchiNode.allowEditingOfContents()

    @staticmethod
    def convert_selected_fbx2rs():
        for node in hou.selectedNodes():
            FBXToRS.convert_fbx2rs(node)

