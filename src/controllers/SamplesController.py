import responses
# import requests
import os
import sqlite3
import json
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
app = Flask(__name__)
# from . import py

# connection = sqlite3.connect('database.sqlite')
# cursor = connection.cursor()
DATABASE = "D:\Prog\PythonBack\src\database\database.sqlite"

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.error as e:
        print(e)
    return conn

# LER TODOS
def index():
    conn = db_connection()
    cursor = conn.cursor()

    cursor = conn.execute("SELECT * FROM savedsample")
    videos = [
        dict(id=row[0], idytb=row[1], title=row[2], views=row[3])
        for row in cursor.fetchall()
    ]
    if videos is not None:
        return jsonify(videos)

def generate():
    conn = db_connection()
    cursor = conn.cursor()

    
    if request.method == "POST":
        new_idytb = request.form["idytb"]
        new_title = request.form["title"]
        new_views = request.form["views"]
        sql = """INSERT INTO savedsample (idytb, title, views)
                VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_idytb, new_title, new_views))
        conn.commit()
            
        return f"New List created successfully", 201 , 201

        


    






