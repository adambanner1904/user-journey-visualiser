from flask import Blueprint, render_template, request, flash, redirect, url_for  # type: ignore
from app.db import create_table, table_exists, insert_dataframe_into_table, get_tables, drop_table
import pandas as pd
import string

projects = Blueprint('projects', __name__, url_prefix='/projects')


@projects.route('')
def manage_projects():
    projects = get_tables()
    return render_template('projects.html', projects=projects)


@projects.route('/add-project', methods=['POST'])
def add_project():
    name = request.form['name']
    file = request.files['data']

    if not is_valid_name(name):
        flash("Name does not match the specified format", category='error')
        return redirect(url_for('projects.manage_projects'))

    formatted_name = format_name(name)
    if table_exists(formatted_name):
        flash(f"There already exists a project with the name {name}", category="error")
        return redirect(url_for('projects.manage_projects'))

    # File checks
    if file.filename == '':
        flash("File is required!", category='error')
        return redirect(url_for('projects.manage_projects'))

    create_table(formatted_name)
    insert_dataframe_into_table(formatted_name, pd.read_csv(file))

    return redirect(url_for('projects.manage_projects'))


@projects.route('/delete-project/<name>')
def delete_project(name):
    drop_table(name)
    return redirect(url_for('projects.manage_projects'))


def format_name(name: str):
    if not is_valid_name(name):
        return redirect(request.url)
    return name.replace('-', '_').replace(' ', '_')


def is_valid_name(name: str) -> bool:
    allowed_chars = set(string.ascii_letters + '-_ ' + string.digits)
    return set(name) <= allowed_chars
