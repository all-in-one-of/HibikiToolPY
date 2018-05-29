import hou
import sys
import os
pyFileFolderPath = os.path.dirname(sys.argv[0])
if pyFileFolderPath not in sys.path:
    sys.path.append(pyFileFolderPath)
else:
    print 'exist:',pyFileFolderPath

from RSConvert import RSConvert


#
# def convert_fbx2rs(fbxNode):
#     for child in fbxNode.children():
#         # print(child.path()+', type:'+child.type().name())
#         if child.type().name() == 'v_fbx':
#             # print (child.type())
#             # print child.params()
#             mapFilePath = child.parm('map1').eval()
#             # node.createNode('')
#
#
#             # params = child.parms()
#             #
#             # for param in params:
#             #     if 'map' in param.name():
#             #         print param.name()
#
# def convert_selected_fbx2rs():
#     for node in hou.selectedNodes():
#         convert_fbx2rs(node)
#
RSConvert.convert_selected_fbx2rs()
