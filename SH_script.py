# -*- coding: utf-8
"""
22.09.05 - "visible_history" 함수 수정 : "groupParts", "groupId" 노드는 제외
"""

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import pymel.core as pm
import math
import maya.OpenMaya as om
import maya.mel as mel

class UndoContext(object):
    def __enter__(self):
        pm.undoInfo(openChunk=True)
    def __exit__(self, *exc_info):
        pm.undoInfo(closeChunk=True)

def hierarchy():
    """
    Select all objects hierarchy from the selected object are selected.
    """
    cmds.select(hierarchy=True)
    print(cmds.ls(sl=1))


def snap():
    """
    Apply the translate and rotate of the first selected object to the second selected object.
    """
    with UndoContext():
        selobj = cmds.ls(sl=1)
        cmds.delete(cmds.parentConstraint(selobj[0], selobj[1], weight=1))
        print("Snap [%s] to [%s]"%(selobj[0],selobj[1]))




# Display Local Axis onOFF
def LRA_onoff(num):
    """
    Turn On and Off DLA of the selected object.
    """
    with UndoContext():
        selObj = cmds.ls(selection=1, flatten=1)

        for sel in selObj:
            cmds.setAttr(sel + ".displayLocalAxis", num)

        if num == 0:
            print("Display Local Axis [" + sel + "] Off")
        else:
            print("Display Local Axis [" + sel + "] On")


# toggle visibility joint
def visible_joint(num):
    """
    Turn On and Off visible of the selected joint.
    """
    with UndoContext():
        _panel = cmds.getPanel(type='modelPanel')

        for _var in _panel:
            cmds.modelEditor(_var, e=True, joints=num)

        if num == 0:
            print("Joint Visible Off")
        else:
            print("Joint Visible On")


# centerJoint
def centerJoint():
    """
    Create a joint in the center of the selected objects.
    """
    with UndoContext():
        newCluster = cmds.cluster(envelope=1)
        cmds.select(clear=True)
        newJoint = cmds.joint(p=(0, 0, 0))
        cmds.delete(cmds.parentConstraint(newCluster, newJoint, weight=1))
        cmds.delete(newCluster)
        print("Create Joint [" + newJoint + "]")


# parnetCommand
def parentCmd():
    """
    Parenting the selected object one by one.
    """
    with UndoContext():
        selObj = cmds.ls(selection=True)
        numList = range(0, len(selObj))
        numList.reverse()
        for num in numList:
            if num > 0:
                cmds.parent(selObj[num - 1], selObj[num])
                print("parent [{0}] - [{1}]".format(selObj[num - 1], selObj[num]))

# vertex Joint
def componentToJoint():
    """
    Create joints of the selected vertex.
    """
    with UndoContext():
        def getSelection():
            components = cmds.ls(sl=1)
            selList = []
            objName = components[0][0:components[0].index(".")]
            # go through every component in the list. If it is a single component ("pCube1.vtx[1]"), add it to the list. Else,
            # add each component in the index ("pCube1.vtx[1:5]") to the list
            for c in components:
                if ":" not in c:
                    selList.append(c)
                else:
                    print(c)
                    startComponent = int(c[c.index("[") + 1: c.index(":")])
                    endComponent = int(c[c.index(":") + 1:c.index("]")])
                    componentType = c[c.index(".") + 1:c.index("[")]
                    while startComponent <= endComponent:
                        selList.append(objName + "." + componentType + "[" + str(startComponent) + "]")
                        startComponent += 1

            return selList

        if cmds.objectType(cmds.ls(sl=1)[0]) != "mesh":
            return
        # return the selection as a list
        selList = getSelection()
        print(selList)
        componentType = selList[0][selList[0].index(".") + 1:selList[0].index("[")]
        componentCenters = []
        # if you selected a face or edge, make our joints at those component's centers
        if componentType == "f" or componentType == "e":
            for c in selList:
                p = cmds.xform(c, q=1, t=1, ws=1)
                # find the average of all our x,y,z points. That's our center
                componentCenters.append([sum(p[0::3]) / len(p[0::3]),
                                         sum(p[1::3]) / len(p[1::3]),
                                         sum(p[2::3]) / len(p[2::3])])
                for loc in componentCenters:
                    cmds.select(cl=1)
                    cmds.joint(n="joint#", p=loc, rad=.25)

        # else make a joint at the location of each vertex
        else:
            for c in selList:
                cmds.select(cl=1)
                # make a joint at the position of each selected vertex
                cmds.joint(n="joint#", p=cmds.pointPosition(c), rad=.25)
        cmds.select(cl=1)



