import sys
import hou
import os
hibikiPath = sys.argv[0]
basicToolsPath = os.path.abspath(os.path.join(hibikiPath,'../../BasicTools'))
if basicToolsPath not in sys.path:
    sys.path.append(basicToolsPath)
else:
    sys.path.remove(basicToolsPath)
    sys.path.append(basicToolsPath)
from BasicFunc import BasicFunc
from BoneQuery import BoneQuery

class HairControl(object):

    @staticmethod
    def GetBoneLine(rootBone):
        lineBones = []
        if rootBone:
            stack = []
            stack.append(rootBone)
            while len(stack) > 0:
                currentNode = stack.pop()
                if currentNode.type().name() != 'bone':
                    continue
                lineBones.append(currentNode)
                nodeOutputs = currentNode.outputs()
                if nodeOutputs and len(nodeOutputs) == 1:
                    stack.append(nodeOutputs[0])
        return lineBones

    @staticmethod
    def CreatePointInGeo(pos, geo):
        if not geo:
            return None
        newPoint = geo.createPoint()
        newPoint.setPosition(pos)
        return newPoint

    @staticmethod
    def DealBoneLines(rootBones):
        if not rootBones:
            return
        worldStage = rootBones[0].parent()
        curveObjNode = worldStage.createNode('geo')
        curveObjNode.setName('curve',True)
        curveNode = curveObjNode.createNode('null')
        curveNode.setHardLocked(True)
        curveGeo = curveNode.geometry().freeze()
        percentAttrName = 'percentOnCurve'
        curveGeo.addAttrib(hou.attribType.Point,percentAttrName,float(0))

        lineList = []
        #curvePosList = []
        ptCount = 0
        indexList = []
        for rootBone in rootBones:
            line = HairControl.GetBoneLine(rootBone)
            lineList.append(line)
            #curve = []
            boneCount = len(line)

            oneLineIndex = []
            for i in range(boneCount):
                bone = line[i]
                newPoint = HairControl.CreatePointInGeo(BasicFunc.getWorldPos(bone), curveGeo)
                pPercent = float(i)/boneCount
                newPoint.setAttribValue(percentAttrName, pPercent)
                #curve.append(newPoint)
                oneLineIndex.append(ptCount)
                ptCount = ptCount + 1

            #print 'end bone:', line[boneCount-1]
            lastPoint = HairControl.CreatePointInGeo(BoneQuery.GetBoneEndPos(line[boneCount-1]), curveGeo)
            #curve.append()
            lastPoint.setAttribValue(percentAttrName, float(1))
            oneLineIndex.append(ptCount)
            ptCount = ptCount + 1
            #curvePosList.append(curve)
            indexList.append(oneLineIndex)
        #print curvePosList
        #for curveLine in curvePosList:
            #curveGeo.createPoints(curveLine)
        polygons = curveGeo.createPolygons(indexList)
        for poly in polygons:
            poly.setIsClosed(False)

def execute_command(argv):
    cmdType = argv[1]
    #print 'cdmType:', cmdType
    selected = hou.selectedNodes()
    if cmdType == 'chb':
        HairControl.DealBoneLines(selected)


if __name__ == '__main__' or  __name__ == '__builtin__':
    execute_command(sys.argv)
else:
    print __name__