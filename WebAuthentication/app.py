import os
from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_httpauth import HTTPDigestAuth
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_dev_key")
digest_auth = HTTPDigestAuth()


USER_DATA = {"admin": "password123"}


@digest_auth.get_password
def get_pw(username):
    return USER_DATA.get(username)


oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password and USER_DATA.get(username) == password:
            session["user"] = username
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/digest-login")
@digest_auth.login_required
def digest_login():
    session["user"] = digest_auth.username()
    return redirect(url_for("index"))


@app.route("/google-login")
def google_login():
    if google is None:
        return "Google OAuth not configured properly", 500

    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    if google is None:
        return "Google OAuth not configured properly", 500

    google.authorize_access_token()
    resp = google.get("https://www.googleapis.com/oauth2/v3/userinfo")

    if resp and resp.status_code == 200:
        user_info = resp.json()
        session["user"] = user_info.get("name")
        return redirect(url_for("index"))

    return "Failed to fetch user info from Google", 400


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    # ssl_ontext='adhocc' for google auth on localhost
    app.run(debug=True, ssl_context="adhoc")