# Freeze jnt
def FreezeJnt():
    """
    Freeze joints of the selected joint.
    """
    with UndoContext():
        def pushRot2JointOrient(skinedJoints=[]):
            for skinedJnt in skinedJoints:
                skinedJnt = pm.PyNode(skinedJnt)
                mMatrix = skinedJnt.getMatrix(os=1)
                mTransformMtx = om.MTransformationMatrix(mMatrix)
                eulerRot = mTransformMtx.eulerRotation()
                angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]

                # Convert rotate into orient of skined Joint or Constrainted
                pm.setAttr(skinedJnt + '.rx', 0)
                pm.setAttr(skinedJnt + '.ry', 0)
                pm.setAttr(skinedJnt + '.rz', 0)
                pm.setAttr(skinedJnt + '.jo', angles)

                print("FreezeJnt [ " + skinedJnt + " ]")

        selList = cmds.ls(sl=1, type='joint')
        pushRot2JointOrient(selList)


# preRig
def preRig():
    """
    Create a joint in the center of the selected objects.
    """
    with UndoContext():
        def preRig_core(curSel):
            shapeList = pm.listRelatives(curSel, shapes=1)
            shapeList_filted = []
            skinClusterList = []
            for _shape in shapeList:
                history = pm.listHistory(_shape)
                for _node in history:
                    print(_node)
                    result = pm.ls(_node, type='skinCluster')

                    if result:
                        # get shapeList
                        shapeList_filted.append(_shape)
                        # get skinCluster
                        skinClusterList.append(result[0])

            jointSkinList = []

            for _skinCluster in skinClusterList:
                _joints = pm.skinCluster(_skinCluster, query=True, influence=True)
                for _jnt in _joints:
                    data = (_jnt, _skinCluster)
                    jointSkinList.append(data)

            # set Prebind
            def get_connectedSkinMtxAt(searchJoint, skinData):
                resultList = []
                for dest in pm.listConnections(searchJoint, destination=1, p=1):
                    if skinData + '.matrix' in str(dest):
                        resultList.append(dest)

                return resultList

            # set preBindPose
            for _jnt, _skin in jointSkinList:
                print('Target Jnt : [%s]' % _jnt)
                print('Target SC : [%s]' % _skin)

                MtxAt = get_connectedSkinMtxAt(_jnt, _skin)[0]
                print(MtxAt)

                bindMtxAt = pm.PyNode(MtxAt.replace('matrix', 'bindPreMatrix'))

                # get worldInverseMatrix[0] of joints
                ivsMtx = pm.getAttr(_jnt + '.worldInverseMatrix[0]')
                pm.setAttr(bindMtxAt, ivsMtx, type='matrix')

            print('finally done.')

        selobj = pm.ls(selection=1, type='transform')

        for _obj in selobj:
            preRig_core(_obj)


# creatFKCtrl Command
def createFKCtrl(part,_radius):
    """
    Create circle shapes in the selected objects.
    """
    with UndoContext():
        selObj = cmds.ls(selection=1, type='transform')

        # _radius = cmds.textField(size_textFieldVar, q=1, text=1)

        if part == 1:
            _selAim = (1, 0, 0)
            print("X")
        elif part == 2:
            _selAim = (0, 1, 0)
            print("Y")
        elif part == 3:
            _selAim = (0, 0, 1)
            print("Z")

        for jntNum in selObj:
            curName = str(jntNum) + "_"
            newCurve = cmds.circle(n=curName, center=(0, 0, 0), normal=_selAim, radius=_radius)
            shapeList = cmds.listRelatives(newCurve, shapes=True)
            cmds.parent(shapeList, jntNum, relative=True, shape=True)
            cmds.delete(newCurve)
            print(shapeList)


