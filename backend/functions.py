#important functions
import os
from wombat_config.config_file import DATABASE
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



class Base:
    def getType(self,name):
        """
        returns the type of file. Example return image if the extension of the file is anything
        in the image_exts like .jpg .png .gif etc.
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

    def get_info(self,link):
		import os
		fileList = []
		fileSize = 0
		folderCount = 0
		rootdir = link
		
		for root, subFolders, files in os.walk(rootdir):
		    folderCount += len(subFolders)
		    for file in files:
		        f = os.path.join(root,file)
		        fileSize = fileSize + os.path.getsize(f)
		        #print(f)
		        fileList.append(f)
		
		
		
		fileSize2 = (fileSize / (1024 * 1024) )
		("Total Size is {0} bytes".format(fileSize2))
		#print fileList
		print("Total Files ", len(fileList))
		print("Total Folders ", folderCount)

#def check_field(data,table):
    """ 
    Returns a boolean value after checking if data is present in the mentioned table
    Good for checking if username or email exists
    """
#    data = User.query.filter_by(data=)


#print DATABASE
