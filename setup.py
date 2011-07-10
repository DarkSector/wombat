#setup the application the starting point to everything
import wombatdb
from wombat_config.config_file import REPO_URL,LOCAL_REPO
from backend.svnfunctions import SVNfunctions
#Create the database

svn = SVNfunctions()

wombatdb.init_db()
svn.checkout_repo(REPO_URL,LOCAL_REPO)
