from flask import Blueprint, render_template
from app.db import get_tables

ujv = Blueprint('ujv', __name__)

@ujv.route('/')
@ujv.route('/user-journey-visualiser')
def user_journey_visualiser():
    projects = get_tables()
    projects = [(project, project.replace('_', ' ').capitalize()) for project in projects]
    return render_template('ujv.html', projects=projects)