import maya.cmds as cmds

def set_selected_controls_color(color_index):
    """Set the color of selected controls."""
    selected_controls = cmds.ls(selection=True)
    
    if not selected_controls:
        cmds.warning("No controls selected. Please select NURBS curves.")
        return
    
    for control in selected_controls:
        if cmds.objectType(control) == "transform":
            shape_nodes = cmds.listRelatives(control, shapes=True, fullPath=True) or []
            for shape_node in shape_nodes:
                enable_color_override(shape_node)
                set_control_color(shape_node, color_index)
        else:
            enable_color_override(control)
            set_control_color(control, color_index)

def enable_color_override(control):
    """Enable the color override for a specific control."""
    try:
        cmds.setAttr(f"{control}.overrideEnabled", 1)
    except RuntimeError as e:
        cmds.warning(f"Failed to enable color override for {control}: {e}")

def set_control_color(control, color_index):
    """Set the color override for a specific control."""
    try:
        cmds.setAttr(f"{control}.overrideColor", color_index)
    except RuntimeError as e:
        cmds.warning(f"Failed to set color for {control}: {e}")

def apply_color(color_slider, color_display):
    """Apply the selected color to the controls."""
    color_index = cmds.intSliderGrp(color_slider, query=True, value=True)
    set_selected_controls_color(color_index)
    cmds.colorSliderGrp(color_display, edit=True, rgb=cmds.colorIndex(color_index, q=True))

def update_color_display(color_slider, color_display, event):
    """Update the color display as the user slides the color_slider."""
    color_index = cmds.intSliderGrp(color_slider, query=True, value=True)
    cmds.colorSliderGrp(color_display, edit=True, rgb=cmds.colorIndex(color_index, q=True))

def create_color_picker_ui():
    """Create a UI with a stepped slider for color picking."""
    if cmds.window("colorPickerUI", exists=True):
        cmds.deleteUI("colorPickerUI", window=True)

    window = cmds.window("colorPickerUI", title="Color Picker UI", sizeable=True, widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)

    # Valid color indices for color override
    valid_color_indices = list(range(32))

    # Create stepped slider for color picking
    color_slider = cmds.intSliderGrp(label="Pick a Color", field=True, minValue=1, maxValue=31, value=0, step=1, fieldMinValue=1, fieldMaxValue=31,
                                     dragCommand=lambda x: update_color_display(color_slider, color_display, x))

    # Create color display
    color_display = cmds.colorSliderGrp(label="Selected Color", rgb=(0, 0, 0))

    # Create apply button
    apply_button = cmds.button(label="Apply Color", command=lambda x: apply_color(color_slider, color_display))

    cmds.showWindow(window)

# Run the UI creation function
create_color_picker_ui()
