# -*- coding: utf-8 -*-
"""
    Wombat 
    ~~~~~~

    An Asset Managment System written using Flask with SQLAlchemy
    
    Extensions used:
        Flask-SQLAlchemy
        Flask-WTF
        Flask-Uploads
        Flask-Mail    

    :Author : Pronoy Chopra
    :Project: Worldforge
    :program: GSoC 2011
    :Mentor : Kai Blin
            
"""
#-----------------------------imports-------------------------------------------
#bunch of imports
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
#from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from wombat_config import config_file
from wombat_config.config_file import LOCAL_REPO, FIRST_VIEW
from wombatdb import db
from wombatdb import User, UserData
from backend.svnfunctions import SVNfunctions
from backend.functions import Base
from flaskext.bcrypt import bcrypt_init, generate_password_hash, \
    check_password_hash
from flaskext.wtf import Form, TextField, TextAreaField, PasswordField, \
    SubmitField, Required, ValidationError, validators

#-------------------------------------------------------------------------------

# create our  application :)
app = Flask(__name__)

# take the configuration from the config file
app.config.from_object(config_file)


#use py-bcrypt for hashing password
bcrypt_init(app)



#all functions need to have to be imported from Base class or SVNfunctions() class
func = Base()
svn = SVNfunctions()

#-----------------------All forms are defined here------------------------------

class LoginForm (Form):
    
    
    username = TextField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Login")
    
    
    def validate_username(self,username):
        access_user = User.query.filter_by(email = username.data).first()
        if access_user is None:
            raise ValidationError, "Invalid Username"


    def validate_password(self,password):
        access_user = User.query.filter_by(email = self.username.data).first()
        if access_user is None:
            raise ValidationError, "Invalid Username"
        else:
            condition = check_password_hash(access_user.password, password.data)
        if not condition:
            raise ValidationError, "Invalid Password"


#this is the registeration form
class RegisterationForm (Form):
        
    #email field: Mandatory
    email = TextField("Email Address", [validators.Length(min=6)])
    
    #password field: Mandatory
    password = PasswordField("New Password", [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    
    #confirm password field: Mandatory
    confirm = PasswordField('Repeat Password')
    
    #generate hash of password
    if confirm == password:
        password = generate_password(password)
    
    #name of the user: Non Mandatory
    Name = TextField("Your full name")
    
    #nick name of the user: Non Mandatory
    Nickname = TextField("Your nick name")
    
    #vcs_username of the user: Non Mandatory
    VCS_Username = TextField("Your VCS Username")
    
    #vcs_password of the user: Non mandatory
    VCS_Password = PasswordField("Your VCS Password")
    
    VCS_Password = generate_password_hash(VCS_Password)
    
    #querying for known entries for the given email

    
    def validate_username(self,email):
        unidentified = User.query.filter_by(email=email.data).first()
        if unidentified is not None:
            raise ValidateError, "Username already exists"


#-----------------------------database related actions--------------------------


def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    g.db.close()
    return response

#----------------------------decorators start here------------------------------

#index page
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
    
    
    
#add a new user 
@app.route('/register', methods=['GET', 'POST'])
def add_user():
    
    #render registeration form
    form = RegisterationForm(request.form)
    
    #if posted and email is non empty and password is non empty
    if request.method == 'POST' and form.validate():
        new_user = User(form.email.data,form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        new_user_data = UserData(form.Name.data, form.Nickname.data, \
            form.VCS_Username.data,form.VCS_Password.data)
        
        #NOTE: The Password and the VCS_Password are already hashed when obtaining
        #      the said values from the form
        #      refer the RegisterationForm class.
        
        db.session.add(new_user_data)
        db.session.commit()
                    
    return render_template('add_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm(request.form)
    if form.validate_on_submit():
        session['logged_in'] = True
        session['username'] = form.username.data
        if session['login']:
            flash('You were logged in '+ session['username'])
        else:
            flash('you were not logged in')
        return redirect(url_for('server_status'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('server_status'))


#---------------------not so important functions--------------------------------

@app.route('/settings')
def settings():
    pass

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



if __name__ == '__main__':
    app.run()
