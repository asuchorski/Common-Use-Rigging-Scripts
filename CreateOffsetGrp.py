import maya.cmds as cmds

def add_offset_group():
    # Get the selected objects
    selection = cmds.ls(selection=True)
    
    # Check if exactly one object is selected
    if len(selection) != 1:
        cmds.error("Please select exactly one control.")
        return
    # Create new group and parent 
    control = selection[0]
    offset_group = cmds.group(empty=True, name=control + '_OffsetGrp')
    cmds.parent(control, offset_group)
    
    # Zero out the group's transformations to match the control's current transform and pivots
    cmds.setAttr(offset_group + ".translate", 0, 0, 0)
    cmds.setAttr(offset_group + ".rotate", 0, 0, 0)
    cmds.setAttr(offset_group + ".scale", 1, 1, 1)
    control_pivot_translation = cmds.xform(control, query=True, rotatePivot=True, worldSpace=True)
    cmds.xform(offset_group, worldSpace=True, pivots=control_pivot_translation)

add_offset_group()