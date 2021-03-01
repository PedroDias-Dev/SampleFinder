from flask import Flask
import routes

app = Flask(__name__)

# app.use(routes)

app.run(routes)