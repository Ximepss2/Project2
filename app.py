from flask import Flask, render_template
import json

import psycopg2 


app = Flask(__name__)



@app.route("/")
def home():
  return render_template("home.html")


def graph():
  return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)