from enum import unique
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    username = db.Column(db.Text,
                primary_key=True)

    password = db.Column(db.Text,
                nullable=False)
    needs_change = db.Column(db.Boolean,
                nullable=False,
                default=False)
    
    @classmethod
    def create(cls, username, password):
        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode('utf8')

        return cls(username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, password):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False

class NewAccount(db.Model):
    """Keeps track of new accounts 
        in Remote Transfers"""

    __tablename__ = 'remote_transfers_new'

    account_number = db.Column(db.Integer,
                primary_key=True)
    old_account_number = db.ForiegnKey('remote_transfers_old.account_number')

    old_account = db.relationship('OldAccount',
                backref='new_account')

    account_name = db.Column(db.Text,
                nullable=False)
    address = db.Column(db.Text,
                nullable=False)
    phone_number = db.Column(db.Text)

    

class OldAccount(db.Model):
    """Keeps track of old accounts 
        in remote transfers"""

    __tablename__ = 'remote_transfers_old'
            
    account_number = db.Column(db.Integer,
                primary_key=True)
    account_name = db.Column(db.Text,
                nullable=False)
    address = db.Column(db.Text,
                nullable=False)
    phone_number = db.Column(db.Text)

    approve_transfer = db.Column(db.Boolean,
                nullable=False,
                default=False)
    
    



