from flask import Blueprint, render_template

# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
bookbp = Blueprint('bookings', __name__, url_prefix='/bookings')

@bookbp.route('/')
def show():
    return render_template('bookings.html')