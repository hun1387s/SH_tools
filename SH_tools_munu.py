from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import os
import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.mel as mel
import pymel.core as pm

import SH_script as SH
import SH_rename as SH_re
import SH_sort_Attr as SH_attr
reload(SH)
reload(SH_re)
reload(SH_attr)


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    # main_window_ptr = omui.MQtUtil.mainWindow()
    # return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    return pm.MelGlobals()['gMainWindow']

class DesignerUI(QtWidgets.QDialog):

    def __init__(self, parent=pm.MelGlobals()['gMainWindow']):
        super(DesignerUI, self).__init__(parent)

        self.setWindowTitle("SH Rig tools")
        self.setMinimumWidth(350)
        self.setMaximumWidth(350)
        self.setMinimumHeight(550)
        self.setMaximumHeight(550)

        self.init_ui()
        # layout = QtWidgets.QGridLayout()
        # layout.addWidget(self.ui.SH_UI_tab)

        self.riggingTab_connections()
        self.renameTab_connections()
        self.colorTab_connections()
        self.optimizeTab_connections()

    def init_ui(self):
        try:
            _path = os.path.dirname(os.path.abspath(__file__))
        except:
            _path = "/backup/dept/rig/users/Sanghun/maya/CustomUI"
        print(_path)

        f = QtCore.QFile("%s/SH_UI.ui" % _path)
        f.open(QtCore.QFile.ReadOnly)

        # f = QtCore.QFile("C:\code\maya\CustomUI\SH_UI.ui")
        # f.open(QtCore.QFile.ReadOnly)



        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f, parentWidget=self)

        f.close()

    def colorTab_connections(self):
        self.ui.color_Btn01.clicked.connect(lambda: SH.overrideColor(0))
        self.ui.color_Btn02.clicked.connect(lambda: SH.overrideColor(1))
        self.ui.color_Btn03.clicked.connect(lambda: SH.overrideColor(2))
        self.ui.color_Btn04.clicked.connect(lambda: SH.overrideColor(3))
        self.ui.color_Btn05.clicked.connect(lambda: SH.overrideColor(4))
        self.ui.color_Btn06.clicked.connect(lambda: SH.overrideColor(5))
        self.ui.color_Btn07.clicked.connect(lambda: SH.overrideColor(6))
        self.ui.color_Btn08.clicked.connect(lambda: SH.overrideColor(7))
        self.ui.color_Btn09.clicked.connect(lambda: SH.overrideColor(8))
        self.ui.color_Btn10.clicked.connect(lambda: SH.overrideColor(9))
        self.ui.color_Btn11.clicked.connect(lambda: SH.overrideColor(10))
        self.ui.color_Btn12.clicked.connect(lambda: SH.overrideColor(11))
        self.ui.color_Btn13.clicked.connect(lambda: SH.overrideColor(12))
        self.ui.color_Btn14.clicked.connect(lambda: SH.overrideColor(13))
        self.ui.color_Btn15.clicked.connect(lambda: SH.overrideColor(14))
        self.ui.color_Btn16.clicked.connect(lambda: SH.overrideColor(15))
        self.ui.color_Btn17.clicked.connect(lambda: SH.overrideColor(16))
        self.ui.color_Btn18.clicked.connect(lambda: SH.overrideColor(17))
        self.ui.color_Btn19.clicked.connect(lambda: SH.overrideColor(18))
        self.ui.color_Btn20.clicked.connect(lambda: SH.overrideColor(19))
        self.ui.color_Btn21.clicked.connect(lambda: SH.overrideColor(20))
        self.ui.color_Btn22.clicked.connect(lambda: SH.overrideColor(21))
        self.ui.color_Btn23.clicked.connect(lambda: SH.overrideColor(22))
        self.ui.color_Btn24.clicked.connect(lambda: SH.overrideColor(23))
        self.ui.color_Btn25.clicked.connect(lambda: SH.overrideColor(24))
        self.ui.color_Btn26.clicked.connect(lambda: SH.overrideColor(25))
        self.ui.color_Btn27.clicked.connect(lambda: SH.overrideColor(26))
        self.ui.color_Btn28.clicked.connect(lambda: SH.overrideColor(27))
        self.ui.color_Btn29.clicked.connect(lambda: SH.overrideColor(28))
        self.ui.color_Btn30.clicked.connect(lambda: SH.overrideColor(29))
        self.ui.color_Btn31.clicked.connect(lambda: SH.overrideColor(30))
        self.ui.color_Btn32.clicked.connect(lambda: SH.overrideColor(31))

        self.ui.Discolor_Btn.clicked.connect(lambda: SH.overrideDisabled())


    def riggingTab_connections(self):
        # pass
        # self.ui.cancelButton.clicked.connect(self.close)
        self.ui.hierarchy_btn.clicked.connect(lambda : SH.hierarchy())
        self.ui.snap_btn.clicked.connect(self.Snap_connection)
        self.ui.vertexFollice_btn.clicked.connect(lambda: SH.vertexFollice())
        self.ui.DLA_on_btn.clicked.connect(lambda: SH.LRA_onoff(1))
        self.ui.DLA_off_btn.clicked.connect(lambda: SH.LRA_onoff(0))
        self.ui.Jnt_on_btn.clicked.connect(lambda: SH.visible_joint(1))
        self.ui.Jnt_off_btn.clicked.connect(lambda: SH.visible_joint(0))
        self.ui.parent_btn.clicked.connect(self.parentCmd_connection)
        self.ui.centerJnt_btn.clicked.connect(self.CenterJnt_connection)
        self.ui.vertexJnt_btn.clicked.connect(lambda: SH.componentToJoint())
        self.ui.freezeJnt_btn.clicked.connect(lambda: SH.FreezeJnt())
        self.ui.preRig_btn.clicked.connect(lambda: SH.preRig())
        self.ui.copybone_bnt.clicked.connect(self.copySkinBone_connection)
        self.ui.blend_btn.clicked.connect(self.BlendTRS_connection)
        # self.ui.MatrixConst_btn.clicked.connect(self.MatrixConst_connection)

        self.ui.FKsize_pushButton.clicked.connect(self.FkCtrl_connection)
        self.ui.BoxCtrl_pushButton.clicked.connect(self.BoxCtrl_connection)
        self.ui.PinCtrl_pushButton.clicked.connect(self.PinCtrl_connection)
        self.ui.offGrp_btn.clicked.connect(self.offGrp_connection)
        self.ui.JntStyle_btn.clicked.connect(self.JntDrawStyle_connection)
        self.ui.JntDiv_btn.clicked.connect(self.JntDivide_connection)

        self.ui.hierarchy_btn.setToolTip(SH.hierarchy.__doc__)
        self.ui.snap_btn.setToolTip(SH.snap.__doc__)
        self.ui.vertexFollice_btn.setToolTip(SH.vertexFollice.__doc__)
        self.ui.DLA_on_btn.setToolTip(SH.LRA_onoff.__doc__)
        self.ui.DLA_off_btn.setToolTip(SH.LRA_onoff.__doc__)
        self.ui.Jnt_on_btn.setToolTip(SH.visible_joint.__doc__)
        self.ui.Jnt_off_btn.setToolTip(SH.visible_joint.__doc__)
        self.ui.parent_btn.setToolTip(SH.parentCmd.__doc__)
        self.ui.centerJnt_btn.setToolTip(SH.centerJoint.__doc__)
        self.ui.vertexJnt_btn.setToolTip(SH.componentToJoint.__doc__)
        self.ui.freezeJnt_btn.setToolTip(SH.FreezeJnt.__doc__)
        self.ui.preRig_btn.setToolTip(SH.preRig.__doc__)
        self.ui.copybone_bnt.setToolTip(SH.copySkinBone.__doc__)
        self.ui.blend_btn.setToolTip(SH.blendTransRotScale.__doc__)
        # self.ui.MatrixConst_btn.setToolTip(SH.matrixConstraint.__doc__)

        self.ui.FKsize_pushButton.setToolTip(SH.createFKCtrl.__doc__)
        self.ui.BoxCtrl_pushButton.setToolTip(SH.createBoxCTRL.__doc__)
        self.ui.PinCtrl_pushButton.setToolTip(SH.createPinCTRL.__doc__)

    # def MatrixConst_connection(self):
    #     SH.matrixConstraint()
    #     className = 'SH.matrixConstraint()'
    #     mel.callLastCommand("""python(\"%s\")""" % className)
    def Snap_connection(self):
        SH.snap()
        cmds.repeatLast(addCommand='python("import SH_script;SH_script.snap();")')

    def parentCmd_connection(self):
        SH.parentCmd()
        cmds.repeatLast(addCommnad='python("import SH_script;SH_script.parentCmd();")')

    def CenterJnt_connection(self):
        SH.centerJoint()
        cmds.repeatLast(addCommand='python("import SH_script;SH_script.centerJoint();")')

    def BlendTRS_connection(self):
        SH.blendTransRotScale()
        cmds.repeatLast(addCommand='python("import SH_script;SH_script.blendTransRotScale();")')

    def JntDivide_connection(self):
        divideVar = self.ui.JntDiv_lineEdit.text()
        SH.jointDivde(divideVar)
        cmds.repeatLast(addCommand='python("import SH_script;SH_script.jointDivde(SH_ui.ui.JntDiv_lineEdit.text());")')

    def JntDrawStyle_connection(self):
        varText = self.ui.JntStyle_comboBox.currentText()
        print("PinCtrl size %s" % varText)
        SH.joint_drawStyle_set2(varText)
        cmds.repeatLast(addCommand='python("import SH_script;SH_script.joint_drawStyle_set2(SH_ui.ui.JntStyle_comboBox.currentText());")')

    def copySkinBone_connection(self):
        SH.copySkinBone()
        cmds.repeatLast(addCommand='python("import SH_script;SH_script.copySkinBone();")')

    def offGrp_connection(self):
        _suffix = self.ui.offGrp_lineEdit.text()
        SH.suffixOffGrp(_suffix)
        cmds.repeatLast(addCommand='python("import SH_script;SH_script.suffixOffGrp(SH_ui.ui.offGrp_lineEdit.text());")')

    def PinCtrl_connection(self):
        _radius = self.ui.pinbox_lineEdit.text()
        print("PinCtrl size %s" % _radius)
        SH.createPinCTRL(_radius)
        cmds.repeatLast(addCommand='python("import SH_script;SH_script.createPinCTRL(SH_ui.ui.pinbox_lineEdit.text());")')

    def BoxCtrl_connection(self):
        _radius = self.ui.pinbox_lineEdit.text()
        print("BoxCtrl size %s" % _radius)
        SH.createBoxCTRL(_radius)
        cmds.repeatLast(addCommand='python("import SH_script;SH_script.createBoxCTRL(SH_ui.ui.pinbox_lineEdit.text());")')

    def FkCtrl_connection(self):
        _radius = self.ui.FKSize_lineEdit.text()

        print("FkCtrl size %s" %_radius)
        if self.ui.FKX_radioButton.isChecked():
            print("FK aim X")
            SH.createFKCtrl(1, _radius)
            cmds.repeatLast(addCommand='python("import SH_script;SH_script.createFKCtrl(1,SH_ui.ui.FKX_radioButton.isChecked());")')
        elif self.ui.FKY_radioButton.isChecked():
            print("FK aim Y")
            SH.createFKCtrl(2, _radius)
            cmds.repeatLast(addCommand='python("import SH_script;SH_script.createFKCtrl(2,SH_ui.ui.FKX_radioButton.isChecked());")')
        elif self.ui.FKZ_radioButton.isChecked():
            print("FK aim Z")
            SH.createFKCtrl(3, _radius)
            cmds.repeatLast(addCommand='python("import SH_script;SH_script.createFKCtrl(3,SH_ui.ui.FKX_radioButton.isChecked());")')



    def renameTab_connections(self):
        self.ui.rename_btn.clicked.connect(self.rename_connect)
        self.ui.replace_btn.clicked.connect(self.replace_connect)
        self.ui.prefix_btn.clicked.connect(self.prefix_connect)
        self.ui.suffix_btn.clicked.connect(self.suffix_connect)
        self.ui.hierarchy2_btn.clicked.connect(SH.hierarchy)

    def rename_connect(self):
        rename1Var = self.ui.rename1_lineEdit.text()
        rename1_1Var = self.ui.rename1_1_lineEdit.text()
        rename2Var = self.ui.rename2_lineEdit.text()
        renameCombo = self.ui.rename_comboBox.currentText()
        SH_re.rename_script(rename1Var, rename1_1Var, renameCombo, rename2Var, )

    def replace_connect(self):
        replace1Var = self.ui.replace1_lineEdit.text()
        replace2Var = self.ui.replace2_lineEdit.text()
        SH_re.replace_script(replace1Var, replace2Var)

    def prefix_connect(self):
        prefixVal = self.ui.prefix_lineEdit.text()
        SH_re.prefix_script(prefixVal)

    def suffix_connect(self):
        suffixVar = self.ui.suffix_lineEdit.text()
        SH_re.suffix_script(suffixVar)

    def optimizeTab_connections(self):
        self.ui.deleteKey_btn.clicked.connect(lambda: SH.delete_keyFrame())
        self.ui.deleteVirus_btn.clicked.connect(lambda: SH.delete_china_virus())
        self.ui.deleteUnkown_btn.clicked.connect(lambda: SH.delete_unknown())
        self.ui.deleteUnused_btn.clicked.connect(lambda: SH.delete_unused())
        self.ui.VisHis_btn.clicked.connect(lambda: SH.visible_history(1))
        self.ui.invisHis_btn.clicked.connect(lambda: SH.visible_history(0))

        self.ui.cutAttr_btn.clicked.connect(lambda: SH_attr.cut_attribute())
        self.ui.copyAttr_btn.clicked.connect(lambda: SH_attr.copy_attribute())
        self.ui.pasteAttr_btn.clicked.connect(lambda: SH_attr.paste_attribute())
        self.ui.divideAttr_btn.clicked.connect(lambda: SH_attr.add_divider_attribute())
        self.ui.upAttr_btn.clicked.connect(lambda: SH_attr.move_up_attribute())
        self.ui.dnAttr_btn.clicked.connect(lambda: SH_attr.move_down_attribute())




    def create_layout(self):
        pass
        # self.ui.layout().setContentsMargins(6, 6, 6, 6)





if __name__ == "__main__":

    try:
        SH_ui.close() # pylint: disable=E0601
        SH_ui.deleteLater()
    except:
        pass

    SH_ui = DesignerUI()
    SH_ui.show()

