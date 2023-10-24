#from package import Class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    # app.debug=True
    app.secret_key='somesecretgoeshere'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventManagement.sqlite'
    #initialise db with flask app
    db.init_app(app)
    Bootstrap5(app)

    
    
    # bootstrap = Bootstrap5(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    # login_manager.login_view='auth.login'
    # login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a common practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import bookings
    app.register_blueprint(bookings.bookbp)

    from . import eventEditor
    app.register_blueprint(eventEditor.editbp)

    from . import eventDetails
    app.register_blueprint(eventDetails.detailsbp)

    from . import auth
    app.register_blueprint(auth.authbp)
    
    from . import register
    app.register_blueprint(register.registerbp)

    from . import login
    app.register_blueprint(login.loginbp)

    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter 
    def not_found(e): 
        return render_template("error.html")
    

     #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    
    return app



