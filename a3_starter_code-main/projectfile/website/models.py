from . import db
from datetime import datetime, date
import enum
from sqlalchemy import Enum

class EventStatusEnum(enum.Enum):
    Open = 'Open'
    SoldOut = 'SoldOut'
    Inactive = 'Inactive'
    Cancelled = 'Cancelled'


class User(db.Model):
    __tablename__ = 'users'
    userID = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(100), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    mobileNo = db.Column(db.String(10), nullable=False)
    

    # relations
    eventCreated = db.relationship('Event', backref='user')
    bookings = db.relationship('Booking', backref='user')
    comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return f"User's Email: {self.email_address}"


class Event(db.Model):
    __tablename__ = 'events'
    eventID = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(100), index=True, nullable=False)
    suburb = db.Column(db.String(100), index=True, nullable=False)
    state = db.Column(db.String(100), index=True, nullable=False)
    dateTime = db.Column(db.Date, nullable=False, default=date)
    genres = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(EventStatusEnum), nullable=False)
    imagePath = db.Column(db.String(200), nullable=False)
    # foreign keys
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    

    # relations
    # eventStatus = db.relationship('EventStatus', backref='event')
    eventDetail = db.relationship('EventDetail', backref='event')
    ticketType = db.relationship('TicketType', backref='event')
    bookings = db.relationship('Booking', backref='event')
    comments = db.relationship('Comment', backref='event')

    def __repr__(self):
        return f"Event's Name: {self.eventName}"

# class EventStatus(db.Model):
#     __tablename__ = 'eventStatus'
#     eventStatusID = db.Column(db.Integer, primary_key=True)
#     eventStatusName = db.Column(db.Enum(EventStatusEnum), nullable=False)
#     eventStatusDate = db.Column(db.DateTime, nullable=False , default=datetime.now())

#     # foreign keys
#     eventID = db.Column(db.Integer, db.ForeignKey('events.eventID'))

#     def __repr__(self):
#         return f"Event's Status: {self.eventStatusName}"

class EventDetail(db.Model):
    __tablename__ = 'eventDetails'

    # foreign key
    eventID = db.Column(db.Integer, db.ForeignKey('events.eventID'), primary_key=True)

    artistName = db.Column(db.String(100), nullable=False)
    imagePath = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    capacity =  db.Column(db.Integer, nullable=False)
    availability =  db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Event's Description: {self.description}"
    

class TicketType(db.Model):
    __tablename__ = 'ticketTypes'
    ticketID = db.Column(db.Integer, primary_key=True)
    ticketType = db.Column(db.String(100), nullable=False)
    ticketPrice = db.Column(db.Integer, nullable=False)
    ticketAvailability = db.Column(db.Integer, nullable=False)

    # foreign keys
    eventID = db.Column(db.Integer, db.ForeignKey('events.eventID'))

    # relations
    # comments = db.relationship('Booking', backref='ticketType')

    def __repr__(self):
        return f"Event's Ticket: {self.ticketType}"
    

class Booking(db.Model):
    __tablename__ = 'bookings'
    bookingID = db.Column(db.Integer, primary_key=True)
    ticketType = db.Column(db.String(100), nullable=False)
    NoOfTicket = db.Column(db.Integer, nullable=False)
    totalPrice = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False , default=datetime.now())

    # foreign keys
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    eventID = db.Column(db.Integer, db.ForeignKey('events.eventID'))
    ticketID = db.Column(db.Integer, db.ForeignKey('ticketTypes.ticketID'))


    def __repr__(self):
        return f"Booking ID: {self.bookingID}"
    

class Comment(db.Model):
    __tablename__ = 'comments'
    commentID = db.Column(db.Integer, primary_key=True)
    post_date = db.Column(db.Date, nullable=False , default=datetime.now())
    commentContent = db.Column(db.String(500), nullable=False)
    ratingValue = db.Column(db.Integer, nullable=False)

    # foreign keys
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    eventID = db.Column(db.Integer, db.ForeignKey('events.eventID'))


    def __repr__(self):
        return f"Comment Content: {self.commentContent}"