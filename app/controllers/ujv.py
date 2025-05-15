from flask import Blueprint, render_template, redirect, url_for, request

from app.db import get_tables
from app.graph import Graph, update_graph_html

ujv = Blueprint('ujv', __name__)

@ujv.route('/')
@ujv.route('/user-journey-visualiser')
def user_journey_visualiser():
    projects = get_tables()
    projects = [(project, project.replace('_', ' ').capitalize()) for project in projects]

    chosen_project = projects[0][0]
    update_graph_html(chosen_project)

    return render_template('ujv.html', projects=projects, chosen_project=chosen_project)

@ujv.route('/show-journey', methods=['POST'])
def show_journey():
    project_name = request.form['project']
    g = Graph(project_name, 'page_views', 0.95)
    g.create_graph()
    return redirect(url_for('ujv.user_journey_visualiser'))

@ujv.route('/get-graph')
def get_graph():
    return render_template('graph.html')

