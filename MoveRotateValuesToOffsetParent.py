import maya.cmds as cmds
import math

def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)

def euler_to_matrix(rotation):
    rx, ry, rz = map(degrees_to_radians, rotation)
    
    cx = math.cos(rx)
    sx = math.sin(rx)
    cy = math.cos(ry)
    sy = math.sin(ry)
    cz = math.cos(rz)
    sz = math.sin(rz)

    # Calculate the rotation matrix
    matrix = [
        [cy * cz, -cy * sz, sy, 0],
        [sx * sy * cz + cx * sz, cx * cz - sx * sy * sz, -sx * cy, 0],
        [-cx * sy * cz + sx * sz, sx * cz + cx * sy * sz, cx * cy, 0],
        [0, 0, 0, 1]
    ]
    
    return matrix

def set_rotation_in_offset_matrix():
    # Ensure an object is selected
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("Please select an object.")
        return
    
    position = cmds.xform(selected_objects, query=True, worldSpace=True, translation=True)
        
    # Create a locator
    locator = cmds.spaceLocator(name="tempOPMloc")
        
    # Move the locator to the position of the selected object
    cmds.xform(locator, worldSpace=True, translation=position)
    
    obj = selected_objects[0]
    
    # Get the rotation values of the object and multiply by -1
    rotation = [-val for val in cmds.getAttr(obj + '.rotate')[0]]
    
    # Convert the rotation values to a matrix
    rotation_matrix = euler_to_matrix(rotation)
    
    # Get the current parent offset matrix
    offset_matrix = cmds.getAttr(obj + '.offsetParentMatrix')
    
    # Create a new offset matrix with the rotation values
    new_matrix = list(offset_matrix)
    
    for i in range(3):
        for j in range(3):
            new_matrix[i*4 + j] = rotation_matrix[i][j]
    
    # Set the new offset matrix
    cmds.setAttr(obj + '.offsetParentMatrix', *new_matrix, type='matrix')
        
    # Move back to temp locator
    cmds.select(selected_objects)
    cmds.select(locator, add=True)
    
    selection = cmds.ls(selection=True)
    
    source = selection[0]
    target = selection[1]
    
    target_matrix = cmds.xform(target, query=True, matrix=True, worldSpace=True)
    
    # Apply the world-space transformation matrix to the source object
    cmds.xform(source, matrix=target_matrix, worldSpace=True)

    # Match pivots
    target_pivot = cmds.xform(target, query=True, rotatePivot=True, worldSpace=True)
    source_pivot = cmds.xform(source, query=True, rotatePivot=True, worldSpace=True)
    
    offset = [target_pivot[i] - source_pivot[i] for i in range(3)]
    
    cmds.xform(source, worldSpace=True, translation=offset, relative=True)

    # Freeze transformations
    cmds.makeIdentity(obj, apply=True, rotate=True, translate=True)
    
    cmds.delete(locator)
    
    print(f"Set rotation {rotation} into offset parent matrix of {obj} and froze transformations.")

# Run the function immediately
set_rotation_in_offset_matrix()
