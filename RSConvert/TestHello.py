import hou


def say_hello():
    print 'hello'
    #result = hou.node('/obj').createNode("geo")
    for node in hou.selectedNodes():
        print('in'+node.path()+':')
        for child in node.children():
            print(child.path()+', type:'+child.type().name())

say_hello()