def createPinCTRL(_radius):
    """
    Create sphere shapes in the selected objects.
    """
    with UndoContext():
        selObj = cmds.ls(selection=1, type='transform')

        # _scale = cmds.textField(pinsize_textFieldVar, q=1, text=1)

        for jntNum in selObj:
            curName = str(jntNum) + "_"
            newCurve = mel.eval(
                'curve -d 1 -p 0 1 0 -p 0 0.92388 0.382683 -p 0 0.707107 0.707107 -p 0 0.382683 0.92388 -p 0 0 1 -p 0 -0.382683 0.92388 -p 0 -0.707107 0.707107 -p 0 -0.92388 0.382683 -p 0 -1 0 -p 0 -0.92388 -0.382683 -p 0 -0.707107 -0.707107 -p 0 -0.382683 -0.92388 -p 0 0 -1 -p 0 0.382683 -0.92388 -p 0 0.707107 -0.707107 -p 0 0.92388 -0.382683 -p 0 1 0 -p 0.382683 0.92388 0 -p 0.707107 0.707107 0 -p 0.92388 0.382683 0 -p 1 0 0 -p 0.92388 -0.382683 0 -p 0.707107 -0.707107 0 -p 0.382683 -0.92388 0 -p 0 -1 0 -p -0.382683 -0.92388 0 -p -0.707107 -0.707107 0 -p -0.92388 -0.382683 0 -p -1 0 0 -p -0.92388 0.382683 0 -p -0.707107 0.707107 0 -p -0.382683 0.92388 0 -p 0 1 0 -p 0 0.92388 -0.382683 -p 0 0.707107 -0.707107 -p 0 0.382683 -0.92388 -p 0 0 -1 -p -0.382683 0 -0.92388 -p -0.707107 0 -0.707107 -p -0.92388 0 -0.382683 -p -1 0 0 -p -0.92388 0 0.382683 -p -0.707107 0 0.707107 -p -0.382683 0 0.92388 -p 0 0 1 -p 0.382683 0 0.92388 -p 0.707107 0 0.707107 -p 0.92388 0 0.382683 -p 1 0 0 -p 0.92388 0 -0.382683 -p 0.707107 0 -0.707107 -p 0.382683 0 -0.92388 -p 0 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -n "Sphere Ctrl";')
            cmds.setAttr(newCurve + '.scaleX', float(_radius))
            cmds.setAttr(newCurve + '.scaleY', float(_radius))
            cmds.setAttr(newCurve + '.scaleZ', float(_radius))
            cmds.makeIdentity(apply=True, s=1)

            shapeList = cmds.listRelatives(newCurve, shapes=True)
            shapeList = cmds.rename(shapeList, curName + 'Shape')
            cmds.parent(shapeList, jntNum, relative=True, shape=True)
            cmds.delete(newCurve)


def createBoxCTRL(_radius):
    """
    Create box shapes in the selected objects.
    """
    with UndoContext():
        selObj = cmds.ls(selection=1, type='transform')

        # _scale = cmds.textField(pinsize_textFieldVar, q=1, text=1)

        for jntNum in selObj:
            curName = str(jntNum) + "_"
            newCurve = mel.eval('curve -d 1 -p 0.5 0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -n "Cube Ctrl" ;')
            cmds.setAttr(newCurve + '.scaleX', float(_radius) * 1)
            cmds.setAttr(newCurve + '.scaleY', float(_radius) * 1)
            cmds.setAttr(newCurve + '.scaleZ', float(_radius) * 1)
            cmds.makeIdentity(apply=True, s=1)

            shapeList = cmds.listRelatives(newCurve, shapes=True)
            shapeList = cmds.rename(shapeList, curName + 'Shape')
            cmds.parent(shapeList, jntNum, relative=True, shape=True)
            cmds.delete(newCurve)



