#important functions
import os
#from wombat_config.config_file import DATABASE
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




class Base (object):
    def __init__(self):
                pass


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
            
            fileList = []
            fileSize = 0
            folderCount = 0
            #rootdir = '/home/darksector/Desktop' 
            rootdir = link

            for root, subFolders, files in os.walk(rootdir):
                    folderCount += len(subFolders)
                    for file in files:
                            f = os.path.join(root,file)
                            fileSize = fileSize + os.path.getsize(f)
                            #print(f)
                            fileList.append(f)

            #print("Total Size is {0} bytes".format(fileSize))
            #print fileSize
            #print fileList
            fileLength = len(fileList)
            #print len(fileList)
            #print folderCount
            return (fileSize,fileLength,folderCount)

    
    def convert_bytes(self,bytes):
            bytes = float(bytes)
            if bytes >= 1099511627776:
                    terabytes = bytes / 1099511627776
                    size = '%.2fT' % terabytes
            elif bytes >= 1073741824:
                    gigabytes = bytes / 1073741824
                    size = '%.2fG' % gigabytes
            elif bytes >= 1048576:
                    megabytes = bytes / 1048576
                    size = '%.2fM' % megabytes
            elif bytes >= 1024:
                    kilobytes = bytes / 1024
                    size = '%.2fK' % kilobytes
            else:
                    size = '%.2fb' % bytes
            return size
            
#def check_field(data,table):
    """ 
    Returns a boolean value after checking if data is present in the mentioned table
    Good for checking if username or email exists
    """
#    data = User.query.filter_by(data=)


#print DATABASE
