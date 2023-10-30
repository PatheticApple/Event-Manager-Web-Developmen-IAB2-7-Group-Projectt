from flask import Blueprint, render_template
from .models import Event, EventDetail, TicketType, Comment, Booking, User

from . import db
#additional import:
from flask_login import login_required, current_user


# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
bookbp = Blueprint('bookings', __name__, url_prefix='/bookings')



@bookbp.route('/')
@login_required
def show():
    allBookings = db.session.query(Booking).filter(Booking.userID == current_user.userID).all()

    # for booking in allBookings:
    #     print(booking)

    return render_template('bookings.html', bookings = allBookings, user = current_user)