bl_info = {
    "name": "Angle UV Image Edit",
    "blender": (2, 80, 0),
    "category": "Edit",
}

#import subprocess
#import sys
#import os
 
#path to python.exe
#python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
#(python_exe)
 
# upgrade pip
#subprocess.call([python_exe, "-m", "ensurepip"])
#subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip", "--user"])
 
# install required packages
#subprocess.call([python_exe, "-m", "pip", "install", "Pillow", "--user"])

import bpy
from PIL import Image, ImageDraw
#FUNCTIONS
def RangeConvert(oldMin, oldMax, oldVal, newMin, newMax):
    return int((((oldVal - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin)

def ModifyImage(self, numShades, shadowHue, minBrightness, maxBrightness):
    #image = object.active_material.texture_paint_images[0]
    image = bpy.data.images[0]
    
    filepath = bpy.path.abspath(image.filepath, library=image.library)
    print("Filepath: " , filepath)
    image = Image.open(filepath)
    imageSizeX = int(image.size[0])
    imageSizeY = int(image.size[1])
    print("image info: ", image.format, image.size, image.mode)
    
    #Convert shadowhue to colors
    red = RangeConvert(0, 1, shadowHue.r, 0, 255)
    green = RangeConvert(0, 1, shadowHue.g, 0, 255)
    blue = RangeConvert(0, 1, shadowHue.b, 0, 255)
    alphaMin = RangeConvert(0, 100, 100 - maxBrightness, 0, 255)
    alphaMax = RangeConvert(0, 100, 100 - minBrightness, 0, 255)
    
    #Cut and resize
    cut = image.crop((0, 0, imageSizeX, imageSizeY))
    image = image.resize((imageSizeX * numShades, imageSizeY))
    print("image info 2: ", image.format, image.size, image.mode)
    
    #Paste hued version of cut
    for i in range(numShades):
        image.paste(cut, (i * imageSizeX, 0))
    
    overlay = Image.new('RGBA', image.size, 0)
    draw = ImageDraw.Draw(overlay)
    for i in range(numShades):
        currBrightness = minBrightness + i * ((maxBrightness - minBrightness) / numShades)
        alpha = RangeConvert(0, numShades, i, alphaMin, alphaMax)
        draw.rectangle([i * imageSizeX, 0, (i + 1) * imageSizeX, imageSizeY], fill=(red, green, blue, alpha))
    image = Image.alpha_composite(image, overlay)
    image.save(filepath)
    
    
#CLASS
class PrebakeLightingImage(bpy.types.Operator):
    """Prebakes object lighting based on parameters"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "image.prebake_lighting_image"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Angle-Based Prebake Lighting: Set Image"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    #Inputs
    numShades = bpy.props.IntProperty(
        name = "Number of Shades:",
        description = "Number of different shades to prebake.",
        default = 5,
        min = 1,
        max = 100)
    
    shadowHue = bpy.props.FloatVectorProperty(name='Shadow Hue:',subtype='COLOR',default=(0.5,0.5,0.9))
    
    minSaturation = bpy.props.IntProperty(
        name = "Min Saturation:",
        description = "Saturation of darkest areas, 0 full saturation, 100 no saturation",
        default = 30,
        min = 0,
        max = 100)
        
    maxSaturation = bpy.props.IntProperty(
        name = "Max Saturation:",
        description = "Saturation of lightest areas, 0 full saturation, 100 no saturation",
        default = 70,
        min = 0,
        max = 100)
    
    #Allows Window
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 300)
    
    #EXECUTE
    def execute(self, context):        # execute() is called when running the operator.
        #bpy.ops.object.editmode_toggle()
        #for obj in context.selected_objects:
        ModifyImage(self, self.numShades, self.shadowHue, self.minSaturation, self.maxSaturation)
        bpy.ops.image.reload()
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.


def menu_func(self, context):
    self.layout.operator(PrebakeLighting.bl_idname)

def register():
    bpy.utils.register_class(PrebakeLightingImage)
    bpy.types.IMAGE_MT_image.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(PrebakeLighting)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()