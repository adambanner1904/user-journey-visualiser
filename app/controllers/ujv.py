from flask import Blueprint, render_template

ujv = Blueprint('ujv', __name__)

@ujv.route('/')
@ujv.route('/user-journey-visualiser')
def user_journey_visualiser():
    return render_template('ujv.html')