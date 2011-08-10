#author: Pronoy Chopra
#imports
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
import wombat_config.config_file
from os.path import splitext
from backend.functions import Base
#initialising the flask application
app = Flask(__name__)

func = Base()

#app.config.from_object(wombat_config.config_file)

#configuration from the SQLALCHEMY_DATABASE_URI variable which is essentially
#the creation of database using sqlite
#can be put in a separate config and be imported
app.config['SQLALCHEMY_DATABASE_URI'] = wombat_config.config_file.DB_URI

#flask extension initialized
db = SQLAlchemy(app)

#Define models here:
class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default=u'Unnamed collection')
    #collections = db.relationship('Collection',backref = 'asset', lazy ='dynamic')

    def __init__(self,name,tags):
        self.name= name
        self.tags= tags


class Asset(db.Model):
   # __bind_key__='assets'
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, default=u'Unnamed Asset')
    used_by = db.Column(db.Integer, db.ForeignKey('collections.id'))

    def __init__(self,name,tags):
        self.name = name
        self.tags = tags

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    active = db.Column(db.Boolean)

    def __init__(self,email,password,active=False):
        self.email = email
        self.password = password
        self.active = active

class UserData(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    nick = db.Column(db.String(255))
    vcs_user = db.Column(db.String(255))
    vcs_pass = db.Column(db.String(255))
    user_id = db.Column(db.String(255),db.ForeignKey('users.id'))

    def __init__(self,name=None, nick=None,vcs_user=None,vcs_pass=None):
        self.name = name
        self.nick = nick
        self.vcs_user = vcs_user
        self.vcs_pass = vcs_pass

class Dir(db.Model):
    __tablename__ = 'dirs'
    path = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    root = db.Column(db.String(255))
    rev_id = db.Column(db.Integer, db.ForeignKey('revisions.id'))
    in_dir = db.Column(db.String(255), db.ForeignKey('dirs.path'))
    #dirs = db.relationship('DIR',backref='files',lazy='dynamic')

    def __init__(self,path,name,root):
        self.path = path
        self.name = name
        self.root = root

class Revision(db.Model):
    __tablename__ = 'revisions'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255), default='')
    log = db.Column(db.Text, default = u'No log message')
    author = db.Column(db.String(255), default = u'Unknown Author')
    date = db.Column(db.DateTime)
    #revisions = db.relationship('Revision',backref='dirs',lazy='dynamic')

    def __init__(self,name,log,author,date):
        self.id = id
        self.name = name
        self.log = log
        self.author = author
        self.date = date

class File(db.Model):
    path = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    size = db.Column(db.Integer)
    root = db.Column(db.String(255))
    ext = db.Column(db.String(20))
    type = db.Column(db.String(20),default=u'other')
    as_thumbnail = db.Column(db.Boolean,default=False)
    in_dir = db.Column(db.String(255),db.ForeignKey('dirs.path'))
    rev_id = db.Column(db.Integer, db.ForeignKey('revisions.id'))
    used_by = db.Column(db.Integer, db.ForeignKey('assets.id'))

    def __init__(self,path,name,size,root):
        self.path = path
        self.name = name
        self.size = size
        self.root = root
        dummy, self.ext = splitext(name)
        self.ext = self.ext.lower()
        self.type = unicode(func.getType(name))


#create the database by db.create_all()
#if database is present, it won't be overwritten
def init_db():
    db.create_all()
