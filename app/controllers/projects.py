import sqlite3

from flask import Blueprint, render_template, request, flash, redirect, url_for  # type: ignore
import pandas as pd
import os


projects = Blueprint('projects', __name__)


@projects.route('/projects', methods=["GET", "POST"])
def manage_projects():
    if request.method == "POST":
        name = request.form['name'].lower().replace(' ', '-')
        file = request.files['data']
        csv = pd.read_csv(file)
        print(csv)

        with sqlite3.connect("temp.db") as conn:
            cur = conn.cursor()
            results = cur.execute("select * from temp")
            for result in results:
                print(result[0])
    return render_template('projects.html')