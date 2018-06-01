import hou
from Scripts.BasicTools.BasicFunc import BasicFunc


class FBXToRS(object):
    @staticmethod
    def convert_fbx2rs(fbxnode):

        fbxShaderNode = BasicFunc.get_node_in_children(fbxnode, 'v_fbx')
        subOutputNode = BasicFunc.get_node_in_children(fbxnode, 'suboutput')
        mapFilePath = fbxShaderNode.parm('map1').eval()
        rsArchiNode = fbxnode.createNode('rs_architectural')
        rsArchiNode.allowEditingOfContents()
        redshiftVopNode = BasicFunc.get_node_in_children(rsArchiNode, 'redshift_vopnet')
        rsArchiInsideNode = BasicFunc.get_node_in_children(redshiftVopNode, 'redshift::Architectural')
        rsSurfInsideOutputNode = BasicFunc.get_node_in_children(redshiftVopNode, 'redshift_material')
        # print rsArchiInsideNode.path()
        rsTexNode = redshiftVopNode.createNode('redshift::TextureSampler')
        rsTexNode.parm('tex0').set(mapFilePath)
        rsArchiInsideNode.setNamedInput('diffuse', rsTexNode, 'outColor')
        rsColorSplitterNode = redshiftVopNode.createNode('redshift::RSColorSplitter')
        rsSubFloatNode = redshiftVopNode.createNode('redshift::RSMathSub')
        rsColorSplitterNode.setNamedInput('input', rsTexNode, 'outColor')
        rsSubFloatNode.setNamedInput('input2', rsColorSplitterNode, 'outA')
        rsSubFloatNode.parm('input1').set(1)
        rsArchiInsideNode.setNamedInput('transparency', rsSubFloatNode, 'out')
        rsArchiInsideNode.parm('refr_ior').set(1)
        subOutputNode.setNamedInput('Surface Shader', rsArchiNode, 'Surface Shader')



    @staticmethod
    def convert_selected_fbx2rs():
        for node in hou.selectedNodes():
            FBXToRS.convert_fbx2rs(node)

