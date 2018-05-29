import hou

class RSConvert:
    @staticmethod
    def convert_fbx2rs(fbxnode):
        for child in fbxnode.children():
            # print(child.path()+', type:'+child.type().name())
            if child.type().name() == 'v_fbx':
                # print (child.type())
                # print child.params()
                mapFilePath = child.parm('map1').eval()
                # node.createNode('')


                # params = child.parms()
                #
                # for param in params:
                #     if 'map' in param.name():
                #         print param.name()

    @staticmethod
    def convert_selected_fbx2rs():
        for node in hou.selectedNodes():
            RSConvert.convert_fbx2rs(node)