# Blend rot, trans, scale
def blendTransRotScale():
    """
    Connect blend node and IK FK Set
    The order of select : IK, FK, Set
    """
    with UndoContext():
        seljnt = cmds.ls(selection=1, type='joint')

        ### trnaslate blend ###
        selTransBlend = cmds.createNode('blendColors', name=seljnt[0] + '_' + seljnt[1] + '_translateBlend')

        cmds.connectAttr(seljnt[0] + '.translate', selTransBlend + '.color1')
        cmds.connectAttr(seljnt[1] + '.translate', selTransBlend + '.color2')
        cmds.connectAttr(selTransBlend + '.output', seljnt[2] + '.translate')

        ### rotate blend ###
        selRotBlend = cmds.createNode('blendColors', name=seljnt[0] + '_' + seljnt[1] + '_rotateBlend')

        cmds.connectAttr(seljnt[0] + '.rotate', selRotBlend + '.color1')
        cmds.connectAttr(seljnt[1] + '.rotate', selRotBlend + '.color2')
        cmds.connectAttr(selRotBlend + '.output', seljnt[2] + '.rotate')

        ### scale blend ###
        selScaleBlend = cmds.createNode('blendColors', name=seljnt[0] + '_' + seljnt[1] + '_scaleBlend')

        cmds.connectAttr(seljnt[0] + '.scale', selScaleBlend + '.color1')
        cmds.connectAttr(seljnt[1] + '.scale', selScaleBlend + '.color2')
        cmds.connectAttr(selScaleBlend + '.output', seljnt[2] + '.scale')


# Offset GRP
def suffixOffGrp(suffix):
    """
    Create OffsetGrp and add Prefix name
    """
    with UndoContext():
        def offGrp_core_UI(target):
            print("Suffix [%s]" % suffix)
            # parent object part
            print('target %s' % target)
            print(target)
            parentobj = cmds.listRelatives(target, parent=1)
            print('parentobj')
            print(parentobj)

            # snap part
            _offGrp = cmds.group(em=True, name=target + suffix)
            cmds.delete(cmds.parentConstraint(target, _offGrp))

            # parenting
            if parentobj: cmds.parent(_offGrp, parentobj[0])
            cmds.parent(target, _offGrp)

        selList = cmds.ls(sl=1)
        print('selList')
        print(selList)
        for target in selList:
            offGrp_core_UI(target)


def joint_drawStyle_set2(target):
    with UndoContext():
        _jnt = cmds.ls(selection=1, type='joint')
        # jointNum = cmds.optionMenu(joint_draw_Menu, query=1, value=1)

        if 'Bone' in target:
            drawStyile = 0

        elif 'Multi' in target:
            drawStyile = 1

        elif 'None' in target:
            drawStyile = 2

        for _var in _jnt:
            cmds.setAttr(_var + ".drawStyle", drawStyile)

            print("Draw style set " + target + "[" + _var + "]")


# def copySkinBone():
#     with UndoContext():
#         selobj = cmds.ls(selection=1, type='transform')
#         # get Shape
#         # get Shape : filter
#         before_shapeList = cmds.listRelatives(selobj[0], shapes=1)
#         shapeList_filted = []
#         for _shape in before_shapeList:
#             result = cmds.listConnections(_shape, source=True, type='skinCluster')
#             # [u'skinCluster8']
#             # []
#             if result:
#                 shapeList_filted.append(_shape)
#
#         # get skinCluster
#         skinClusterList = []
#         for _shape in shapeList_filted:
#             result = cmds.listConnections(_shape, source=True, type='skinCluster')
#             skinClusterList.extend(result)
#
#         # get Joints
#         # jointSkinList => [ (joint1, skinCluster), .... ]
#         jointSkinList = []
#
#         for _skinCluster in skinClusterList:
#             _joints = cmds.skinCluster(_skinCluster, query=True, influence=True)
#             for _jnt in _joints:
#                 jointSkinList.append(_jnt)
#
#         cmds.skinCluster(jointSkinList, selobj[1], toSelectedBones=1)
#
#         after_shapeList = cmds.listRelatives(selobj[1], shapes=1)
#         after_shapeList_filted = []
#         for _shape in after_shapeList:
#             result = cmds.listConnections(_shape, source=True, type='skinCluster')
#             # [u'skinCluster8']
#             # []
#             if result:
#                 after_shapeList_filted.append(_shape)
#
#         # get skinCluster
#         after_skinClusterList = []
#         for _shape in after_shapeList_filted:
#             result = cmds.listConnections(_shape, source=True, type='skinCluster')
#             after_skinClusterList.extend(result)
#
#         # Sometimes skin weights wouldn't be copied exactly. So this should be excuted more than one time.
#         # cmds.copySkinWeights(selobj[0], selobj[1], influenceAssociation='name', surfaceAssociation='closestPoint')
#         cmds.copySkinWeights(ss=skinClusterList[0], ds=after_skinClusterList[0], noMirror=True, influenceAssociation='name', surfaceAssociation='closestPoint')
#         cmds.copySkinWeights(ss=skinClusterList[0], ds=after_skinClusterList[0], noMirror=True, influenceAssociation='name', surfaceAssociation='closestPoint')
#         cmds.copySkinWeights(ss=skinClusterList[0], ds=after_skinClusterList[0], noMirror=True, influenceAssociation='name', surfaceAssociation='closestPoint')
#         cmds.copySkinWeights(ss=skinClusterList[0], ds=after_skinClusterList[0], noMirror=True, influenceAssociation='name', surfaceAssociation='closestPoint')
#
#         cmds.select(selobj)
#         mel.eval('CopySkinWeights;')
#

