from flask import Blueprint, render_template

# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
editbp = Blueprint('creator', __name__, url_prefix='/creator')

@editbp.route('/')
def show():
    return render_template('eventEditor.html')