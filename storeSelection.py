import maya.cmds as cmds

stored_selection = []

def store_selection(*args):
    global stored_selection
    stored_selection = cmds.ls(selection=True)
    print("Stored Selection:", stored_selection)

def select_stored_items(*args):
    if stored_selection:
        cmds.select(stored_selection, add=True)
        print("Selected Stored Items:", stored_selection)
    else:
        cmds.warning("No items stored!")

def create_ui():
    if cmds.window("selectionUI", exists=True):
        cmds.deleteUI("selectionUI", window=True)
    window = cmds.window("selectionUI", title="Store and Select Items", widthHeight=(300, 100))
    cmds.columnLayout(adjustableColumn=True)
    cmds.button(label="Store Selected Items", command=store_selection)
    cmds.button(label="Select Stored Items", command=select_stored_items)

    cmds.showWindow(window)

create_ui()
