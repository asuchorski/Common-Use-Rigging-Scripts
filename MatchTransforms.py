import maya.cmds as cmds

def match_transformations():
    # Get the selected objects
    selection = cmds.ls(selection=True)
    
    # Check if exactly two objects are selected
    if len(selection) != 2:
        cmds.error("Please select exactly two objects.")
        return

    # The first selected object (source)
    source = selection[0]
    # The second selected object (target)
    target = selection[1]
    
    # Get the world-space transformation matrix of the target object
    target_matrix = cmds.xform(target, query=True, matrix=True, worldSpace=True)
    
    # Apply the world-space transformation matrix to the source object
    cmds.xform(source, matrix=target_matrix, worldSpace=True)

    # Match pivots
    target_pivot = cmds.xform(target, query=True, rotatePivot=True, worldSpace=True)
    source_pivot = cmds.xform(source, query=True, rotatePivot=True, worldSpace=True)
    
    offset = [target_pivot[i] - source_pivot[i] for i in range(3)]
    
    cmds.xform(source, worldSpace=True, translation=offset, relative=True)

    print(f"Matched {source} transformations to {target}.")

# Run the function
match_transformations()
