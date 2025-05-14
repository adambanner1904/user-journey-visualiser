import sqlite3
import string

from flask import Blueprint, render_template, request, flash, redirect, url_for  # type: ignore
import pandas as pd

from app.db import create_table, table_exists, insert_dataframe_into_table

projects = Blueprint('projects', __name__, url_prefix='/projects')


@projects.route('', methods=["GET"])
def manage_projects():
    return render_template('projects.html')


@projects.route('/add-project', methods=['POST'])
def add_project():
    name = request.form['name']
    file = request.files['data']

    # Name checks
    if not is_valid_name(name):
        flash("Name does not match the specified format", category='error')
        return redirect(request.url)

    formatted_name = format_name(name)

    # Check if formatted name is already a table name
    # Cant have duplicate tables
    if table_exists(formatted_name):
        flash(f"There already exists a project with the name {name}", category="error")
        return redirect(request.url)

    # File checks
    if file.filename == '':
        flash("File is required!", category='error')
        return redirect(request.url)

    data = pd.read_csv(file)

    create_table(formatted_name)
    insert_dataframe_into_table(formatted_name, data)
    return redirect(url_for('projects.manage_projects'))


def format_name(name: str):
    if not is_valid_name(name):
        return redirect(request.url)
    print(f'My name is {name}')
    return name.replace('-', '_').replace(' ', '_')


def is_valid_name(name: str) -> bool:
    allowed_chars = set(string.ascii_letters + '-_ ')
    return set(name) <= allowed_chars
