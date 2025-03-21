from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
import pykakasi, os
from cron import get_oura_data

app = Flask(__name__)

@app.route("/")
def home():
    latest_bpm, latest_timestamp = get_oura_data.get_lastbpm() # latest_bpmとlatest_timestampを取得
    return render_template('home.html', latest_bpm=latest_bpm, latest_timestamp=latest_timestamp)

@app.route("/timeline")
def timeline():
    return render_template('timeline.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/post")
def post():
    return render_template('post.html')

@app.errorhandler(500)
def system_error(error):
    error_description = error.description
    return render_template('system_error.html', 
                           error_description=error_description), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)


