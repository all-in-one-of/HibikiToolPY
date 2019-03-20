import sys
import hou
import os
#print execfile()
hibikiPath = sys.argv[0]
basicToolsPath =  os.path.abspath(os.path.join(hibikiPath,'../../BasicTools'))
#basicFuncPyPath = os.path.abspath('file')
#print 'bfp:', basicFuncPyPath
if basicToolsPath not in sys.path:
    print 'not in'
    sys.path.append(basicToolsPath)
from BasicFunc import BasicFunc
#else:
    #print 'sys path has it:', basicFuncPyPath
#for sp in sys.path:
    #print sp,'\n'

class JointsToBones(object):
    @staticmethod
    def ConvertJointsToBones(fbxNode):
        for child in fbxNode.children():
            if child.type().name() == 'bone':
                childInputs = child.inputs()
                if childInputs is not None and len(childInputs) > 0:

                    jointParentNode = child.inputs()[0]
                    jointParentName = jointParentNode.name()
                    jointRealName = jointParentName.split('_')[-1]

                    #print child.name(), '->' , child.inputs()
                    realBoneNode = fbxNode.createNode('bone','bone_'+jointRealName)
                    BasicFunc.adjustLayout(realBoneNode)
                    BasicFunc.connect_node(child, realBoneNode)
                    #print 'okok'



def execute_command(argv):
    cmdType = argv[1]
    #print 'cdmType:', cmdType
    selected = hou.selectedNodes()
    for fbxNode in selected:
        JointsToBones.ConvertJointsToBones(fbxNode)


if __name__ == '__main__' or  __name__ == '__builtin__':
    execute_command(sys.argv)
else:
    print __name__