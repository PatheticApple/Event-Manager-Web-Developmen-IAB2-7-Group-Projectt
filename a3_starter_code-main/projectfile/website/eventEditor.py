from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, EventDetail, TicketType
import os
from . import db
from werkzeug.utils import secure_filename
from .forms import CommentForm
from datetime import datetime,date

#additional import:
from flask_login import login_required, current_user


# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
editbp = Blueprint('creator', __name__, url_prefix='/creator')

def check_upload_file(image):
  #get file data from form  
  fp = image
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = 'image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@editbp.route('/')
@login_required
def show():
    return render_template('eventEditor.html')


@editbp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    # Get form data
    event_name = request.form['event_name']
    suburb = request.form['suburb']
    state = request.form['state']
    date1 = request.form['date']
    date2 = datetime.strptime(date1, '%Y-%m-%d')
    genres = request.form['genres']
    filePath = request.files['file']
    filePath2 = check_upload_file(filePath)
    artist_name = request.form['artist_name']
    description = request.form['description']
    capacity = request.form['capacity']
    # availability = request.form['availability']
    filePath3 = request.files['file2']

    status = request.form['status']
    filePath32 = check_upload_file(filePath3)


    custom_ticket_names = request.form.getlist('custom_ticket_names[]')
    custom_ticket_prices = request.form.getlist('custom_ticket_prices[]')
    custom_ticket_quantities = request.form.getlist('custom_ticket_quantities[]')


        
    # Get ticket types from the form
    # ticket_types = request.form.getlist('ticket_types[]')
    # if date2 < datetime.today():
    #    status = "Inactive"
    # else:
    #    status = "Open"
    # Create Event object and add it to the database

    eventDetaiis = EventDetail(description = description, artistName = artist_name, capacity = capacity, availability = capacity, imagePath = filePath32)
    event = Event(eventName = event_name, suburb = suburb, state = state, dateTime = date2, genres = genres, imagePath = filePath2, status=status, eventDetail = eventDetaiis, user = current_user)  # Assuming 'filename' is the path to the uploaded image
    

    
    db.session.add(event)
    db.session.commit()
  


    for name, price, quantity in zip(custom_ticket_names, custom_ticket_prices, custom_ticket_quantities):
        ticket = TicketType(eventID=event.eventID, ticketType=name, ticketPrice=float(price), ticketAvailability = quantity)
        db.session.add(ticket)
        db.session.commit()
    # Create TicketType objects and add them to the database
    # for ticket_type in ticket_types:
    #     if ticket_type == 'VIP':
    #         price = 50.0
    #     elif ticket_type == 'Normal':
    #         price = 25.0

    #     ticket = TicketType(event_id=event.id, type=ticket_type, price=price)
    #     db.session.add(ticket)
    #     db.session.commit()

    # Redirect to a success page or home page
    flash("Event created", "info")
    return redirect(url_for('main.index'))



@editbp.route('/update_event/<id>', methods=['GET', 'POST'])
@login_required
def show2(id):
    event = db.session.scalar(db.select(Event).where(Event.eventID==id))
    eventDetails = db.session.scalar(db.select(EventDetail).where(EventDetail.eventID==id))
    ticketDetails = db.session.query(TicketType).filter(TicketType.eventID == id).all()

    return render_template('eventEditor2.html', event=event, eventDetails=eventDetails, ticketDetails=ticketDetails)



@editbp.route('/update_event/<id>/update', methods=['GET', 'POST'])
@login_required
def update2(id):
    print("ID:", id)
    # Get form data
    event_name = request.form['event_name']
    suburb = request.form['suburb']
    state = request.form['state']
    date1 = request.form['date']
    date2 = datetime.strptime(date1, '%Y-%m-%d')
    genres = request.form['genres']
    # filePath = request.files['file']
    # filePath2 = check_upload_file(filePath)
    artist_name = request.form['artist_name']
    description = request.form['description']
    capacity = request.form['capacity']
    status = request.form['status']
    # availability = request.form['availability']
    # filePath3 = request.files['file2']
    # filePath32 = check_upload_file(filePath3)


    custom_ticket_names = request.form.getlist('custom_ticket_names[]')
    custom_ticket_prices = request.form.getlist('custom_ticket_prices[]')
    custom_ticket_quantities = request.form.getlist('custom_ticket_quantities[]')
    

    event = db.session.scalar(db.select(Event).where(Event.eventID==id))
    eventDetails = db.session.scalar(db.select(EventDetail).where(EventDetail.eventID==id))
    ticketDetails = db.session.query(TicketType).filter(TicketType.eventID == id).all()
    cform = CommentForm() 
    event.eventName = event_name
    event.suburb = suburb
    event.state = state
    event.date = date2
    event.genres = genres
    event.status = status
    eventDetails.artistName = artist_name
    eventDetails.description = description

    oldCapacity = int(eventDetails.capacity)
    differenceCapacity = int(capacity) - oldCapacity 
    eventDetails.capacity = capacity
    eventDetails.availability += differenceCapacity
    db.session.commit()

    return redirect(url_for('details.show', id=id))