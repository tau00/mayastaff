import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

#CREATE BASE DISTANCE TABLE
obj = pm.ls(sl=1)[0]
print obj
vtxNum = pm.polyEvaluate(obj, v=1)
print vtxNum
baseDistanceList = []
cmds.currentTime(0, edit=True)
gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
cmds.progressBar(gMainProgressBar,
                 edit=True,
                 beginProgress=True,
                 isInterruptable=True,
                 status='Generate Base Distance',
                 maxValue=vtxNum)

for i in range(0, vtxNum):
    if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True):
        break
    else:
        conVtxsList = obj.getShape().vtx[i].connectedVertices()
        #print conVtxsList

        tempList = {}
        tempList.clear()

        pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(0.0, 0.0, 1.0))
        for conVtx in conVtxsList:
            distance = obj.getShape().vtx[int(i)].getPosition(space="world").distanceTo(
                obj.getShape().vtx[int(conVtx.name().split("[")[1].replace("]",""))].getPosition(space="world"))
            #tempList.append("{}:{}:{}".format(i, conVtx.name().split("[")[1].replace("]",""), distance))
            tempList.update({conVtx.name().split("[")[1].replace("]", ""):"{}:{}".format(i, distance)})

        baseDistanceList.append(tempList)

    cmds.progressBar(gMainProgressBar, edit=True, step=1)
cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)

print baseDistanceList


#CREATE COLOR BASE ON BASE DISTANCE TABLE COMPARE TO ACTUAL DISTANCE

frame = 250
for f in range(0, frame):
    cmds.currentTime(f, edit=True)
tempList = []
distanceVal = []
obj = pm.ls(sl=1)[0]
vtxNum = pm.polyEvaluate(obj, v=1)
print vtxNum
gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
cmds.progressBar(gMainProgressBar,
                 edit=True,
                 beginProgress=True,
                 isInterruptable=True,
                 status='Generate Heat Map',
                 maxValue=vtxNum)

obj = pm.ls(sl=1)[0]
vtxNum = pm.polyEvaluate(obj, v=1)
#print vtxNum

for i in range(0, vtxNum):
    if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True):
        break
    else:
        conVtxsList = obj.getShape().vtx[i].connectedVertices()
        tempList[:] = []
        distanceVal[:] = []
        baseDistance = 0
        for conVtx in conVtxsList:
            distance = obj.getShape().vtx[int(i)].getPosition(space="world").distanceTo(
                obj.getShape().vtx[int(conVtx.name().split("[")[1].replace("]", ""))].getPosition(space="world"))
            #print int(conVtx.name().split("[")[1].replace("]", ""))
            baseDistance =float(baseDistanceList[i][str(conVtx.name().split("[")[1].replace("]", ""))].split(":")[1])
            #print "dostanca: ", float(baseDistance) - float(distance)
            distanceVal.append((float(distance) - float(baseDistance)))
            print distanceVal
        avarge = round(sum(distanceVal)/len(distanceVal), 8)
        print avarge
        vsp = 0

        if avarge == baseDistance:
            pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(0.0, 0.0, 1.0))
        elif avarge < baseDistance:
            vsp = avarge/baseDistance / 2
            pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(vsp, vsp, 1.0))
        elif avarge > baseDistance:
            vsp = avarge/baseDistance / 2
            pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(vsp, vsp/2, 0.0))

        #pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(0.0, 0.0, 1.0))
    #cmds.setAttr("polyColorPerVertex1.vertexColor[{}].vertexColorRGB".format(i),
                 #0.0, 0.0, 1.0, type="double3")

    cmds.progressBar(gMainProgressBar, edit=True, step=1)
cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)




for i in range(0, vtxNum):
    pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(0.0, 0.5, 0.0))

print pm.distanceDimension( sp=obj.getShape().vtx[194].getPosition(space="world"), ep=obj.getShape().vtx[170].getPosition(space="world") )
print obj.getShape().vtx[194].getPosition(space="world").distanceTo(obj.getShape().vtx[170].getPosition(space="world"))
tedt = obj.getShape().vtx[194].connectedVertices()
for t in tedt:
    print t.name().split("[")[1].replace("]","")

cmds.setAttr("vtxColoreyeBrowCR_M_Shape_CTR.vertexColor[0].vertexColorRGB",
             0.0, 0.0, 1.0, type="double3")
 #
 # for vt in range(0, vertsNum):
 #            vertIfno = cmds.polyInfo("{0}.vtx[{1}]".format(nameuiBoxButton[0], vt), vf=True)
 #            newList = filter(None, vertIfno[0].split(" "))
 #            cmds.connectAttr("{0}.output".format(multiDivideName),"{0}.vertexColor[{1}].vertexFaceColor[{2}].vertexFaceColorRGB".format(vtxColorName, vt,newList[2]))




