from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
import pykakasi, os
from cron import get_oura_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/post")
def post():
    return render_template('post.html')

if __name__ == "__main__":
    app.run(debug=True)
