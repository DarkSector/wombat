# -*- coding: utf-8 -*-
"""
    Wombat 
    ~~~~~~

    An Asset Managment System written using Flask with SQLAlchemy
    

    :Author: Pronoy Chopra
    :Project: Worldforge
    :program: GSoC 2011
    :Mentor : Kai Blin
            
"""

#bunch of imports
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
#from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from wombat_config import config_file
from wombat_config.config_file import LOCAL_REPO, FIRST_VIEW
from wombatdb import db
from wombatdb import User
from backend.svnfunctions import SVNfunctions
from backend.functions import Base

from flaskext.bcrypt import bcrypt_init, generate_password_hash, \
    check_password_hash



# create our  application :)
app = Flask(__name__)
app.config.from_object(config_file)
# take the configuration from the config file


#use py-bcrypt for hashing password
bcrypt_init(app)


#all functions need to have to be imported from Base class or SVNfunctions() class
func = Base()
svn = SVNfunctions()


def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])

"""
#Use the following only for non SQLAlchemy based system

def init_db():
    #Creates the database tables.
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
"""



@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    g.db.close()
    return response




@app.route('/')
def server_status():
    #The repository information belongs to the updated copy of a 
    #checked out version on the local system
    url_out = svn.get_url()
        #returns the URL of the repository not the checked out version
    svn.update_copy()
        #call this function before fetching any other information
    revision = svn.get_revision_no()
        #gets the revision number
    
    fileSize,fileLength,folderCount = func.get_info(LOCAL_REPO)
    #unfurl a touple 
    
    fileSize = func.convert_bytes(fileSize)
    #convert fileSize in human readable form
    
    serverdict = (dict(url_out=url_out,revision=revision,fileSize=fileSize, \
        fileLength=fileLength,folderCount=folderCount,first_view=FIRST_VIEW)) 
    #create a dict out of the information that needs to be passed to the template

    return render_template('server_status.html',serverdict=serverdict)
    #pass serverdict as the context
    

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email_entered = request.form['email']
        password_entered = request.form['password']
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        name = first_name + ' ' + last_name
        nick = request.form['nick']
        vcs_user = request.form['vcs-username']
        vcs_pass = request.form['vcs-password']
        #user_id = request.form['user-id']
        #email and password from the form
        
        unidentified = User.query.filter_by(email=email_entered).first()
        exists = unidentified is None
        #check whether the user exists in the database
        
        """
        syntax:
        <Table>.query.filter_by(<field>=<data>).first()

        unidentified is None
        returns false this means the data exists in the field

        if true it means unidentified does not exist in the field
        """
        
        if not exists:
            flash('Sorry the email is already registered')
        
        else:
            pw_hash = generate_password_hash(password_entered)
            #hash the password entered into the form
            
            vcspw_hash = generate_password_hash(vcs_pass)
            #hash the vcs password entered into the form
            new_user = User(email_entered,pw_hash)
            #enter the information into the databse
            
            db.session.add(new_user)
            db.session.commit()   
            #commit the change to User 
            
            new_user_data = UserData(name,nick,vcs_user,vcspw_hash)
            db.session.add(new_user_data)
            db.session.commit()
            
            flash('email registered')
            
            """
            syntax:
            <variable> = <Table>(values accepted in the __init__() function)
            db.session.add(<variable>)
            db.session.commit()
            """
            
            
    return render_template('add_user.html')

@app.route('/docs/know_more')
def know_more():
    return render_template('know_more.html')

@app.route('/docs/why')
def why():
    return render_template('why.html')

@app.route('/docs/license')
def license():
    return render_template('license.html')

@app.route('/docs')
def show_docs():
    return render_template('docs.html')

"""
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('server_status'))
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email_access = request.form['email']
        password_access = request.form['password']
        access_user = User.query.filter_by(email=email_access).first()
        check = access_user is None
        if check:
            error = 'Invalid username'
        elif not (check_password_hash(access_user.password,password_access)):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('server_status'))
    return render_template('login.html', error=error)
    
    
#@app.route('/settings')
#def settings():
#        if session.logged


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('server_status'))


if __name__ == '__main__':
    app.run()
