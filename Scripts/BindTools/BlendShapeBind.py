import hou
from Scripts.BasicTools.BasicFunc import BasicFunc

class BlendShapeBind(object):
    @staticmethod
    def setBlendShapeControl(bsNode, ctlNode = None):
        if ctlNode is None:
            bsNodePath = bsNode.path()
            nodePathParts = bsNodePath.split('/')
            containerNodePath = '/'+nodePathParts[0]+'/'+nodePathParts[1]
            ctlNode = hou.node(containerNodePath)
            if ctlNode is None:
                print 'wrong path:', containerNodePath

        useExist = node.parm('useExist').eval()

        ctlNode = hou.node('/obj/geo1')
        # ctlNode.parm('tx').set(ctlNode.parm('ty'))
        bsNode = hou.node('../blendshapes1')
        count = 0
        blendParms = []
        for parm in bsNode.parms():
            if count > 0:
                # print 'blend ',count,':',parm.name()
                blendParms.append(parm)
                count = count - 1
            elif parm.name() == 'nblends':
                count = parm.eval()

                print 'find nblends'
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
            print 'want add:', currentParmTempName
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