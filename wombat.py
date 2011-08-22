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
from flaskext.mail import Mail
import os
#-------------------------------------------------------------------------------

# create our  application :)
app = Flask(__name__)

# take the configuration from the config file
app.config.from_object(config_file)


#use py-bcrypt for hashing password
bcrypt_init(app)

mail = Mail(app)


#all functions need to have to be imported from Base class or SVNfunctions() class
func = Base()
svn = SVNfunctions(app.config['LOCAL_REPO'])

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
    
    def validate_user(self,username):
        access_user = User.query.filter_by(email = username.data).first()
        if not access_user.active:
            raise ValidationError, "User not Active"


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
        
    #name of the user: Non Mandatory
    Name = TextField("Your full name")
    
    #nick name of the user: Non Mandatory
    Nickname = TextField("Your nick name")
    
    #vcs_username of the user: Non Mandatory
    VCS_Username = TextField("Your VCS Username")
    
    #vcs_password of the user: Non mandatory
    VCS_Password = PasswordField("Your VCS Password")

    submit = SubmitField("Register")   
    
    #querying for known entries for the given email    
    def validate_username(self,email):
        unidentified = User.query.filter_by(email=email.data).first()
        if unidentified is not None:
            raise ValidationError, "Username already exists"
     
     
     
    class UpdateForm (Form):
        
        #username = TextField("Your new email")
        password = PasswordField("New Password", [
                                validators.Required(),
                                validators.EqualTo('confirm', 
                                message='Passwords must match')
                                ])
        confirm = PasswordField("Your new password again")
        Name = TextField("Your name")
        Nickname = TextField("Your nickname")    
        VCS_Username = TextField("Your VCS Username")
        VCS_Password = PasswordField("Your VCS Password")
        Update = SubmitField("Update Information")
           
           
     class ForgotPassword (Form):
         
         username = TextField("Your Email/Username ")
         submit = SubmitField("Check for Username")
         
         def validate_email(self,username):
             forgetful_user = User.query.filter_by(email=username.data).first()
             if forgetful_user is None:
                 raise ValidationError, "Username doesn't exist"
         
            
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
    #unwind a touple 
    
    fileSize = func.convert_bytes(fileSize)
    #convert fileSize in human readable form
    
    serverdict = (dict(url_out=url_out,revision=revision,fileSize=fileSize, \
        fileLength=fileLength,folderCount=folderCount)) 
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
        
        #need to hash password
        password_hash = generate_password_hash(form.password.data)
        new_user = User(form.email.data,password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        #bug fixed: if VCS_Password is not empty then hash otherwise not
        if not (form.VCS_Password.data == ''):
            #need to hash VCS password
            VCS_Password_hash = generate_password_hash(form.VCS_Password.data)
            new_user_data = UserData(form.Name.data, form.Nickname.data, \
                form.VCS_Username.data,VCS_Password_hash)
        
        else:
            new_user_data= UserData(form.Name.data, form.Nickname.data, \
                form.VCS_Username.data,form.VCS_Password.data)
        
        
        db.session.add(new_user_data)
        db.session.commit()
        
        #simple check to see if the user has been registered
        access_user = User.query.filter_by(email = form.email.data).first()
        if not access_user is None:
            flash('The User details have been registered. ')
            #func.send_activation(form.email.data)
            
            #status of registeration
            registeration_status="Sent email to user for activation"
            return redirect(url_for('login'), registered=registeration_status)
        else:
            flash("The User doesn't seem to be in our Database yet, please try again")
        
                    
    return render_template('add_user.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm(request.form)
    if form.validate_on_submit():
        session['logged_in'] = True
        session['username'] = form.username.data
        if session['logged_in']:
            flash('You were logged in as '+ session['username'])
        else:
            flash('oops you were not logged in')
        return redirect(url_for('server_status'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('server_status'))

@app.route('/navigator', methods=['GET', 'POST'])
def navigator():
    path =  request.args['path']
    repo_path = app.config['LOCAL_REPO']
    
    path = path[1:]
        
    requested_path = os.path.join(repo_path, path)
    
    if not os.path.exists(requested_path):
        return render_template("navigator.html", 
                                listType="PATHNOTFOUND")
        
    elif not os.path.isdir(requested_path):
        return render_template("navigator.html", 
                                listType="SHOWFILE", 
                                path=path)
                                
    else:
        return render_template('navigator.html', 
                                listType = "SHOWDIRECTORY",
                                path="/" + path, 
                                listing=svn.get_dir_info(path))
#---------------------not so important pages------------------------------------


        


@app.route('/activate/<username>/<hash>')
def activate_username():

@app.route('/forgot_password')
def forgot_password():
    form = ForgotPassword(request.form)
    if form.validate_on_submit():
        return render_template('forgot_password.html')


@app.route('/workbench')
def workbench():
    return render_template('workbench.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/settings/account')
def account_settings():
    form = UpdateForm(request.form)
    if request.method == 'POST' and form.validate():
        logged_user = session['username']
        request_user = User.query.filter_by(username = logged_user).first()
        
        
        
        
    return render_template('account_settings.html')


@app.route('/status')
def status_view():
    return render_template('status.html')
    
@app.route('/mail')
def mail():
    return render_template('mail.html')

@app.route('/mail/inbox')
def mail_inbox():
    return render_template('mail_inbox.html')

@app.route('/docs')
def show_docs():
    return render_template('docs.html')

@app.route('/docs/know_more')
def know_more():
    return render_template('know_more.html')

@app.route('/docs/why')
def why():
    return render_template('why.html')

@app.route('/docs/license')
def license():
    return render_template('license.html')

if __name__ == '__main__':
    app.run()
