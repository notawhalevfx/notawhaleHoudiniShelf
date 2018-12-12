########################
# Some scripts for Smoke/Pyro simulation
# Nikita Musatov
# not.a.whale@gmail.com
#
# skype: notawhale
#
#
########################
import toolutils,os,hou

bbox = """bbox(chs('{path}'),D_{TYPE}SIZE) + ch('naw_expand{type}')"""
centroid = """centroid(chs('{path}'),D_{TYPE}) + explodematrix(optransform(opcreator(chs('{path}'))),"SRT","XYZ","T{TYPE}")"""
DIM = ["x","y","z"]

if hou.applicationVersion()[0]>=17:
    src = ["volumesource","soppath"]
else:
    src = ["sourcevolume","source_path"]

def dialog(tp):
    nodes = hou.selectedNodes()
    found_node = None
    for nd in nodes:
        if nd.type().name() == tp:
            found_node = nd
    if not found_node:
        raise hou.Error("Node type {} wasn't selected".format(tp))
    return found_node
    
def addExtendSize(node,parm=None):
        try:
                ptg = node.parmTemplateGroup()
                extendParm = hou.FloatParmTemplate("naw_expand","Expand",3,(0,0,0))
                ptg.insertAfter("t",extendParm)
                node.setParmTemplateGroup(ptg)
        except hou.OperationFailed:
                pass
        if parm!= None:
                parm.set(node.parm("executeAf"))

def setExpressionSrcToObj(smk_obj,vol_src):
    path = os.path.join(smk_obj.relativePathTo(vol_src),src[1])
    for dim in DIM:
        smk_obj.parm("size"+dim).setExpression(bbox.format(path=path,type=dim,TYPE=dim.capitalize()))
        smk_obj.parm("t"+dim).setExpression(centroid.format(path=path,TYPE=dim.capitalize()))

def connectSourceToObject(kwargs):
    smk_obj = dialog("smokeobject")
    vol_src = dialog(src[0])
    addExtendSize(smk_obj)
    setExpressionSrcToObj(smk_obj,vol_src)

def setExpressionSrcToTrk(gasresize,vol_src):
    path = os.path.join(gasresize.relativePathTo(vol_src),src[1])
    gasresize.parm("use_tracking_objects").set(vol_src.parm("activation"))
    gasresize.parm("tracking_path").set("""`chs("{}")`""".format(path))

def connectSourceToResizeTrackingObject(kwargs):
    gasresize = dialog("gasresizefluiddynamic")
    vol_src = dialog(src[0])
    setExpressionSrcToTrk(gasresize,vol_src)
