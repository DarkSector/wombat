#setup the application the starting point to everything
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
import wombatdb


#Create the database
wombatdb.init_db()

