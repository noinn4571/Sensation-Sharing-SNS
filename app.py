from flask import Flask, render_template, request, redirect, url_for, abort, session
from werkzeug.utils import secure_filename
import pykakasi, os
from cron import get_oura_data
import pyrebase # Firebaseを使うためのライブラリ

app = Flask(__name__)
secret_key = os.urandom(24)
app.secret_key = secret_key  # セッションのためのシークレットキーを設定

# Firebaseの設定
firebase_config = {
    "apiKey": "AIzaSyBoiM0YSR1BZ-ROnxkn5JjanMxsV0bCXo0",
    "authDomain": "sensation-sharing-sns.firebaseapp.com",
    "databaseURL": "https://sensation-sharing-sns.firebaseio.com",
    "projectId": "sensation-sharing-sns",
    "storageBucket": "sensation-sharing-sns.firebasestorage.app",
    "messagingSenderId": "779528505803",
    "appId": "1:779528505803:web:1e5133a2b657ce7e82ce4e",
    "measurementId": "G-7NS8QH0E1E"
}

firebase = pyrebase.initialize_app(firebase_config)  # Firebaseアプリを初期化
auth = firebase.auth()  # Firebase認証を初期化

@app.route("/")
def home():
    if 'user' in session:
        latest_bpm, latest_timestamp = get_oura_data.get_lastbpm()  # latest_bpmとlatest_timestampを取得
        return render_template('home.html', latest_bpm=latest_bpm, latest_timestamp=latest_timestamp)
    else:
        return redirect(url_for('login'))  # ユーザーがログインしていない場合、ログインページにリダイレクト

@app.route("/login", methods=["GET", "POST"])
def login():
    result = True
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)  # Firebaseでユーザーを認証
            session['user'] = user['idToken']  # セッションにユーザーのIDトークンを保存
            return redirect(url_for('home'))  # 認証が成功した場合、ホームページにリダイレクト
        except:
            result = False  # 認証が失敗した場合、resultをFalseに設定
    return render_template('login.html', result=result)  # GETリクエストの場合、ログインページを表示

@app.route("/registration", methods=["GET", "POST"])
def registration():
    result = True
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.create_user_with_email_and_password(email, password)  # Firebaseで新しいユーザーを作成
            session['user'] = user['idToken']  # セッションにユーザーのIDトークンを保存
            return redirect(url_for('home'))  # ユーザー作成が成功した場合、ホームページにリダイレクト
        except:
            result = False
            return render_template('registration.html', result=result)  # ユーザー作成が失敗した場合、エラーメッセージを表示
    return render_template('registration.html')  # GETリクエストの場合、登録ページを表示

@app.route("/logout")
def logout():
    session.pop('user', None)  # セッションからユーザー情報を削除
    return redirect(url_for('login'))  # ログアウト後、ログインページにリダイレクト

@app.route("/timeline")
def timeline():
    if 'user' in session:
        return render_template('timeline.html')  # ユーザーがログインしている場合、タイムラインページを表示
    else:
        return redirect(url_for('login'))  # ユーザーがログインしていない場合、ログインページにリダイレクト

@app.route("/profile")
def profile():
    if 'user' in session:
        return render_template('profile.html')  # ユーザーがログインしている場合、プロフィールページを表示
    else:
        return redirect(url_for('login'))  # ユーザーがログインしていない場合、ログインページにリダイレクト

@app.route("/post")
def post():
    if 'user' in session:
        return render_template('post.html')  # ユーザーがログインしている場合、投稿ページを表示
    else:
        return redirect(url_for('login'))  # ユーザーがログインしていない場合、ログインページにリダイレクト

@app.errorhandler(500)
def system_error(error):
    error_description = error.description
    return render_template('system_error.html', error_description=error_description), 500  # 500エラーが発生した場合、システムエラーページを表示

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404  # 404エラーが発生した場合、ページが見つからないエラーページを表示

if __name__ == "__main__":
    app.run(debug=True)  # デバッグモードでアプリケーションを実行
