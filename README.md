# Blender Baked Lighting
An addon for blender to bake lighting based on an angle. Written in Python.

## Usage:
First prep the UV Map in Blender's image editor using Tools -> Angle Based Lighting: Image
Set the number of shades you desire and the shadow color. This will create an altered UV with many darkened images corresponding to the number of shades.

Next, in the model editor, use Tools -> Angle Based Lighting: Model
Set the **same** number of shades and lighting angles to apply the UV based on the lighting angle.
