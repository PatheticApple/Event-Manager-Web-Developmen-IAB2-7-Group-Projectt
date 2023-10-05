from flask import Blueprint, render_template

# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
detailsbp = Blueprint('details', __name__, url_prefix='/details')

@detailsbp.route('/')
def show():
    return render_template('eventDetails.html')