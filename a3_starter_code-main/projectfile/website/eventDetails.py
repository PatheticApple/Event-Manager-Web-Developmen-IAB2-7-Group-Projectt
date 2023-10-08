from flask import Blueprint, render_template
from .models import Event, EventDetail, TicketType
from . import db
# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
detailsbp = Blueprint('details', __name__, url_prefix='/details')

@detailsbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.eventID==id))
    eventDetails = db.session.scalar(db.select(EventDetail).where(EventDetail.eventID==id))
    ticketDetails = db.session.query(TicketType).filter(TicketType.eventID == id).all()
    # print(tickets)
    return render_template('eventDetails.html', event=event, eventDetails= eventDetails, ticketDetails= ticketDetails)