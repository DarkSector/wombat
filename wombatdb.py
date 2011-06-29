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

class Assets(db.Model):
    asset_id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(80))
    asset_type = db.Column(db.String(40))
    asset_commit = db.Column(db.Text)
    change_user = db.Column(db.String(50))
    asset_size = db.Column(db.Integer)
    date_stamp = db.Column(db.DateTime)


    def __init__(self, asset_id, asset_name, asset_type, \
            asset_commit, change_user, asset_size, date_stamp=None):
        self.asset_id = asset_id
        self.asset_name = asset_name
        self.asset_type = asset_type
        if date_stamp is None:
            self.date_stamp = date_stamp
        self.asset_commit = asset_commit
        self.change_user = change_user
        self.asset_type = asset_type
        

    def __repr__(self):
        return '<Asset %r>' % self.asset_name

"""





#create the database by db.create_all()
#if database is present, it won't be overwritten
def init_db():
    db.create_all()
