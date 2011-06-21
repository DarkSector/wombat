#!BPY
"""
Name: 'Screenshot Taker'
Blender: 242
Group: 'Export'
Tooltip: 'MAWM'
"""

import Blender

from Blender import *

from Blender.Scene import Render

import math

def getSceneObject(scn, obName):
	for ob in scn.objects:
		if ob.name == obName:
			return ob
	return None

scn = Scene.GetCurrent()

context = scn.getRenderingContext()

print context.getRenderWinSize()

context.setRenderWinSize(25)

cube = getSceneObject(scn, "Cube")

for i in range(0, 18):
	cube.RotX = math.radians(i * 10)

	for j in range(0, 36):
		cube.RotZ = math.radians(j * 10)
		context.render()
		context.saveRenderedImage("foo" + str(i) + str(j))


