########################
# Reset Simulation
# Nikita Musatov
# not.a.whale@gmail.com
#
# skype: notawhale
#
########################

import hou

def FindAllDopNetNode(node):
    dop_nodes = []
    if node.type().name() == "dopnet":
        dop_nodes.append(node)
    for nd in node.children():
        dop_nodes += FindAllDopNetNode(nd)
    return dop_nodes

def ResetSimulation(dopnode):
    if dopnode.type().name() == "dopnet":
        dopnode.parm("resimulate").pressButton()

def run(kwargs):
    if kwargs["ctrlclick"]:
        for dopnode in FindAllDopNetNode(hou.root()):
            ResetSimulation(dopnode)        
    else:
        dopnode = hou.currentDopNet()
        if dopnode!=None:
            ResetSimulation(dopnode)