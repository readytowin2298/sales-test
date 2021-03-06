from enum import unique
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from forms import NewAccQuest, OldAccQuest

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
    """Keeps track of new account
        options in Remote Transfers"""

    __tablename__ = 'remote_transfers_new'

    name = db.Column(db.Text,
                nullable=False)
    phone_number = db.Column(db.Text,
                nullable=False)

    new_account_num = db.Column(db.Integer,
                primary_key=True)
    
    old_account_num = db.Column(db.Integer)

    equipment_present = db.Column(db.Boolean,
                nullable=False,
                default=True)

    wants_equipment_moved = db.Column(db.Boolean,
                nullable=False,
                default=False)

    knows_where_equipment = db.Column(db.Boolean,
                nullable=False,
                default=True)

    eth_present = db.Column(db.Boolean,
                nullable=False,
                default=True)
    eth_to_poe = db.Column(db.Boolean,
                nullable=False,
                default=True)
    eth_in_port = db.Column(db.Boolean,
                nullable=False,
                default=True)
    poe_light = db.Column(db.Boolean,
                nullable=False,
                default=True)
    transfer_when = db.Column(db.Text,
                nullable=False,
                default="n/a")
    wants_managed_router = db.Column(db.Boolean,
                nullable=False,
                default=False)
    need_router_ship = db.Column(db.Boolean,
                nullable=False,
                default=False)
    wifi_ssid = db.Column(db.Text,
                nullable=True)
    wifi_pw = db.Column(db.Text,
                nullable=True)
    created_by = db.Column(db.Text,
              db.ForeignKey('users.username'))
    
    def fill_form(self):
        form = NewAccQuest()
        form.account_number.data = self.new_account_num
        form.account_name.data = self.name
        form.phone_number.data = self.phone_number
        form.equipment_present.data = int(self.equipment_present)
        form.wants_equipment_moved.data = int(self.wants_equipment_moved)
        form.knows_where_equipment.data = int(self.knows_where_equipment)
        form.eth_present.data = int(self.knows_where_equipment)
        form.eth_in_port.data = int(self.eth_in_port)
        form.poe_light.data = int(self.poe_light)
        form.cx_wants_router.data = int(self.wants_managed_router)
        form.old_account_num.data = int(self.old_account_num)
        form.wifi_ssid.data = self.wifi_ssid
        form.wifi_pw.data = self.wifi_pw
        form.need_router_ship.data = int(self.need_router_ship)
        form.transfer_when.data = self.transfer_when

        return form

    
    

class OldAccount(db.Model):
    """Keeps track of old account
        options in Remote Transfers"""

    __tablename__ = 'remote_transfers_old'

    name = db.Column(db.Text,
                nullable=False)
    phone_number = db.Column(db.Text,
                nullable=False)
    new_account_num = db.Column(db.Integer)
    
    old_account_num = db.Column(db.Integer,
                primary_key=True)

    approve_transfer = db.Column(db.Boolean,
                nullable=False,
                default=False)
    equipment_present = db.Column(db.Boolean,
                nullable=False,
                default=True)

    recent_service_issues = db.Column(db.Text,
                nullable=True)

    currently_connected = db.Column(db.Boolean)

    knows_where_equipment = db.Column(db.Boolean,
                nullable=False,
                default=True)
    eth_present = db.Column(db.Boolean,
                nullable=False,
                default=True)
    eth_to_poe = db.Column(db.Boolean,
                nullable=False,
                default=True)
    eth_in_port = db.Column(db.Boolean,
                nullable=False,
                default=True)
    poe_light = db.Column(db.Boolean,
                nullable=False,
                default=True)
    has_managed_router = db.Column(db.Boolean,
                nullable=False,
                default=False)
    created_by = db.Column(db.Text,
              db.ForeignKey('users.username'))
    
    def fill_form(self):
        form = OldAccQuest()
        form.account_number.data = self.old_account_num
        form.account_name.data = self.name
        form.phone_number.data = self.phone_number
        form.equipment_present = int(self.equipment_present)
        form.approve_transfer.data = int(self.approve_transfer)
        form.recent_service_issues.data = self.recent_service_issues
        form.currently_connected.data = int(self.currently_connected)
        form.knows_where_equipment.data = int(self.knows_where_equipment)
        form.eth_present.data = int(self.eth_present)
        form.eth_in_port.data = int(self.eth_in_port)
        form.poe_light.data = int(self.poe_light)
        form.has_managed_router.data = int(self.has_managed_router)
        form.new_account_num.data = int(self.new_account_num)

        return form
    



