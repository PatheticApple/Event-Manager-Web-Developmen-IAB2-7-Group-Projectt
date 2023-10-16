from flask import Blueprint, render_template

# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
loginbp = Blueprint('login', __name__, url_prefix='/login')

@loginbp.route('/')
def show():
    return render_template('login.html')