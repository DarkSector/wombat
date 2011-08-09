import bcrypt
import wombat

class LocalFunctions ():
    
    def hashPassword(self,unhashed):
        hashed = bcrypt.hashpw(unhashed,gensalt())
        
