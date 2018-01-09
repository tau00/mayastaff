from customCtrlUi import Ui_CUCO
import traceback
from maya import OpenMayaUI as omui
import maya.OpenMaya as OpenMaya

import numpy as np
import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm
import string
try:
  from PySide2.QtCore import *
  from PySide2.QtGui import *
  from PySide2.QtWidgets import *
  from PySide2 import __version__
  from shiboken2 import wrapInstance
except ImportError:
  from PySide.QtCore import *
  from PySide.QtGui import *
  from PySide import __version__
  from shiboken import wrapInstance

# PARENT TO MAYA
def maya_main_window():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    return mayaMainWindow #shiboken.wrapInstance(long(main_window_ptr), QtGui.QWidget)


class CucoMain(QWidget, Ui_CUCO):

    def __init__(self, parent=None):
        super(CucoMain, self).__init__(parent)
        self.setupUi(self)
        self.allClickCtrlSetup()
        self.controlListSetup()

    def selectListObj(self, grpName, objSuffixName=None):
        # objSel = ["_JNT","_meshDrive","_pCtr"]
        check = cmds.ls(grpName)
        if check:
            cmds.select(grpName, hi=1, r=1)
            allObj = cmds.ls(sl=1, type="transform")
            newList = []
            if objSuffixName == None:
                # for obj in allObj:
                newList = allObj
            else:
                for obj in allObj:
                    if (obj.find(objSuffixName) + 1) != 0:
                        newList.append(obj)
            cmds.select(cl=1)
        else:
            newList = []
        return newList

    def controlListSetup(self):

        try:
            newList = self.selectListObj("customCtrl_GRP", "_CTR")
            #newList = cmds.listRelatives(newList, type="transform")
            #newList = cmds.listRelatives(newList, p=True)
        except:
            newList = []
        # print newList

        self.controlList.clear()
        if newList:
            newList = sorted(newList)
            print newList
            for list in newList:
                self.controlList.addItem("{0}".format(list))

            self.controlList.sizeHint()


    def onOkRefresh(self, message):
        print message + " w nowym oknie"
        self.controlListSetup()
        self.controlList.repaint()
        # allObj = cmds.ls(o=1)
        # if any(x == "facePosesMain_GRP" for x in allObj) == True:
        #self.tablePoseFill()
        #self.tableCorrectivesFill()
        #all = cmds.ls(o=1)
        #if any(x == "facePanel_GRP" for x in all) == True:
            #self.createPanleBTN.setDisabled(True)
        #else:
            #self.createPanleBTN.setEnabled(True)

    def allClickCtrlSetup(self):
        self.controlList.itemDoubleClicked.connect(self.selectCtrl)
        self.controlList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.addControl.clicked.connect(self.addCtrl)

    def addCtrl(self):
        print "jestem"
        self.createcustomCtrl()
        #self.controlListSetup()
        #self.controlList.repaint()
        self.onOkRefresh("add")


    def selectCtrl(self, item):
        cmds.select(str(item.text()), r=1)


    def softSelection(self):
        # Grab the soft selection
        selection = OpenMaya.MSelectionList()
        softSelection = OpenMaya.MRichSelection()
        OpenMaya.MGlobal.getRichSelection(softSelection)
        softSelection.getSelection(selection)

        dagPath = OpenMaya.MDagPath()
        component = OpenMaya.MObject()

        # Filter Defeats the purpose of the else statement
        iter = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMeshVertComponent)
        elements, weights = [], []
        nodes = []
        while not iter.isDone():
            iter.getDagPath(dagPath, component)
            dagPath.pop()  # Grab the parent of the shape node
            node = dagPath.fullPathName()
            if node not in nodes:
                nodes.append(node)
            fnComp = OpenMaya.MFnSingleIndexedComponent(component)
            getWeight = lambda i: fnComp.weight(i).influence() if fnComp.hasWeights() else 1.0

            for i in range(fnComp.elementCount()):
                elements.append('%s.vtx[%i]' % (node, fnComp.element(i)))
                weights.append(getWeight(i))
            iter.next()

        return elements, weights, nodes



    def makeCtrl(self, name):
            c1 = pm.circle(r=1, s=8, n="{}_CTR".format(name))[0]
            c2 = pm.circle(r=1, s=8, n="{}A_CTR".format(name))[0]
            c3 = pm.circle(r=1, s=8, n="{}B_CTR".format(name))[0]
            pm.parent(c2.getShape(), c1, s=1, r=1)
            pm.parent(c3.getShape(), c1, s=1, r=1)
            pm.delete(c2)
            pm.delete(c3)
            s = c1.getShape().split("_")
            pm.select("{}A_{}.cv[0:7]".format(s[0], s[1]), r=1)
            pm.rotate(0, 0, 90)
            pm.select("{}B_{}.cv[0:7]".format(s[0], s[1]), r=1)
            pm.rotate(0, 90, 0)
            pm.select(cl=1)
            return c1

    def connectPosOffset(self, parent, child):
        pmaNodePos = pm.createNode("plusMinusAverage", n="{}_PosPMA".format(parent))
        pm.setAttr("{}.operation".format(pmaNodePos), 2)
        pm.connectAttr("{}.translate".format(parent), "{}.input3D[0]".format(pmaNodePos))
        pm.disconnectAttr("{}.translate".format(parent), "{}.input3D[0]".format(pmaNodePos))
        pm.connectAttr("{}.translate".format(parent), "{}.input3D[1]".format(pmaNodePos))
        pm.connectAttr("{}.output3D".format(pmaNodePos), "{}.translate".format(child))

        pmaNodeRot = pm.createNode("plusMinusAverage", n="{}_RotPMA".format(parent))
        pm.setAttr("{}.operation".format(pmaNodePos), 2)
        pm.connectAttr("{}.rotate".format(parent), "{}.input3D[0]".format(pmaNodeRot))
        pm.disconnectAttr("{}.rotate".format(parent), "{}.input3D[0]".format(pmaNodeRot))
        pm.connectAttr("{}.rotate".format(parent), "{}.input3D[1]".format(pmaNodeRot))

        pm.connectAttr("{}.output3D".format(pmaNodeRot), "{}.rotate".format(child))




    def createLocatorFollicle(self):
        if not pm.core.pluginInfo("meshVertexPosition", q=True, l=True):
            pm.core.loadPlugin("meshVertexPosition")

        result = []
        vertexList = cmds.ls(sl=True, fl=True)
        solverList = {}
        for obj in vertexList:
            if ".vtx[" in obj:
                elements = obj.split(".")
                objName = elements[0]
                vertexID = int(elements[1].replace("vtx[", "").replace("]", ""))
                if objName not in solverList:
                    shapeName = cmds.listRelatives(objName, s=True)[0]
                    connections = cmds.listConnections(
                        shapeName + ".worldMesh[0]", type="meshVertexPosition")
                    if connections == None:
                        solverList[objName] = cmds.createNode("meshVertexPosition")
                        cmds.connectAttr(
                            shapeName + ".worldMesh[0]", solverList[objName] + ".inMesh")
                    else:
                        solverList[objName] = connections[0]
                        if 1 < len(connections):
                            cmds.warning("More than one meshVertexPosiotion node connected to " +
                                         objName + " causing useless computation. Please use only one node per a mesh")
                solverName = solverList[objName]
                newLocShape = cmds.createNode("locator")
                newLoc = cmds.listRelatives(newLocShape, p=True)[0]
                result.append(newLoc)
                cmds.setAttr(
                    solverName + ".index[" + str(vertexID) + "]", vertexID)
                cmds.connectAttr(
                    solverName + ".transformation[" + str(vertexID) + "].position", newLoc + ".translate")
                cmds.connectAttr(
                    solverName + ".transformation[" + str(vertexID) + "].rotation", newLoc + ".rotate")
        return result


    def connectetToNext(self, edge, edgeList, index, connectedList):
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

    def convertToCurve(self, edgesList):
        #edgesList = pm.ls(os=1)
        for edge in edgesList:
            if ":" in edge.split(".")[1]:
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
            print str(connectedList)
            print str(edge)
            #edgesCorrectList.append(egdge)

            connected = self.connectetToNext(edge, edgesList, edgesList.index(edge), connectedList)
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
        cmds.select(cl=1)
        curve = ""
        for edge in edgesCorrectList:
            if str(edge) not in "!!":
                print edge
                pm.select(edge, add=1)
            else:
                curve = mel.eval("polyToCurve -form 2 -degree 1;")
                cmds.select(cl=1)

        return curve


    def createcustomCtrl(self):

        #alphabet = list(string.ascii_uppercase)

        vertsList = pm.ls(sl=1)

        for vert in vertsList:
            mainObj = pm.PyNode(vert.split(".")[0])
            weightsList = self.softSelection()

            name = self.newControlName.toPlainText()

            check = cmds.ls("customCtrl_GRP")
            if check == []:
                    ctrlGrp = pm.group(em=True, name="customCtrl_GRP")
                    staticGRP = pm.group(em=True, name="staticSetup_GRP")
                    staticGeoGRP = pm.group(em=True, name="staticGeo_GRP")
                    pm.parent(staticGRP, ctrlGrp)
                    pm.parent(staticGeoGRP, ctrlGrp)
            else:
                    ctrlGrp = "customCtrl_GRP"
                    staticGRP = "staticSetup_GRP"

            offsetGrp = pm.group(em=True, name="{}_offset_GRP".format(name))
            vertPos = vert.getPosition(space="world")

            ctrl = self.makeCtrl(name)
            pm.parent(ctrl, ctrlGrp)
            ctrl.setTranslation(vertPos)
            pm.makeIdentity(ctrl, a=1)
            prtCns = pm.parentConstraint(ctrl, offsetGrp)
            pm.delete(prtCns)
            pm.parent(offsetGrp, ctrlGrp)
            mainJnt = pm.joint(n="{}MainJNT".format(name))
            pm.xform(mainJnt, ws=1, t=mainObj.getTranslation())
            duplikats = []
            for object in weightsList[2]:
                mesh = object #pm.PyNode(vert.split(".")[0].replace("Shape",""))
                duplikat = pm.duplicate(mesh, n="{}{}BLN".format(mesh, name))[0]
                pm.select(cl=1)
                pm.skinCluster(duplikat, mainJnt)
                pm.parent(duplikat, staticGeoGRP)
                duplikats.append(duplikat)
            #meshBlnVert = "{}.{}".format(pm.PyNode(duplikat).getShape(),vert.split(".")[1])
            #vertBln = pm.PyNode(meshBlnVert)
            edges = vert.connectedEdges()
            print edges
            e = pm.ls(edges, fl=1)
            curve = self.convertToCurve(e[:2])
            curveShape = pm.PyNode(curve[0]).getShape()
            print curveShape
            pm.disconnectAttr("{}.outputcurve".format(curve[1]), "{}.create".format(curveShape))
            pm.delete(curve[0])
            fallowNode = "{}_fallow".format(name)
            pm.rename(curve[1], fallowNode)
            nodePoc = pm.createNode("pointOnCurveInfo", n="{}POC".format(name))
            pm.setAttr("{}.parameter".format(nodePoc), 0.5)
            pm.connectAttr("{}.outputcurve".format(fallowNode), "{}.inputCurve".format(nodePoc))
            fallowLoc = self.createLocatorFollicle()
            fallowLoc = pm.rename(fallowLoc, "{}_fallowLoc".format(name))
            #pm.xform(fallowLoc, ws=1, t=vertPos)
            #pm.makeIdentity(fallowLoc, a=1)
            #pm.select(cl=1)
            jntBln = pm.joint(n="{}_blnJNT".format(name))
            pm.xform(jntBln, ws=1, t=vertPos)
            pm.parent(jntBln, fallowLoc)
            pm.parent(fallowLoc, staticGRP)

            self.connectPosOffset(fallowLoc, offsetGrp)
            #pm.connectAttr("{}.position".format(nodePoc), "{}.translate".format(offsetGrp))
            pm.parent(ctrl, offsetGrp)
            pm.makeIdentity(ctrl, a=1)
            #pm.connectAttr("{}.translate".format(ctrl), "{}.translate".format(fallowLoc))


            activeSkincluster = \
            pm.listConnections(pm.PyNode(duplikat).getShape(), type="skinCluster")[0]
            pm.skinCluster(activeSkincluster, e=1, wt=0, lw=1, ai=jntBln)
            pm.setAttr("{}.liw".format(jntBln), 0)
            for vert, w in zip(weightsList[0], weightsList[1]):
                    print vert, w
                    for duplikat in duplikats:
                        if duplikat in vert:
                            cmds.skinPercent(str(activeSkincluster), "{}.{}".format(duplikat,vert.split(".")[1]), transformValue=[(str(jntBln), w)])


if __name__ == "__main__":

    # Make sure the UI is deleted before recreating
    try:
        myWin.deleteLater()
    except:
        pass

    try:
        myWin = CucoMain(parent=maya_main_window())
        myWin.setWindowFlags(Qt.Window)
        myWin.show()
    except:
        traceback.print_exc()
        #myWin.deleteLater()


