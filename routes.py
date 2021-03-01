from flask import Flask
import sys
import sqlite3
import os
from src.controllers import SamplesController
from flask_cors import CORS, cross_origin
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)

# SamplesController.index()

DATABASE = "D:\Prog\PythonBack\src\database\database.sqlite"
YoutubeApiPath = "D:\Prog\PythonBack\src\controllers\py.py"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def db_connection():
    conn = None
    
    conn = sqlite3.connect(DATABASE)
    # except sqlite3.error as e:
    #     print(e)
    return conn

@app.route("/samples", methods=["GET"])
@cross_origin()
def samplescon():
    return SamplesController.index()

@app.route("/samples/<int:id>", methods=["GET"])
@cross_origin()
def single_sample(id):
    conn = db_connection()
    cursor = conn.cursor()
    
    cursor = conn.execute("SELECT * FROM savedsample WHERE id=?", (id,))
    videos = [
        dict(id=row[0], idytb=row[1], title=row[2], views=row[3])
        for row in cursor.fetchall()
    ]
    if videos is not None:
        return jsonify(videos)

@app.route("/generate", methods=["POST", "DELETE"])
@cross_origin()
def generate_list():
    conn = db_connection()
    cursor = conn.cursor()

    exec(open('D:\Prog\PythonBack\src\controllers\py.py').read())

    # try:
    if request.method == "POST":
        new = request.get_json()

        # new_title = request.args["title"]
        # new_idytb = request.args["idytb"]
        # new_views = request.args["views"]

        new_title = new.get("title")
        new_idytb = new.get("idytb")
        new_views = new.get("views")

        sql = """INSERT INTO savedsample (idytb, title, views) VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_idytb, new_title, new_views))
        conn.commit()
                    
        return f"New List created successfully (id: {cursor.lastrowid})", 201
    # except Exception as e:
    #     return e
    if request.method == "DELETE":
        sql = """ DELETE FROM savedsample """
        conn.execute(sql)
        conn.commit()
        return "The current list  has been deleted. ID: {}".format(id), 200


@app.route("/")
def hello_world():
    return "Hello World! <strong>I am learning Flask</strong>", 200

app.run()




# routes.get('/samples', samplesController.index);
# routes.post('/samples', samplesController.create);

# routes.use('/generate', python)

# routes.get('/savedsamples', samplesController.index);
# routes.post('/savedsamples', samplesController.create);