import hou
from Scripts.BasicTools.BasicFunc import BasicFunc


class FBXToRS(object):
    @staticmethod
    def convert_fbx2rs(fbxnode):

        fbxShaderNode = BasicFunc.get_node_in_children(fbxnode, 'v_fbx')
        subOutputNode = BasicFunc.get_node_in_children(fbxnode, 'suboutput')
        mapFilePath = fbxShaderNode.parm('map1').eval()
        rsArchiNode = fbxnode.createNode('rs_architectural')
        rsArchiNode.parm("reflectivity").set(0)
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

    @staticmethod
    def convert_fbx2principle(fbxNode):
        selected = hou.selectedNodes()
        matnet = fbxNode.createNode('matnet')
        newMatDic = {}
        for child in fbxNode.children():
            shopMatPathParm = child.parm('shop_materialpath')
            matPath = shopMatPathParm.eval()
            if len(matPath) == 0:
                continue
            # print 'matPath:',matPath
            matNode = child.node(matPath)
            print 'matNode:', matNode
            matNodeFullPath = matNode.path()
            # seek for exist
            psdNodePath = ''
            if matNodeFullPath in newMatDic:
                psdNodePath = newMatDic[matNodeFullPath]
            else:
                psdNode = matnet.createNode('principledshader::2.0')
                FBXToRS.CopyFbxMatToPrinciple(matNode, psdNode, True)
                psdNodePath = psdNode.path()
                newMatDic[matNodeFullPath] = psdNodePath
            shopMatPathParm.set(psdNodePath)


    @staticmethod
    def CopyFbxMatToPrinciple(fbxMatNode, psdNode, copyName=False):
        if copyName:
            psdNode.setName(fbxMatNode.name())
        fbxShaderNode = BasicFunc.get_node_in_children(fbxMatNode, 'v_fbx')
        mapFilePath = fbxShaderNode.parm('map1').eval()
        cdr = fbxShaderNode.parm('Cdr').eval()
        cdg = fbxShaderNode.parm('Cdg').eval()
        cdb = fbxShaderNode.parm('Cdb').eval()
        psdNode.parm('basecolorr').set(cdr)
        psdNode.parm('basecolorg').set(cdg)
        psdNode.parm('basecolorb').set(cdb)
        texPath = fbxShaderNode.parm('map1').eval()
        if len(texPath) > 0:
            psdNode.parm('basecolor_useTexture').set(1)
            psdNode.parm('basecolor_texture').set(texPath)