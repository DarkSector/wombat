import os
import pysvn
from functions import Base

func = Base()

class SVNfunctions:
    def __init__(self, path):
        self.path = path
        self.client = pysvn.Client()
        
    def checkout_repo(self,link,local_link):
        self.client.checkout(link,local_link)

    def update_copy(self):
        self.client.update(self.path)

    def get_url(self):
        entry = self.client.info(self.path)
        return entry.url

    def get_dir_content(self,updated_link):
        entry_list = self.client.ls('.')
        return entry_list

    def get_revision_no(self):
        rev_no = self.client.info(self.path).revision.number
        return rev_no
        
    def get_info(self, filePath):
        fullPath = os.path.join(self.path, filePath)
        entries = self.client.info2(fullPath, recurse=False)
        
        infoDict = {}
        
        for p, i in entries:
            for k in i:
                infoDict[k] = i[k]
                
        return infoDict
        
    def get_dir_info(self, path):
        items = self.client.ls(os.path.join(self.path, path))
        
        items = [str(os.path.basename(i['name'])) for i in items]

        listing = []    
        
        for i in items:
            objectInfo = {}
            
            if i == ".svn":
                continue
                
            fullPath = os.path.join(self.path, path, i)
            relativePath = os.path.join(path, i)
            
            fileType = func.getType(i)

            if fileType == "other":
                if os.path.isdir(fullPath):
                    fileType = "directory"
                elif os.path.isfile(fullPath):
                    fileType = "unknown"
        
            objectInfo['name'] = i
            objectInfo['fileType'] = fileType
            objectInfo['path'] = "/" + relativePath
            objectInfo['svndetails'] = self.get_info(relativePath)
            
            listing.append(objectInfo)
        
        return listing
        
        
        
