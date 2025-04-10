from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
import shiboken2
import maya.OpenMayaUI as omui

def get_maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)

class JointSubdividerUI(QtWidgets.QDialog):
    def __init__(self, parent=get_maya_main_window()):
        super(JointSubdividerUI, self).__init__(parent)
        self.setWindowTitle("Subdivide Joint Chain")
        self.setMinimumSize(450, 200)
        self.setWindowFlags(QtCore.Qt.Window)  # Allows minimize, resize, etc.

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.num_joints_label = QtWidgets.QLabel("Joints to insert:")
        self.num_joints_spin = QtWidgets.QSpinBox()
        self.num_joints_spin.setMinimum(1)
        self.num_joints_spin.setValue(2)

        self.radius_label = QtWidgets.QLabel("Joint Radius:")
        self.radius_spin = QtWidgets.QDoubleSpinBox()
        self.radius_spin.setDecimals(2)
        self.radius_spin.setMinimum(0.01)
        self.radius_spin.setValue(1.0)

        self.color_label = QtWidgets.QLabel("Joint Color (RGB):")
        self.color_btn = QtWidgets.QPushButton("Pick Color")
        self.color_display = QtWidgets.QLabel()
        self.color_display.setFixedSize(40, 20)
        self.color = QtGui.QColor(255, 255, 255)
        self.update_color_display()

        self.apply_btn = QtWidgets.QPushButton("Subdivide")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.num_joints_label, self.num_joints_spin)
        form_layout.addRow(self.radius_label, self.radius_spin)

        color_layout = QtWidgets.QHBoxLayout()
        color_layout.addWidget(self.color_btn)
        color_layout.addWidget(self.color_display)
        form_layout.addRow(self.color_label, color_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.apply_btn)

    def create_connections(self):
        self.color_btn.clicked.connect(self.pick_color)
        self.apply_btn.clicked.connect(self.on_apply)

    def pick_color(self):
        new_color = QtWidgets.QColorDialog.getColor(initial=self.color, parent=self)
        if new_color.isValid():
            self.color = new_color
            self.update_color_display()

    def update_color_display(self):
        pixmap = QtGui.QPixmap(40, 20)
        pixmap.fill(self.color)
        self.color_display.setPixmap(pixmap)

    def on_apply(self):
        num_joints = self.num_joints_spin.value()
        radius = self.radius_spin.value()
        rgb = [self.color.redF(), self.color.greenF(), self.color.blueF()]
        main_subdivision_logic(num_joints, radius, rgb)

def apply_radius_and_color(joint, radius, color_rgb):
    cmds.setAttr(f"{joint}.radius", radius)
    cmds.setAttr(f"{joint}.overrideEnabled", 1)
    cmds.setAttr(f"{joint}.overrideRGBColors", 1)
    cmds.setAttr(f"{joint}.overrideColorRGB", *color_rgb)

def subdivide_joint_chain(joints, num_joints_to_insert, radius, color_rgb):
    new_joints = []

    # Apply to first joint
    apply_radius_and_color(joints[0], radius, color_rgb)

    for i in range(len(joints) - 1):
        start_joint = joints[i]
        end_joint = joints[i + 1]

        start_pos = cmds.xform(start_joint, query=True, worldSpace=True, translation=True)
        end_pos = cmds.xform(end_joint, query=True, worldSpace=True, translation=True)

        inserted_joints = []
        for j in range(1, num_joints_to_insert + 1):
            t = j / (num_joints_to_insert + 1)
            new_pos = [(1 - t) * start_pos[k] + t * end_pos[k] for k in range(3)]

            new_joint = cmds.joint(position=new_pos)
            apply_radius_and_color(new_joint, radius, color_rgb)

            inserted_joints.append(new_joint)
            new_joints.append(new_joint)

        cmds.parent(end_joint, inserted_joints[-1])

    # Apply to last joint
    apply_radius_and_color(joints[-1], radius, color_rgb)

    return new_joints

def main_subdivision_logic(num_joints_to_insert, radius, color_rgb):
    selected_joints = cmds.ls(selection=True, type='joint')
    if not selected_joints:
        cmds.warning("Please select the root joint of the joint chain.")
        return

    joint_chain = cmds.listRelatives(selected_joints[0], allDescendents=True, type='joint') or []
    joint_chain.append(selected_joints[0])
    joint_chain.reverse()

    subdivide_joint_chain(joint_chain, num_joints_to_insert, radius, color_rgb)
    cmds.select(clear=True)
    print("Joint chain subdivided successfully.")

def show_ui():
    try:
        for widget in QtWidgets.QApplication.allWidgets():
            if isinstance(widget, JointSubdividerUI):
                widget.close()
    except:
        pass
    ui = JointSubdividerUI()
    ui.show()

show_ui()
