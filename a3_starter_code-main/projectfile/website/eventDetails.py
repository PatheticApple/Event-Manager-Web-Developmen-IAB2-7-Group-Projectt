from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Event, EventDetail, TicketType, Comment
from .forms import CommentForm
from . import db


#additional import:
from flask_login import login_required, current_user

# name - first argument is the blueprint name 
# import name - second argument - helps identify the root url for it 
detailsbp = Blueprint('details', __name__, url_prefix='/details')


@detailsbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.eventID==id))
    eventDetails = db.session.scalar(db.select(EventDetail).where(EventDetail.eventID==id))
    ticketDetails = db.session.query(TicketType).filter(TicketType.eventID == id).all()
    cform = CommentForm() 
    # print(tickets)
    return render_template('eventDetails.html', event=event, eventDetails= eventDetails, ticketDetails= ticketDetails, form = cform)



@detailsbp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(id):
    #here the form is created  form = CommentForm()
    form = CommentForm()
    #get the destination object associated to the page and the comment
    eventDetails = db.session.scalar(db.select(Event).where(Event.eventID==id))
    print("EVENT DETAILS:", eventDetails)
    eventComments = db.session.scalar(db.select(Comment).where(Comment.eventID==id))
    comment_content = request.form['comment_content']
    rating_value = request.form['rating_value']

    if comment_content and comment_content != "" and rating_value:
        print("DOES IT GET POST?")
        new_comment = Comment(
            commentContent=comment_content,
            ratingValue=rating_value,
            event = eventDetails,
            user = current_user
            # user=1,  # Replace with the actual user ID (you might get this from the logged-in user)
            # event=1  # Replace with the actual event ID
        )
        db.session.add(new_comment)
        db.session.commit()
    # if form.validate_on_submit():
    #     print("DOES IT GET POST?")
    #     new_comment = Comment(
    #         commentContent=comment_content,
    #         ratingValue=rating_value,
    #         event = eventDetails,
    #         user = current_user
    #         # user=1,  # Replace with the actual user ID (you might get this from the logged-in user)
    #         # event=1  # Replace with the actual event ID
    #     )
    #     db.session.add(new_comment)
    #     db.session.commit()
    # flash('Your comment has been added', 'success')  
    #flashing a message which needs to be handled by the html
    # print(f"The following comment has been posted: {form.text.data}")
  # notice the signature of url_for
    return redirect(url_for('details.show', id=id))