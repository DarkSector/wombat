#flask sqlalchemy test1
#author: Pronoy Chopra


#imports
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
import wombat_config
#import model
#initialising the flask application
app = Flask(__name__)

#app.config.from_object(wombat_config.config_file)


return app.metadata

#configuration from the SQLALCHEMY_DATABASE_URI variable which is essentially
#the creation of database using sqlite
#can be put in a separate config and be imported
app.config['SQLALCHEMY_DATABASE_URI'] = wombat_config.config_file.DB_URI

#flask extension initialized
db = SQLAlchemy(app)

#METADATA = app.metadata
#engine = app.engine


#create the database by db.create_all()
#if database is present, it won't be overwritten
def init_db():
    db.create_all()
