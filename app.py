import os
from flask import Flask, render_template, request, flash, redirect, session, g
from models import connect_db, db, User
from forms import UserForm

CURR_USER_KEY = "curr_user"


app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres://rfdqftki:a0Y8qhkuFT-um6ZWMYd78Vq5cde9t_Kh@ziggy.db.elephantsql.com:5432/rfdqftki'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

@app.route('/')
def home():
    if not g.user:
        return redirect('/login')

    return render_template('/base/home.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if g.user:
        flash("You are already logged in!", category="warning")
        return redirect('/')
    form = UserForm()
    if form.authenticate_on_submit():
        






















"""Stop flask from caching anything"""
@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req