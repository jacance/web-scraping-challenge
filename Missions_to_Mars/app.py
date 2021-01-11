# import libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# create instance of Flask app
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def echo():
    return render_template("index.html", text= "Mission to Mars")

if __name__ == "__main__":
    app.run(debug=True)