def copySkinBone():
    selobj = pm.ls(selection=1, type='transform')
    # get Shape
    # get Shape : filter
    before_shapeList = pm.listRelatives(selobj[0], shapes=1)
    shapeList_filted = []
    for _shape in before_shapeList:
        result = pm.listConnections(_shape, source=True, type='skinCluster')
        # [u'skinCluster8']
        # []
        if result:
            shapeList_filted.append(_shape)

    # get skinCluster
    skinClusterList = []
    for _shape in shapeList_filted:
        # result = pm.listConnections(_shape, source=True, type='skinCluster')
        result = pm.listHistory(_shape, type='skinCluster')
        skinClusterList.extend(result)

    # get Joints
    # jointSkinList => [ (joint1, skinCluster), .... ]
    jointSkinList = []

    for _skinCluster in skinClusterList:
        _joints = pm.skinCluster(_skinCluster, query=True, influence=True)
        for _jnt in _joints:
            jointSkinList.append(_jnt)

    pm.skinCluster(jointSkinList, selobj[1], toSelectedBones=1)

    after_shapeList = pm.listRelatives(selobj[1], shapes=1)
    after_shapeList_filted = []
    for _shape in after_shapeList:
        result = pm.listConnections(_shape, source=True, type='skinCluster')
        # [u'skinCluster8']
        # []
        if result:
            after_shapeList_filted.append(_shape)

    # get skinCluster
    after_skinClusterList = []
    for _shape in after_shapeList_filted:
        result = pm.listConnections(_shape, source=True, type='skinCluster')
        after_skinClusterList.extend(result)

    # Sometimes skin weights wouldn't be copied exactly. So this should be excuted more than one time.
    # pm.copySkinWeights(selobj[0], selobj[1], influenceAssociation='name', surfaceAssociation='closestPoint')
    pm.copySkinWeights(ss=skinClusterList[0], ds=after_skinClusterList[0], noMirror=True, influenceAssociation='name', surfaceAssociation='closestPoint')
    pm.copySkinWeights(ss=skinClusterList[0], ds=after_skinClusterList[0], noMirror=True, influenceAssociation='name', surfaceAssociation='closestPoint')
    pm.copySkinWeights(ss=skinClusterList[0], ds=after_skinClusterList[0], noMirror=True, influenceAssociation='name', surfaceAssociation='closestPoint')
    pm.copySkinWeights(ss=skinClusterList[0], ds=after_skinClusterList[0], noMirror=True, influenceAssociation='name', surfaceAssociation='closestPoint')

    pm.select(selobj)
    mel.eval('CopySkinWeights;')
    pm.select(selobj)


