import pysvn
import os
#import errno

client = pysvn.Client()

HOME_VAR = os.environ['HOME']
REPO_VAR = HOME_VAR + "/wombat_repo/"
#try:
#    os.makedirs(REPO_VAR)
#except OSError, e:
#    if e.errno != errno.EEXIST:
#        raise


client.checkout('https://svn.worldforge.org:886/svn/media/trunk', REPO_VAR)
"""Checkout the repository """
