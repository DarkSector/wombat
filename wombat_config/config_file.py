#wombat 2011
# configuration
import os
wd = os.getcwd()
DB_URI = 'sqlite:///wombatDatabase.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
DATABASE = 'wombatDatabase.db'
REPO_URL = 'http://localhost/svn/dummy'
LOCAL_REPO = wd +'/repository'
