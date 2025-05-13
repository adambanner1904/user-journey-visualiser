from flask import Blueprint, render_template, request, flash, redirect, url_for  # type: ignore
import pandas as pd
import os


projects = Blueprint('projects', __name__)


@projects.route('/projects', methods=["GET", "POST"])
def manage_projects():
    flash("This works")
    if request.method == "POST":
        name = request.form['name'].lower().replace(' ', '-')
        project_dir = os.path.join("/user-journey-visualiser/app/static/projects", name)
        if os.path.exists(project_dir):
            flash("This project already exists", 'error')
            return redirect(url_for('manage_projects'))

        os.mkdir(project_dir)
        print(f"{project_dir} directory created!")
        # file = request.files['data']
        # print(file)


    return render_template('projects.html')