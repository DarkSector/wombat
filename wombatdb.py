#flask sqlalchemy test1
#author: Pronoy Chopra


#imports
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
import wombat_config.config_file


#initialising the flask application
app = Flask(__name__)

#app.config.from_object(wombat_config.config_file)

#configuration from the SQLALCHEMY_DATABASE_URI variable which is essentially
#the creation of database using sqlite engine
#can be put in a separate config and be imported
app.config['SQLALCHEMY_DATABASE_URI'] = wombat_config.config_file.DB_URI

#flask extension initialized
db = SQLAlchemy(app)

#import models here:


#import model.__init__
#import model.asset
#model.asset.create_db()

"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True)

    def __init__(self,username):
        self.username = username
"""

#create the database by db.create_all()
#if database is present, it won't be overwritten
def init_db():
    db.create_all()
