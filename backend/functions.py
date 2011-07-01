#important functions

import os.path

img_inline = ['.gif', '.jpg', '.png']
image_exts = ['.bmp', '.gif', '.ico', '.jpg', '.png', '.psd',
        '.psp','.pspimage', '.psptube', '.raw', '.svg', '.tga', '.tif', '.xcf']
model_exts = ['.3dc', '.3ds', '.blend', '.caf', '.cal', '.cmf', '.crf', '.csf',
        '.dxf', '.emdl', '.lwo', '.max', '.md3', '.mdl', '.mesh', '.mtl',
        '.ndo', '.obj', '.skeleton', '.srf', '.texture', '.wings', '.wrl',
        '.xaf', '.xmf', '.xrl', '.xsf', '.xsi']
sound_exts = ['.mid', '.mp3', '.ogg', '.wav']
text_exts = ['.asm', '.bat', '.cfg', '.cg', '.conf', '.glsl', '.hlsl','.htm',
        '.html', '.ini', '.material', '.txt', '.url', '.xml']

def getType(name):
    """
    """
    base, ext = os.path.splitext(name)
    ext = ext.lower()

    if ext in image_exts:
        type = "image"
    elif ext in model_exts:
        type = "model"
    elif ext in sound_exts:
        type = "sound"
    elif ext in text_exts:
        type = "text"
    else:
        type = "other"

    return type
