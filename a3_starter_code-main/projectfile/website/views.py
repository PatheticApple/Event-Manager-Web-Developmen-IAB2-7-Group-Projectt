from flask import Blueprint, render_template, request, redirect, url_for
from .models import User, Event, EventDetail, Booking, Comment, TicketType
from datetime import datetime

bp = Blueprint('main', __name__)
from . import db

@bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    
    return render_template('index.html', events = events)

@bp.route('/search', methods=['GET'])
def search():
    search = request.args.get('mainSearchBar')
    genres = request.args.getlist('genre')
    statuses = request.args.getlist('status')
    state = request.args.get('stateInput')
    suburb = request.args.get('suburbInput')
    date = request.args.get('eventDateTime')
    if search or genres or statuses or state or suburb or date or search != "" or state != "" or suburb != "":
        if genres:
            # print(type(genres))
            events = Event.query.filter(Event.genres.in_(genres))
        else:
            events = Event.query

        if statuses:
            events = events.filter(Event.status.in_(statuses))

        if state:
            if (state == "tasmania" or state == "Tasmania"):
                state = "TAS"
            if (state == "queensland" or state == "Queensland"):
                state = "QLD"
            if (state == "new south wales" or state == "New South Wales"):
                state = "NSW"
            if (state == "victoria" or state == "Victoria"):
                state = "VIC"
            if (state == "south australia" or state == "South Australia"):
                state = "SA"
            if (state == "western australia" or state == "Western Australia"):
                state = "WA"
            events = events.filter(Event.state.ilike(f"%{state}%"))

        if suburb:
            events = events.filter(Event.suburb.ilike(f"%{suburb}%"))
        
        if search:
            query = "%" + search + "%"
            events = Event.query.filter(
            (Event.genres.ilike(f"%{query}%")) |
            (Event.status.ilike(f"%{query}%")) |
            (Event.dateTime.ilike(f"%{query}%")) |
            (Event.state.ilike(f"%{query}%")) |
            (Event.suburb.ilike(f"%{query}%")) |
            (Event.eventName.ilike(f"%{query}%")))
        
        if date:
            try:
                print("Date: " + date)
                events = events.filter(Event.dateTime == date)
            except ValueError:
                # Handle invalid date format if needed
                pass
        # if search_query:
        #     events = events.filter(Event.name.ilike(f"%{search_query}%"))

        events = events.all()

        return render_template('index.html', events=events, genres = genres)
    else:
        return redirect(url_for('main.index'))
    
        