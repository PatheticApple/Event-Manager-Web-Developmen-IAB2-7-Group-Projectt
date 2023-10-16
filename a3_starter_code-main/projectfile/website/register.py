from flask import Blueprint, render_template

# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
registerbp = Blueprint('register', __name__, url_prefix='/register')

@registerbp.route('/')
def show():
    return render_template('register.html')