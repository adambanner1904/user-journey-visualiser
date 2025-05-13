import sqlite3
import string

from flask import Blueprint, render_template, request, flash, redirect, url_for  # type: ignore
import pandas as pd
import os

from app.db import create_table, table_exists

projects = Blueprint('projects', __name__)


@projects.route('/projects', methods=["GET", "POST"])
def manage_projects():
    if request.method == "POST":
        name = request.form['name']
        file = request.files['data']

        # Name checks
        if not is_valid_name(name):
            flash("Name does not match the specified format", category='error')
            return redirect(request.url)
        name = format_name(name)

        # Check if formatted name is already a table name
        # Cant have duplicate tables
        if table_exists(name):
            flash(f"There already exists a project with the name {name}", category="error")
            return redirect(request.url)

        # File checks
        if file.filename == '':
            flash("File is required!", category='error')
            return redirect(request.url)

        csv = pd.read_csv(file)
        create_table(name)
        # with sqlite3.connect("temp.db") as conn:
        #     cur = conn.cursor()
        #     results = cur.execute("select * from temp")
        #     for result in results:
        #         print(result[0])
    return render_template('projects.html')


def format_name(name: str):
    if not is_valid_name(name):
        return redirect(request.url)
    print(f'My name is {name}')
    return name.replace('-', '_').replace(' ', '_')

def is_valid_name(name: str) -> bool:
    allowed_chars = set(string.ascii_letters + '-_ ')
    return set(name) <= allowed_chars