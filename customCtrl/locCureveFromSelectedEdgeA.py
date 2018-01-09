import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel


def connectetToNext(edge, edgeList, index, connectedList):
    if len(edgeList) > (index + 1):
        if str(edgeList[index + 1]).split("[")[1].split("]")[0] in str(connectedList):
            return 1
        else:
            return 0
    elif len(edgeList) == 0:
        if str(edgeList[index + 1]).split("[")[1].split("]")[0] in str(connectedList):
            return 1
        else:
            return 0
    elif len(edgeList) == (index + 1):
        if str(edgeList[index - 1]).split("[")[1].split("]")[0] in str(connectedList):
            return 1
        else:
            return -1


def convertToCurve(edgesList):
    # edgesList = pm.ls(os=1)
    for edge in edgesList:
        if ":" in edge.split(".")[1]:
            print "numer", edge.isConnectedToEdge(edge.split(":")[1].replace("]", ""))
            if edge.isConnectedToEdge(edge.split(":")[1].replace("]","")):
                print edge.isConnectedToEdge(edge.split(":")[1].replace("]",""))
            temp = edgesList[edgesList.index(edge)]
            id = edgesList.index(edge)
            print temp, id
            edgesList[id] = edgesList[id - 1]
            edgesList[id - 1] = temp

    print edgesList
    edgesList = pm.ls(edgesList, fl=1)
    edgesCorrectList = []
    for edge in edgesList:
        connectedList = edge.connectedEdges()
        connectedList = ''.join(str(pm.ls(connectedList, fl=1)))
        print str(connectedList)
        print str(edge)
        # edgesCorrectList.append(egdge)

        connected = connectetToNext(edge, edgesList, edgesList.index(edge), connectedList)
        print connected
        if connected == 1:
            edgesCorrectList.append(edge)
        elif connected == -1:
            # edgesCorrectList.append("!!")
            edgesCorrectList.append(edge)
        else:
            edgesCorrectList.append(edge)
            edgesCorrectList.append("!!")

    edgesCorrectList.append("!!")
    print edgesCorrectList
    cmds.select(cl=1)
    curveList = []
    cToEdgeList = []
    curve = ""
    for edge in edgesCorrectList:
        if str(edge) not in "!!":
            print edge
            pm.select(edge, add=1)
        else:
            curve = mel.eval("polyToCurve -form 2 -degree 1;")
            curveList.append(curve[0])
            cmds.select(cl=1)
            cToEdgeList.append(curve[1])

    return curveList, edgesList, cToEdgeList

from maya import OpenMaya

def getUParam(pnt=[], crv=None):
    point = OpenMaya.MPoint(pnt[0], pnt[1], pnt[2])
    curveFn = OpenMaya.MFnNurbsCurve(getDagPath(crv))
    # print curveFn
    paramUtill = OpenMaya.MScriptUtil()
    paramPtr = paramUtill.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve == True:
        curveFn.getParamAtPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)
    else:
        point = curveFn.closestPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)
        curveFn.getParamAtPoint(point, paramPtr, 0.001, OpenMaya.MSpace.kObject)

    param = paramUtill.getDouble(paramPtr)
    return param


def getDagPath(objectName):
    print objectName
    if not isinstance(objectName, basestring) == True:
        oNodeList = []
        for o in objectName:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(o)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            oNodeList.append(oNode)
        return oNodeList
    else:
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(objectName)
        oNode = OpenMaya.MDagPath()
        selectionList.getDagPath(0, oNode)
        return oNode

edgeList = pm.ls(os=1)
print edgeList
crv, list, cEdge = convertToCurve(edgeList)
#crv = pm.ls(sl=1, fl=1)
vertList = pm.polyListComponentConversion(list, fe=1, tv=1)
sel = pm.ls(vertList, fl=1)
crvForLoc = crv[0]
locList=[]
sel = pm.PyNode(crvForLoc).numCVs()
print sel
for s in range(0, sel):
    loc = pm.spaceLocator(n="{}_LOC".format(crv[0]))
    pos = pm.pointPosition("{}.cv[{}]".format(crv[0], s))
    pm.xform(loc, ws=1, t=pos)
    #pm.xform(loc, ws=1, t=s.getPosition(space="world"))
    locList.append(loc)
print sel, crv, locList,cEdge

pm.delete(crv[1],ch=1)
pm.delete(crv[0],ch=1)

loftNode = cmds.createNode("loft", n="{}{}_LOFT".format(crv[0], crv[1]))
#loftNode = pm.PyNode("loft1")
pm.connectAttr("{}.worldSpace[0]".format(crv[0]), "{}.inputCurve[0]".format(loftNode), f=1)
pm.connectAttr("{}.worldSpace[0]".format(crv[1]), "{}.inputCurve[1]".format(loftNode), f=1)

#pm.connectAttr("{}.outputcurve".format(cEdge[0]), "{}.inputCurve[0]".format(loftNode), f=1)
#pm.connectAttr("{}.outputcurve".format(cEdge[1]), "{}.inputCurve[1]".format(loftNode), f=1)
#pm.disconnectAttr("{}.outputcurve".format(cEdge[0]), "{}.create".format(crv[0]))
#pm.disconnectAttr("{}.outputcurve".format(cEdge[1]), "{}.create".format(crv[1]))
#pm.delete(crv[1], crv[0])

print crvForLoc

attr_list = ["tangentU", "normal", "tangentV", "position"]
axes = ["X", "Y", "Z"]
u=0.5
for s in locList:
    print s
    pos = pm.xform(s, q=1, ws=1, t=1)
    print pos
    v = getUParam(pos, "polyToCurve4attachedCurve2")
    print v

    name = s.replace("_LOC", "_MP")
    pci = pm.createNode("pointOnSurfaceInfo", n=name)
    #rfc = cmds.createNode("rotateFromTangent", n="{}_RFT".format(loc))
    rfc = pm.createNode("fourByFourMatrix", n="{}_RFT".format(loc))
    dm = pm.createNode("decomposeMatrix", n="{}_DM".format(loc))
    for i, attr in enumerate(attr_list):
        for j, ax in enumerate(axes):
            if attr == "position" or attr == "output":
                norm = ""
            else:
                norm = "normalized"
                attr = attr[0].upper() + attr[1:]

            pm.connectAttr("{}.{}{}{}".format(pci, norm, attr, ax),
                           "{}.in{}{}".format(rfc, i, j))
    rfc.output.connect(dm.inputMatrix)
    pm.connectAttr("{}.outputSurface".format(loftNode), "{}.inputSurface".format(pci))

    #pm.connectAttr("{}.position".format(pci), "{}.pos".format(rfc))
    #pm.connectAttr("{}.normal".format(pci), "{}.normal".format(rfc))
    #pm.connectAttr("{}.tangentU".format(pci), "{}.tanU".format(rfc))
    #pm.connectAttr("{}.tangentV".format(pci), "{}.tanV".format(rfc))

    #cmds.connectAttr("{0}.worldSpace".format(crvForLoc), "{0}.geometryPath".format(pci))
    print v
    cmds.setAttr("{0}.parameterV".format(pci), u)
    cmds.setAttr("{0}.parameterU".format(pci), v)
    #cmds.connectAttr("{0}.position".format(pci), "{0}.translate".format(s))
    #cmds.connectAttr("{0}.outRot".format(rfc), "{0}.rotate".format(s))
    for attr in ["translate", "rotate"]:
        for ax in axes:
            pm.connectAttr("{}.output{}{}{}".format(dm, attr[0].upper(), attr[1:], ax),
                           "{}.{}{}".format(s, attr, ax))



pm.delete(crv[1], crv[0])