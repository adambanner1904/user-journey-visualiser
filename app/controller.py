from flask import Blueprint, render_template, request # type: ignore
import pandas as pd
projects = Blueprint('projects', __name__)


@projects.route('/projects')
def manage_projects():
    return render_template('projects.html')

@projects.route('/projects', methods=["POST"])
def manage_projects():
    csv = request.files.get("data")
    # pd.read_csv(csv)
    return 