#!!!!!!!!!!!!!!!!!!!!!!!!VER2!!!!!!!!!!!!!


import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

#CREATE BASE DISTANCE TABLE
obj = pm.ls(sl=1)[0]
print obj
vtxNum = pm.polyEvaluate(obj, v=1)
print vtxNum
baseDistanceList = []
cmds.currentTime(0, edit=True)
gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
cmds.progressBar(gMainProgressBar,
                 edit=True,
                 beginProgress=True,
                 isInterruptable=True,
                 status='Generate Base Distance',
                 maxValue=vtxNum)

for i in range(0, vtxNum):
    if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True):
        break
    else:
        conVtxsList = obj.getShape().vtx[i].connectedVertices()
        #print conVtxsList

        tempList = {}
        tempList.clear()

        pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(0.0, 0.0, 1.0))
        for conVtx in conVtxsList:
            distance = obj.getShape().vtx[int(i)].getPosition(space="world").distanceTo(
                obj.getShape().vtx[int(conVtx.name().split("[")[1].replace("]",""))].getPosition(space="world"))
            #tempList.append("{}:{}:{}".format(i, conVtx.name().split("[")[1].replace("]",""), distance))
            tempList.update({conVtx.name().split("[")[1].replace("]", ""):"{}:{}".format(i, distance)})

        baseDistanceList.append(tempList)

    cmds.progressBar(gMainProgressBar, edit=True, step=1)
cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)

print baseDistanceList


#CREATE COLOR BASE ON BASE DISTANCE TABLE COMPARE TO ACTUAL DISTANCE

frame = 250
for f in range(0, frame):
    cmds.currentTime(f, edit=True)
tempList = []
distanceVal = []
obj = pm.ls(sl=1)[0]
vtxNum = pm.polyEvaluate(obj, v=1)
print vtxNum
gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
cmds.progressBar(gMainProgressBar,
                 edit=True,
                 beginProgress=True,
                 isInterruptable=True,
                 status='Generate Heat Map',
                 maxValue=vtxNum)

obj = pm.ls(sl=1)[0]
vtxNum = pm.polyEvaluate(obj, v=1)
#print vtxNum

for i in range(0, vtxNum):
    if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True):
        break
    else:
        conVtxsList = obj.getShape().vtx[i].connectedVertices()
        tempList[:] = []
        distanceVal[:] = []
        baseDistance = 0
        for conVtx in conVtxsList:
            distance = obj.getShape().vtx[int(i)].getPosition(space="world").distanceTo(
                obj.getShape().vtx[int(conVtx.name().split("[")[1].replace("]", ""))].getPosition(space="world"))
            #print int(conVtx.name().split("[")[1].replace("]", ""))
            baseDistance =float(baseDistanceList[i][str(conVtx.name().split("[")[1].replace("]", ""))].split(":")[1])
            #print "dostanca: ", float(baseDistance) - float(distance)
            distanceVal.append((float(distance) - float(baseDistance)))
            print distanceVal
        avarge = round(sum(distanceVal)/len(distanceVal), 8)
        print avarge
        vsp = 0

        if avarge == baseDistance:
            pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(0.0, 0.0, 1.0))
        elif avarge < baseDistance:
            vsp = avarge/baseDistance / 2
            pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(vsp, vsp, 1.0))
        elif avarge > baseDistance:
            vsp = avarge/baseDistance / 2
            pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(vsp, vsp/2, 0.0))

        #pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(0.0, 0.0, 1.0))
    #cmds.setAttr("polyColorPerVertex1.vertexColor[{}].vertexColorRGB".format(i),
                 #0.0, 0.0, 1.0, type="double3")

    cmds.progressBar(gMainProgressBar, edit=True, step=1)
cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)




for i in range(0, vtxNum):
    pm.polyColorPerVertex("{}.vtx[{}]".format(obj, i), rgb=(0.0, 0.5, 0.0))

print pm.distanceDimension( sp=obj.getShape().vtx[194].getPosition(space="world"), ep=obj.getShape().vtx[170].getPosition(space="world") )
print obj.getShape().vtx[194].getPosition(space="world").distanceTo(obj.getShape().vtx[170].getPosition(space="world"))
tedt = obj.getShape().vtx[194].connectedVertices()
for t in tedt:
    print t.name().split("[")[1].replace("]","")

cmds.setAttr("vtxColoreyeBrowCR_M_Shape_CTR.vertexColor[0].vertexColorRGB",
             0.0, 0.0, 1.0, type="double3")
 #