def jointDivde(num):
    with UndoContext():
        divideNum = int(num)
        selobj = cmds.ls(sl = 1)
        baseXLength = cmds.getAttr(selobj[1] + ".translateX")
        baseYLength = cmds.getAttr(selobj[1] + ".translateY")
        baseZLength = cmds.getAttr(selobj[1] + ".translateZ")
        divideXLength = baseXLength / (divideNum - 1)
        divideYLength = baseYLength / (divideNum - 1)
        divideZLength = baseZLength / (divideNum - 1)


        JntVar = []
        for _num in range(divideNum-2):
            print(_num)
            dupJnt = cmds.duplicate(selobj[1])
            print(dupJnt)

            if not JntVar:
                pass
            else:
                cmds.parent(dupJnt, JntVar[-1])

            JntVar.append(dupJnt[0])

            cmds.setAttr(dupJnt[0] + ".translateX", divideXLength)
            cmds.setAttr(dupJnt[0] + ".translateY", divideYLength)
            cmds.setAttr(dupJnt[0] + ".translateZ", divideZLength)

    cmds.parent(selobj[1], JntVar[-1])


def delete_unknown():
    """Delete unknown node"""
    print(cmds.ls(type="unknown"))
    cmds.delete(cmds.ls(type="unknown"))

def delete_unused():
    """Delete unused node"""
    mel.eval('MLdeleteUnused;')

# delete Keyframe
def delete_keyFrame():
    """Delete keyFrame node"""
    with UndoContext():
        animKeyNode = []
        animKeyNode = animKeyNode + cmds.ls(type='animCurveTL')
        animKeyNode = animKeyNode + cmds.ls(type='animCurveTA')
        animKeyNode = animKeyNode + cmds.ls(type='animCurveTU')

        for _node in animKeyNode:
            cmds.delete(_node)

            print('Delete Succese [' + _node + ']')


# delete china virus
def delete_china_virus():
    """Delete China virus"""
    with UndoContext():
        jobs = cmds.scriptJob(lj=True)
        for job in jobs:
            if "leukocyte.antivirus()" in job:
                id = job.split(":")[0]
                if id.isdigit():
                    cmds.scriptJob(k=int(id), f=True)

        script_nodes = cmds.ls("vaccine_gene", type="script")
        script_nodes = script_nodes + cmds.ls("breed_gene", type="script")
        if script_nodes:
            cmds.delete(script_nodes)

def visible_history(num):
    """
    Turn On and Off ChannelBox history of all nodes.
    """
    with UndoContext():
        nodeList = cmds.ls()
        for _node in nodeList:
            if cmds.nodeType(_node) != "groupParts":
                if cmds.nodeType(_node) != "groupId":
                    cmds.setAttr('%s.isHistoricallyInteresting' % _node, num)


def overrideColor(colorNum):
    """
    Select color able overrideColor of selected objects
    """
    with UndoContext():
        selobj = cmds.ls(sl=1)
        for _obj in selobj:

            # selobj_shp = []
            selobj_shp = cmds.listRelatives(_obj, fullPath=0, shapes=1)
            print(selobj_shp)

            if selobj_shp == [None]:

                overrideValue = cmds.getAttr("%s.overrideEnabled" % _obj)

                if overrideValue == 0:
                    cmds.setAttr("%s.overrideEnabled" % _obj, 1)
                    cmds.setAttr("%s.overrideRGBColors" % _obj, 1)

                cmds.setAttr("%s.overrideColor" % _obj, colorNum)

            else:
                for _shp in selobj_shp:
                    print(_shp)
                    overrideValue = cmds.getAttr("%s.overrideEnabled" % _shp)

                    if overrideValue == 0:
                        cmds.setAttr("%s.overrideEnabled" % _shp, 1)

                    cmds.setAttr("%s.overrideRGBColors" % _shp, 0)
                    cmds.setAttr("%s.overrideColor" % _shp, colorNum)

def overrideDisabled():
    """
    Disable overrideColor of selected objects
    """
    with UndoContext():
        selobj = cmds.ls(sl=1)
        for _obj in selobj:
            selobj_shp = cmds.listRelatives(_obj, fullPath=1, shapes=1)

            for _shp in selobj_shp:
                cmds.setAttr("%s.overrideEnabled" % _shp, 0)


