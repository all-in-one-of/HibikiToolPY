import hou
from Scripts.BasicTools.BasicFunc import BasicFunc


class FBXToRS(object):
    @staticmethod
    def convert_fbx2rs(fbxnode):

        fbxShaderNode = BasicFunc.get_node_in_children(fbxnode, 'v_fbx')
        mapFilePath = fbxShaderNode.parm('map1').eval()
        rsArchiNode = fbxnode.createNode('rs_architectural')
        rsArchiNode.allowEditingOfContents()
        redshiftVopNode = BasicFunc.get_node_in_children(rsArchiNode, 'redshift_vopnet')
        rsArchiInsideNode = BasicFunc.get_node_in_children(redshiftVopNode, 'redshift::Architectural')
        print rsArchiInsideNode.path()
        rsTexNode =  redshiftVopNode.createNode('redshift::TextureSampler')
        rsTexNode.parm('tex0').set(mapFilePath)
        # for child in fbxnode.children():
        #     print(child.path()+', type:'+child.type().name())
        #     if child.type().name() == 'v_fbx':
        #         # print (child.type())
        #         # print child.params()
        #         mapFilePath = child.parm('map1').eval()
        #         # node.createNode('')
        #         rsArchiNode = fbxnode.createNode('rs_architectural')
        #         rsArchiNode.allowEditingOfContents()


    @staticmethod
    def convert_selected_fbx2rs():
        for node in hou.selectedNodes():
            FBXToRS.convert_fbx2rs(node)

