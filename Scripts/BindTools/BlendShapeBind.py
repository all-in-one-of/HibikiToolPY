import sys
import hou

# from ..BasicTools.BasicFunc import BasicFunc
class BlendShapeBind(object):
    @staticmethod
    def setBlendShapeControl(bsNode, useExist = True, ctlNode = None):
        if ctlNode is None:
            bsNodePath = bsNode.path()
            nodePathParts = bsNodePath.split('/')
            #print 'nodePathParts:', nodePathParts[0:3]
            containerNodePath = '/'.join(nodePathParts[0:3])# '/'+nodePathParts[0]+'/'+nodePathParts[1]+'/'+nodePathParts[2]
            #print 'containerNodePath:', containerNodePath
            ctlNode = hou.node(containerNodePath)
            if ctlNode is None:
                print 'wrong path:', containerNodePath
            else:
                #print 'ctlNode:', ctlNode
                pass

        #useExist = bsNode.parm('useExist').eval()

        #ctlNode = hou.node('/obj/geo1')
        #bsNode = hou.node('../blendshapes1')
        count = 0
        blendParms = []
        for parm in bsNode.parms():
            if count > 0:
                # print 'blend ',count,':',parm.name()
                blendParms.append(parm)
                count = count - 1
            elif parm.name() == 'nblends':
                count = parm.eval()
                # print 'find nblends'
        parm_group = ctlNode.parmTemplateGroup()
        folderName = bsNode.name()
        createFolder = 0
        parm_folder = parm_group.findFolder(folderName)
        if parm_folder is None:
            createFolder = 1
            parm_folder = hou.FolderParmTemplate('folder', folderName)
        resultParmNames = []
        for parm in blendParms[1:]:
            parmTemp = parm.parmTemplate()
            currentParmTempName = parmTemp.name()
            # print 'want add:', currentParmTempName
            if not ctlNode.parm(currentParmTempName) is None:
                if useExist:
                    pass
                else:
                    currentParmTempName += '1'
                    while not ctlNode.parm(currentParmTempName) is None:
                        # exist so change name
                        currentParmTempName += '1'
                    parmTemp.setName(currentParmTempName)
                    parm_folder.addParmTemplate(parmTemp)
            else:
                parmTemp.setName(currentParmTempName)
                parm_folder.addParmTemplate(parmTemp)
            resultParmNames.append(currentParmTempName)

        print resultParmNames
        if createFolder:
            parm_group.append(parm_folder)
            ctlNode.setParmTemplateGroup(parm_group)
        for i in range(len(blendParms) - 1):
            # print blendParms[i+1]
            ctlParm = ctlNode.parm(resultParmNames[i])
            blendParms[i + 1].deleteAllKeyframes()
            blendParms[i + 1].set(ctlParm)
            # ctlParm.deleteAllKeyframes()


def execute_command(argv):
    cmdType = argv[1]
    #print 'cdmType:', cmdType
    if cmdType == 'BindBSControlOnTopObj':
        slNodes = hou.selectedNodes()
        # print 'execute for node:', slNodes
        if len(slNodes) > 0:
            bsNode = slNodes[0]
            if bsNode.type().name() == 'blendshapes::2.0':
                BlendShapeBind.setBlendShapeControl(bsNode)
    elif cmdType == 'BindBSControlOnSecond':
        slNodes = hou.selectedNodes()
        if len(slNodes) == 2:
            bsNode = slNodes[0]
            ctlNode = slNodes[1]
            if bsNode.type().name() == 'blendshapes::2.0':
                BlendShapeBind.setBlendShapeControl(bsNode, True, ctlNode)



execute_command(sys.argv)