def vertexFollice():
    """Create Follicle as vertex position"""
    with UndoContext():
        selobj = pm.ls(sl=1, fl=1)

        mel.eval('ConvertSelectionToUVs')

        selUV = pm.ls(sl=1, fl=1)

        if not 'FollicleGrp' in pm.ls():
            FollicleGrp = pm.group(name = 'FollicleGrp', em = 1, world = 1)

        else:
            FollicleGrp = 'FollicleGrp'

        for _uv, num in zip(selUV, range(0, len(selUV))):
            # _uv = selUV[0]
            buffer = []
            # _token = mel.eval('tokenize %s "." %s'%(_uv, buffer))
            buffer = _uv.split(".")

            _shp = buffer[0]
            _flcShp = pm.createNode("follicle", name = "%s_follicle%s"%(_shp,num))
            _flc = pm.listRelatives(_flcShp, parent =1)[0]

            ## poly vs nurbs
            if pm.attributeQuery("outMesh", node = _shp, exists =1):
                print("Create Follicle at Mesh")
                pm.connectAttr("%s.outMesh"%_shp, "%s.inputMesh"%_flcShp, force =1 )
                _uvPos = pm.polyEditUV(_uv, query=1)

            elif pm.attributeQuery("local", node = _shp, exists =1):
                print("Create Follicle at Nurbs")
                pm.connectAttr("%s.outMesh" % _shp, "%s.inputMesh" % _flcShp, force=1)
                _uvPos = pm.polyEditUV(_uv, query=1)
                _size = len(_uvPos)


            pm.connectAttr("%s.worldMatrix"%_shp, "%s.inputWorldMatrix"%_flcShp, force = 1)
            pm.connectAttr("%s.outTranslate"%_flcShp, "%s.translate"%_flc, force = 1)
            pm.connectAttr("%s.outRotate"%_flcShp, "%s.rotate"%_flc, force = 1)

            pm.setAttr("%s.parameterU"%_flcShp, _uvPos[0], lock =1 )
            pm.setAttr("%s.parameterV"%_flcShp, _uvPos[1], lock =1 )

            # clean up Grp
            pm.parent(_flc, FollicleGrp)

def matrixConstraint():
    """Connect select obj as MatrixConstraint"""
    with UndoContext():
        def multiplyMatrices(matrix1, matrix2):
            return om.MMatrix().setToProduct(matrix1, matrix2)

        def getDagPath(obj):
            Msel = om.MSelectionList()  # create "cmds.ls(sl = 1)" array
            Msel.add(obj)
            DagPath = Msel.getDagPath(0)
            return DagPath

        obj = cmds.ls(sl=1)
        if not len(obj) >= 2:
            print('Target list was empty or contained no valid targets')
            return 0
        elif len(obj) == 2:
            sou = obj[0]
            tar = obj[-1]
            if not cmds.attributeQuery('offsetAttr', n=tar, exists=1) == 1:
                cmds.addAttr(tar, ln='offsetAttr', at='matrix')

            souM = getDagPath(sou)
            tarM = getDagPath(tar)
            offsetM = multiplyMatrices(tarM.inclusiveMatrix(), souM.inclusiveMatrix().inverse())
            cmds.setAttr('%s.offsetAttr' % tar, offsetM, type='matrix')
            if not cmds.ls('%s_MConstraint' % tar):
                mulM = cmds.shadingNode('multMatrix', asUtility=1, n='%s_MConstraint' % tar)
                cmds.connectAttr('%s.offsetAttr' % tar, '%s.matrixIn[0]' % mulM);
                cmds.connectAttr('%s.worldMatrix[0]' % sou, '%s.matrixIn[1]' % mulM)
                cmds.connectAttr('%s.parentInverseMatrix[0]' % tar, '%s.matrixIn[2]' % mulM)
                decomM = cmds.shadingNode('decomposeMatrix', asUtility=1, n='%s_DCM' % tar);
                cmds.connectAttr('%s.matrixSum' % mulM, '%s.inputMatrix' % decomM);

                cmds.connectAttr('%s.outputTranslate' % decomM, '%s.translate' % tar);
                cmds.connectAttr('%s.outputRotate' % decomM, '%s.rotate' % tar);
                cmds.connectAttr('%s.outputScale' % decomM, '%s.scale' % tar);
