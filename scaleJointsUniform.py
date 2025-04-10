import maya.cmds as mc
JointList = mc.ls(type='joint')
for j in JointList:
    mc.setAttr('%s.segmentScaleCompensate'%(j),0)