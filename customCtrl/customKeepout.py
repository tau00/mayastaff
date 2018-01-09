import maya.cmds as cmds
import pymel.core as pm

selection = pm.ls(sl=1)
name = "nowa"
coliderName = ""
selectCtrl = pm.ls(sl=1)
for obj in selection:
    pos = pm.xform(obj, q=1, ws=1, t=1)
    locName = pm.spaceLocator(n="{}loc".format(name))
    pm.xform(locName, ws=1, t=pos)
    print locName
    pm.makeIdentity(locName)
    #followUpLidNode = cmds.createNode("transform", name=name + "_followUp_%s" % name)
    #followUpNodeList.append(followUpLidNode)
    # tworze keepout nodey oraz grupe ofsetujaca - offset grupa ma orient constrainta od glowy
    upKeepOutNode = addKeepOutForNode(node=locName, inDirection="Z", negativeDirection=True)

def addKeepOutForNode(node, inDirection, negativeDirection):
    keepOutShape = cmds.createNode("cMuscleKeepOut", n="{}_KONShape".format(node))
    tempTransform = cmds.listRelatives(keepOutShape, p=True)
    transform = cmds.rename(tempTransform, "{}_KON".format(node))
    print node
    pm.parent(pm.PyNode(transform).name(), pm.PyNode(node).name())
    pm.makeIdentity(transform)
    Driven = cmds.createNode("transform", n=node + "_KON_Driven")
    cmds.parent(Driven, transform)
    cmds.makeIdentity(Driven)

    cmds.setAttr("%s.inDirectionX" % keepOutShape, 0)
    if negativeDirection == True:
        cmds.setAttr("%s.inDirection%s" % (keepOutShape, inDirection), -1)
    else:
        cmds.setAttr("%s.inDirection%s" % (keepOutShape, inDirection), 1)

    cmds.connectAttr("%s.worldMatrix[0]" % transform , "%s.worldMatrixAim" % keepOutShape)
    cmds.connectAttr("%s.outTranslateLocal" % keepOutShape, "%s.translate" % Driven)


