#wombat created by Kai Blin ported by Pronoy Chopra to Flask
#all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
from flaskext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declartive import declarative_base



engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine)))

Base = decarative_base()
Base.query = db_session.query_property()

def init_db():
    import wombat.models
    Base.metadata.create_all(bind=engine)


#configuration

DB = '/tmp/wombat.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_envvar('WOMBAT_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:'



def conect_db():
    return sqlite3.connect(app.config['DB'])

@app.route('/')
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run()

