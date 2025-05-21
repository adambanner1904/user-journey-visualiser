from flask import Blueprint, render_template, redirect, url_for, request

from app.db import get_tables
from app.graph import write_graph_html

ujv = Blueprint('ujv', __name__)

EDGE_WIDTH_OPTIONS = ['unique_page_views', 'page_views']

@ujv.route('/')
@ujv.route('/user-journey-visualiser')
def user_journey_visualiser():
    projects = get_tables()
    chosen_project = request.args.get('project_name')
    precision = request.args.get('precision')
    chosen_edge_width = request.args.get('edge_width')

    # If chosen precision is not in query parameters then
    # set the default graph precision to 0.9
    if not precision:
        chosen_precision = 0.9
    else:
        chosen_precision = float(precision)

    if not chosen_edge_width:
        chosen_edge_width = 'unique_page_views'


    # If chosen project is not in query parameters then choose the first project as the default
    if not chosen_project:
        chosen_project = projects[0]

    write_graph_html(chosen_project, chosen_edge_width, chosen_precision)

    return render_template('ujv.html'
                           , projects=format_attributes(projects)
                           , edge_width_options=format_attributes(EDGE_WIDTH_OPTIONS)
                           , chosen_project=chosen_project
                           , chosen_precision=chosen_precision
                           , chosen_edge_width=chosen_edge_width)

@ujv.route('/show-journey', methods=['POST'])
def show_journey():
    project_name = request.form['project']
    precision = request.form['precision']
    edge_width = request.form['edge-width']

    return redirect(url_for('ujv.user_journey_visualiser', project_name=project_name, edge_width=edge_width, precision=precision))

@ujv.route('/get-graph')
def get_graph():
    return render_template('graph.html')



# Helper functions

def format_attributes(attributes: list[str]) -> list[tuple[str, str]]:
    return [(attribute, attribute.replace('_', ' ').capitalize()) for attribute in attributes]
