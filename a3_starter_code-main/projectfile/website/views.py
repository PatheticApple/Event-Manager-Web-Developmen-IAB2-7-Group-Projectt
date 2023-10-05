from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    # return '<h1>Starter code for the assessment<h1>'
    return render_template('index.html')

