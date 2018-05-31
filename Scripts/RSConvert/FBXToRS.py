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
        # rsLightShaderNode = redshiftVopNode.createNode('redshift_light_shader')
        # rsLightShaderNode.setNamedInput('Light Shader',rsTexNode,'outColor')
        
        # rsMulVecNode = redshiftVopNode.createNode('redshift::RSMathMulVector')
        # rsMulVecNode.setNamedInput('input1', rsTexNode, 'outColor')
        # rsMulVecNode.setNamedInput('input2', rsArchiInsideNode, 'outColor')
        # rsSurfInsideOutputNode.setNamedInput('Surface', rsMulVecNode, 'out')
        # rsSurfInsideOutputNode.setNamedInput('Surface', rsTexNode, 'outColor')
        subOutputNode.setNamedInput('Surface Shader', rsArchiNode, 'Surface Shader')



    @staticmethod
    def convert_selected_fbx2rs():
        for node in hou.selectedNodes():
            FBXToRS.convert_fbx2rs(node)

