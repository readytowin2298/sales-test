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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rfdqftki:a0Y8qhkuFT-um6ZWMYd78Vq5cde9t_Kh@ziggy.db.elephantsql.com:5432/rfdqftki'

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
    old_accounts = OldAccount.query.filter_by(created_by=g.user.username).all()
    new_accounts = NewAccount.query.filter_by(created_by=g.user.username).all()
    return render_template('/base/home.html', old_accounts=old_accounts, new_accounts=new_accounts)


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
        new_account = NewAccount.query.filter_by(new_account_num=old_account.new_account_num).first()
        if new_account:
            new_account = new_account.fill_form()
         
    if not new_account:
        new_account = None
    old_account = old_account.fill_form()
    return render_template('/forms/accountCompare.html', new_account=new_account, old_account=old_account)
@app.route('/accounts/new/<int:account_num>')
def new_account_view(account_num):
    if not g.user:
        flash("You must be logged in for that!", category='warning')
        return redirect('/login')
    new_account = NewAccount.query.filter_by(new_account_num=account_num).first()
    if not new_account:
        flash("Sorry, we can't locate that account", category='danger')
        return redirect('/old-accounts')
    if new_account.old_account_num:
        old_account = OldAccount.query.filter_by(old_account_num=new_account.old_account_num).first()
    if not old_account:
        old_account = None
    return render_template('/forms/accountCompare.html', new_account=new_account, old_account=old_account)


@app.route('/old-accounts/add', methods=["GET", "POST"])
def add_old_account():
    if not g.user:
        flash("You aren't logged in!", category='warning')
        return redirect('/login')
    form = OldAccQuest()
    if form.validate_on_submit():
        acc = OldAccount(
            name=form.account_name.data,
            phone_number=form.phone_number.data,
            new_account_num=form.account_number.data,
            old_account_num=form.account_number.data,
            approve_transfer=bool(form.approve_transfer.data),
            equipment_present=bool(form.equipment_present.data),
            recent_service_issues=form.recent_service_issues.data,
            currently_connected=bool(form.currently_connected.data),
            knows_where_equipment=bool(form.knows_where_equipment.data),
            eth_present=bool(form.eth_present.data),
            eth_to_poe=bool(form.eth_to_poe.data),
            eth_in_port=bool(form.eth_in_port.data),
            poe_light=bool(form.poe_light.data),
            has_managed_router=bool(form.has_managed_router.data),
            created_by=g.user.username

        )
        try:
            db.session.add(acc)
            db.session.commit()
            flash("Success", category='success')
            return redirect('/old-accounts')
        except:
            flash("Sorry, error connecting to database", category="danger")
            return redirect("/")
    return render_template('/forms/OldAccForm.html', form=form)

@app.route('/new-accounts/add', methods=['GET','POST'])
def add_new_account():
    if not g.user:
        flash("You aren't logged in!", category='warning')
        return redirect('/login')
    form = NewAccQuest()
    if form.validate_on_submit():
        acc = NewAccount(
            name=form.account_name.data,
            phone_number=form.phone_number.data,
            new_account_num=form.account_number.data,
            old_account_num=form.account_number.data,
            equipment_present=bool(form.equipment_present.data),
            wants_equipment_moved=bool(form.wants_equipment_moved.data),
            knows_where_equipment=bool(form.knows_where_equipment.data),
            eth_present=bool(form.eth_present.data),
            eth_to_poe=bool(form.eth_to_poe.data),
            eth_in_port=bool(form.eth_in_port.data),
            poe_light=bool(form.poe_light.data),
            transfer_when=form.transfer_when.data,
            wants_managed_router=bool(form.wants_managed_router.data),
            need_router_ship=bool(form.need_router_ship.data),
            wifi_ssid=form.wifi_ssid.data,
            wifi_pw=form.wifi_pw.data,
            created_by=g.user.username
        )
        try:
            db.sesssion.add(acc)
            db.session.commit()
            flash("Account info added correctly!", category='success')
        except:
            flash("Sorry, error connecting to database", category="danger")
            return redirect("/")
        if acc.old_account_num and not OldAccount.query.filter_by(old_account_num=acc.old_account_num).first():
            flash(f"Please input information for account {acc.old_account_num}", category='warning')
            return redirect('/old-accounts/add')
        return redirect(f'/accounts/new/{acc.new_account_number}')
    return render_template('/forms/NewAccForm.html', form=form)

@app.route('/accounts/new/<int:account_num>/edit', methods=["GET", "POST"])
def edit_new(accout_num):
    if not g.user:
        flash("You aren't logged in!", category='warning')
        return redirect('/login')
    account = NewAccount.query.filter_by(new_account_num=account_num).first()
    if not account:
        flash("Sorry, we can't locate that accout.", category="danger")
        return redirect("/")
    form = account.fill_form()
    if form.validate_on_submit():
        account.name = form.account_name.data
        account.phone_number = form.phone_number.data
        account.new_account_num = form.new_account_num.data
        account.old_account_num = form.old_account_num.data
        account.equipment_present = bool(form.equipment_present.data)
        account.wants_equipment_moved = bool(form.wants_equipment_moved.data)
        account.knows_where_equipment = bool(form.knows_where_equipment.data)
        account.eth_present = bool(form.eth_present.data)
        account.eth_to_poe = bool(form.eth_to_poe.data)
        account.eth_in_port = bool(form.eth_in_port.data)
        account.poe_light = bool(form.poe_light.data)
        account.transfer_when = form.transfer_when.data
        account.wants_managed_router = bool(form.wants_managed_router.data)
        account.need_router_ship = bool(form.need_router_ship.data)
        account.wifi_ssid = form.wifi_ssid.data
        account.wifi_pw = form.wifi_pw.data
        try:
            db.session.add(account)
            db.session.commit()
            flash("Success!", category='success')
            return redirect(f"/accounts/new/{account.new_account_num}")
        except:
            flash("Sorry, error connecting to database", category="danger")
            return redirect("/")
        











"""Stop flask from caching anything"""
@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req