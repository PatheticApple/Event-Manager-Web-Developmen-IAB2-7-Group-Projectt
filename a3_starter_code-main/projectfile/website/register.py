from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm

# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
registerbp = Blueprint('register', __name__, url_prefix='/register')

@registerbp.route('/', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True):
            print("you have successfully registered")
            #get username, password and email from the form
            fname = register.first_name.data
            lname = register.last_name.data
            pnumber = register.phone_number.data
            pwd = register.password.data
            email = register.email_id.data
            #check if a user exists
            user = db.session.scalar(db.select(User).where(User.email_address==email))
            if user:#this returns true when user is not None
                flash('Email is already in use, please try another')
                return redirect(url_for('auth.register'))
            # don't store the password in plaintext!
            pwd_hash = generate_password_hash(pwd)
            #create a new User model object
            new_user = User(firstName=fname, lastName=lname, mobileNo=pnumber, password_hash=pwd_hash, email_address=email)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('user.html', form=register, heading='Register')