#flask sqlalchemy test1
#author: Pronoy Chopra


#imports
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
import wombat_config

import model
#initialising the flask application
app = Flask(__name__)

#app.config.from_object(wombat_config.config_file)

#configuration from the SQLALCHEMY_DATABASE_URI variable which is essentially
#the creation of database using sqlite
#can be put in a separate config and be imported
app.config['SQLALCHEMY_DATABASE_URI'] = wombat_config.config_file.DB_URI

#flask extension initialized
db = SQLAlchemy(app)

METADATA = app.metadata
engine = app.engine
"""
#database model or table declaration. The structure of the tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    level = db.Column(db.String(50), unique=True)


#init function the functions will be called as 
#wombatdb.db.User.<function name>
    def __init__(self, username, email,level):
        self.username = username
        self.email = email
        self.level = level


    def __repr__(self):
        return '<User %r>' % self.username

"""





#create the database by db.create_all()
#if database is present, it won't be overwritten
def init_db():
    db.create_all()
