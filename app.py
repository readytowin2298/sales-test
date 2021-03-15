import os
from flask import Flask, render_template, request, flash, redirect, session, g
from models import connect_db, db, User, NewAccount, OldAccount
from forms import  UserForm, NewAccQuest, OldAccQuest

CURR_USER_KEY = "curr_user"


app = Flask(__name__)

app.config['WTF_CSRF_ENABLED'] = False
# Only un-comment while testing

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgres://rfdqftki:a0Y8qhkuFT-um6ZWMYd78Vq5cde9t_Kh@ziggy.db.elephantsql.com:5432/rfdqftki'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///sales_test'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


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
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username must be unique!", category="danger")
            return redirect('/signup')
        u = User.create(username=form.username.data, password=form.password.data)
        try:
            db.session.add(u)
            db.session.commit()
        except:
            db.session.rollback()
            flash("Error Contacting Database", category='warning')
            return redirect('/')
        do_login(u)
        flash("Account Successfully Created", category='success')
        return redirect('/')
    return render_template('/users/signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if g.user:
        flash("You are already logged in!", category="warning")
        return redirect('/')
    form = UserForm()

    if form.validate_on_submit():
        u = User.authenticate(username=form.username.data, password=form.password.data)
        if not u:
            flash("Invalid Credentials", category='warning')
            return redirect('/login')
        else:
            do_login(u)
            flash("Successfully Logged in", category="success")
            return redirect('/')
    return render_template('/users/login.html', form=form)


@app.route('/logout')
def logout():
    do_logout()
    flash("Come Back Soon!", category='warning')
    return redirect('/')


@app.route('/new-accounts')
def show_new_accounts():
    if not g.user:
        flash("You must be logged in for that!", category="warning")
        return redirect('/login')
    accounts = NewAccount.query.all()
    return render_template("/base/newAcct.html", accounts=accounts)


@app.route('/old-accounts')
def show_old_accounts():
    if not g.user:
        flash("You must be logged in for that!", category="warning")
        return redirect('/login')
    accounts = OldAccount.query.all()
    return render_template("/base/oldAcct.html", accounts=accounts)


@app.route('/accounts/old/<int:account_num>')
def old_account_view(account_num):
    if not g.user:
        flash("You must be logged in for that!", category='warning')
        return redirect('/login')
    old_account = OldAccount.query.filter_by(old_account_num=account_num).first()
    if not old_account:
        flash("Sorry, we can't locate that account", category='danger')
        return redirect('/new-accounts')
    if old_account.new_account_num:
        new_account = NewAccount.query.filter_by(new_account_num=old_account.new_account_num).first().fill_form()
    else:
        new_account = None
    old_account = old_account.fill_form()
    return render_template('/forms/accountCompare.html', new_account=new_account, old_account=old_account)
@app.route('/accounts/new/<int:account_num>')
def new_account_view(account_num):
    if not g.user:
        flash("You must be logged in for that!", category='warning')
        return redirect('/login')
    new_account = NewAccount.query.filter_by(old_account_num=account_num).first()
    if not new_account:
        flash("Sorry, we can't locate that account", category='danger')
        return redirect('/old-accounts')
    if new_account.old_account_num:
        old_account = OldAccount.query.filter_by(old_account_num=new_account.old_account_num).first().fill_form()
    else:
        old_account = None
    new_account = new_account.fill_form()
    return render_template('/forms/accountCompare.html', new_account=new_account, old_account=old_account)



    












"""Stop flask from caching anything"""
@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req