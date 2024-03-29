
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed
ALLOWED_FILE = {'PNG','JPG','png','jpg'}


#creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email", validators=[InputRequired('Enter email')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name=StringField("First Name", validators=[InputRequired()])
    last_name=StringField("Last Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone_number=StringField("Phone Number", validators=[InputRequired()])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")



# Comment forms
class CommentForm(FlaskForm):
  text = TextAreaField('Share your experience here!', [InputRequired()])
  rating = IntegerField('Please give a rating out of 5', validators=[NumberRange(min=1, max=5, message="Please select a rating between 1 and 5")])
  submit = SubmitField('Post a review')


class CreateEventForm(FlaskForm):
   eventName = TextAreaField('Your Event Name', [InputRequired()])
   suburb = TextAreaField('Suburb', [InputRequired()])
   state = TextAreaField('State', [InputRequired()])
   date = DateField('Date', [InputRequired()], format='%Y-%m-%d')
   time = TimeField('Time', [InputRequired()], format='%H:%M')
   image = FileField('Destination Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])