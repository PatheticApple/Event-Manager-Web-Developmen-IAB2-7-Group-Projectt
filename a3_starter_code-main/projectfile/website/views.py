from flask import Blueprint, render_template
from .models import User, Event, EventDetail, Booking, Comment, TicketType
bp = Blueprint('main', __name__)
from . import db

@bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    
    return render_template('index.html', events = events)

