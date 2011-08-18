#wombat 2011
# configuration
import os

#gets the working directory used for absolute paths
wd = os.getcwd()


#database engine and database name with location
DB_URI = 'sqlite:///wombatDatabase.db'
        
#debugging key
DEBUG = True
SECRET_KEY = 'development key'

#temporary username and password
USERNAME = 'admin'
PASSWORD = 'default'

#database name for explicit calls in functions
DATABASE = 'wombatDatabase.db'

#repository url default host: localhost
REPO_URL = 'http://localhost/svn/dummy'
LOCAL_REPO = wd +'/repository'

#first time users
FIRST_VIEW= False

#construction flag
CONSTRUCTION = True

#---------------------------Flask-Mail config-----------------------------------

MAIL_SERVER = 'Localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
#MAIL_DEBUG = app.debug
MAIL_USERNAME = None
MAIL_PASSWORD = None
DEFAULT_MAIL_SENDER = None
