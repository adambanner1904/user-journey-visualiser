from flask import Blueprint, render_template, redirect, url_for, request

from app.db import get_tables
from app.graph import write_graph_html

ujv = Blueprint('ujv', __name__)

@ujv.route('/')
@ujv.route('/user-journey-visualiser')
def user_journey_visualiser():
    projects = get_tables()
    chosen_project = request.args.get('project_name')
    precision = request.args.get('precision')

    # If chosen precision is not in query parameters then
    # set the default graph precision to 0.9
    if not precision:
        chosen_precision = 0.9
    else:
        chosen_precision = float(precision)

    # If chosen project is not in query parameters then choose the first project as the default
    if not chosen_project:
        chosen_project = projects[0]

    write_graph_html(chosen_project, chosen_precision)

    return render_template('ujv.html'
                           , projects=projects_with_formatted(projects)
                           , chosen_project=chosen_project
                           , chosen_precision=chosen_precision)

@ujv.route('/show-journey', methods=['POST'])
def show_journey():
    project_name = request.form['project']
    precision = request.form['precision']
    return redirect(url_for('ujv.user_journey_visualiser', project_name=project_name, precision=precision))

@ujv.route('/get-graph')
def get_graph():
    return render_template('graph.html')



# Helper functions

def projects_with_formatted(projects: list[str]) -> list[tuple[str, str]]:
    return [(project, project.replace('_', ' ').capitalize()) for project in projects]