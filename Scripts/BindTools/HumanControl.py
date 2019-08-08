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

class HumanControl(object):

    @staticmethod
    def AddFKControl(boneNode):
        #x to next, y to world up, that's all!
        if boneNode.type().name() != 'bone':
            print 'not bone:', boneNode.name()
            return

        boneTransformMatrix = boneNode.worldTransform()
        ctl = BasicFunc.create_null_at_obj(boneNode)
        lookAtNode = None
        nodeOutputs = boneNode.outputs()
        if nodeOutputs is not None and len(nodeOutputs) > 0:
            lookAtNode = nodeOutputs[0]
        selfPos = BasicFunc.getWorldPos(boneNode)
        targetPos = BasicFunc.getWorldPos(lookAtNode)
        #this kind of way is really stupid....
        direction = targetPos-selfPos
        sideDirection = direction.cross(hou.Vector3(0,1,0))
        sidePos = selfPos-sideDirection
        sideEye = boneNode.parent().createNode('null')
        BasicFunc.setWorldPos(sideEye,sidePos[0],sidePos[1],sidePos[2])
        upVec = sideDirection.cross(direction)
        matrix = ctl.buildLookatRotation(sideEye,upVec)
        ctl.setWorldTransform(matrix)

        sideEye.destroy()






def execute_command(argv):
    cmdType = argv[1]
    selected = hou.selectedNodes()
    if cmdType == 'fk':
        for boneNode in selected:
            HumanControl.AddFKControl(boneNode)
    else:
        print 'unknown command for HumanControl'


if __name__ == '__main__' or __name__ == '__builtin__':
    execute_command(sys.argv)
else:
    print __name__