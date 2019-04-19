import sys
import hou
import os


class BoneQuery(object):
    @staticmethod
    def GetBoneEndPos(boneNode):
        if boneNode:
            worldTrans = boneNode.worldTransform()
            #return (worldTrans.at(3, 0), worldTrans.at(3, 1), worldTrans.at(3, 2))
            boneLength = boneNode.parm('length').eval()
            localOffset = hou.Vector3(0, 0, -boneLength)
            return localOffset * worldTrans
