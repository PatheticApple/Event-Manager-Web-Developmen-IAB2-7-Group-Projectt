from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import check_password_hash
from .models import User
from . import db
from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm

# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
loginbp = Blueprint('login', __name__, url_prefix='/login')

@loginbp.route('/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if(login_form.validate_on_submit()==True):
        #get the username and password from the database
        email = login_form.email.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email_address==email))
        #if there is no user with that name
        if user is None:
            error = 'Invalid Credentials'#could be a security risk to give this much info away
        #check the password - notice password hash function
        elif not check_password_hash(user.password_hash, password): # takes the hash and password
            error = 'Incorrect password'
        if error is None:
            #all good, set the login_user of flask_login to manage the user
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')