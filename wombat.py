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
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
#from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from wombat_config import config_file
from wombat_config.config_file import LOCAL_REPO
from wombatdb import db
from wombatdb import User
from backend.svnfunctions import SVNfunctions
from backend.functions import Base
from flaskext.login import LoginManager
# create our little application :)




app = Flask(__name__)
app.config.from_object(config_file)



login_manager = LoginManager()
#login_manager = setup_app(app)

func = Base()
svn = SVNfunctions()



@login_manager.user_loader
def load_user(userid):
        return User.get(userid)



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
        #returns the URL of the local repository
    svn.update_copy()
        #call this function before fetching any other information
    revision = svn.get_revision_no()
        #gets the revision number
        #info = func.get_info(LOCAL_REPO)
        #gets the number of bytes(size), number of files, number of folders
    #if not session.get('logged_in'):
        #cur = g.db.execute('select title, text from entries order by id desc')
        #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    #fileCount = 'foo'
    #fileSize = 'foo'
    #fileListLen = 'foo'
    return render_template('server_status.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email_entered = request.form['email']
        password_entered = request.form['password']
        unidentified = User.query.filter_by(email=email_entered).first()
        exists = unidentified is None
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
            new_user = User(email_entered,password_entered)
            db.session.add(new_user)
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
        access_user = User.query.filter_by(email=email_access).first()
        check = access_user is None
        if check:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('server_status'))


if __name__ == '__main__':
    app.run()
