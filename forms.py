from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField, RadioField
from wtforms import validators
from wtforms.validators import DataRequired, InputRequired, Length


class UserForm(FlaskForm):

    username = StringField("Billmax Username",
                validators=[InputRequired()])
    password = PasswordField("A password of your choosing",
                validators=[Length(min=6, message="Password must be at least six characters long")])
    

class AccountForm(FlaskForm):

    account_number = IntegerField("*Account Number",
                validators=[InputRequired()])
    account_name = StringField("*Account Name",
                validators=[InputRequired()])
    address = StringField("*Service Address",
                validators=[InputRequired()])
    phone_number = StringField("Best Callback",
                validators=[InputRequired()])

class NewAccQuest(FlaskForm):

    new_account_num = IntegerField("*New Account Number",
                validators=[InputRequired()])
    old_account_num = IntegerField("*Old Account Number",
                validators=[InputRequired()])
    equipment_present = RadioField("*Is the POE Present?", 
            choices=[(1, 'Yes'), (0, 'No')], coerce=int,
            validators=[InputRequired()])

    wants_equipment_moved = RadioField("*Would the customer like the equipment moved?", 
            choices=[(1, 'Yes'), (0, 'No')], coerce=int,
            validators=[InputRequired()])

    knows_where_equipment = RadioField("*Are you familiar with the location where the service line enters your home?", 
            choices=[(1, 'Yes'), (0, 'No')], coerce=int,
            validators=[InputRequired()])

    eth_present = RadioField("*Do you see a cord coming from the wall or from a service jack on the wall?", 
            choices=[(1, 'Yes'), (0, 'No')], coerce=int,
            validators=[InputRequired()])

    eth_in_port = RadioField("*Is that cord currently connected to a small box, roughly the size of a bar of soap? ", 
            choices=[(1, 'Yes'), (0, 'No')], coerce=int,
            validators=[InputRequired()])

    poe_light = RadioField("*Is there a light on the small box?", 
            choices=[(1, 'Yes'), (0, 'No')], coerce=int,
            validators=[InputRequired()])

    prev_cx_managed_router = RadioField("*Did the previous Tenant have a managed router?", 
            choices=[(1, 'Yes'), (0, 'No')], coerce=int,
            validators=[InputRequired()])
    cx_wants_router = RadioField("*Does this customer want a Nextlink Managed Router?",
            choices=[(1, 'Yes'), (0, 'No')], coerce=int,
            validators=[InputRequired()])


class OldAccQuest(FlaskForm):

        old_account_num = IntegerField("*Old Account Number",
                        validators=[InputRequired()])
        new_account_num = IntegerField("New Account Number (optional)")
    
        equipment_present = RadioField("*Is the POE Present?", 
                choices=[(1, 'Yes'), (0, 'No')], coerce=int,
                validators=[InputRequired()])
        approve_transfer = RadioField("*Does the account holder approve the transfer?", 
                choices=[(1, 'Yes'), (0, 'No')], coerce=int,
                validators=[InputRequired()])
        recent_service_issues = TextAreaField("Are there any recent service issues that you have been experiencing?(Leave blank if none)")

        currently_connected = RadioField("*Are you able to connect to the internet currently?",
                choices=[(1, 'Yes'), (0, 'No')], coerce=int,
                validators=[InputRequired()])

        knows_where_equipment = RadioField("*Are you familiar with the location where the service line enters your home?", 
                choices=[(1, 'Yes'), (0, 'No')], coerce=int,
                validators=[InputRequired()])

        eth_present = RadioField("*Do you see a cord coming from the wall or from a service jack on the wall?", 
                choices=[(1, 'Yes'), (0, 'No')], coerce=int,
                validators=[InputRequired()])

        eth_in_port = RadioField("*Is that cord currently connected to a small box, roughly the size of a bar of soap? ", 
                choices=[(1, 'Yes'), (0, 'No')], coerce=int,
                validators=[InputRequired()])

        poe_light = RadioField("*Is there a light on the small box?", 
                choices=[(1, 'Yes'), (0, 'No')], coerce=int,
                validators=[InputRequired()])
        has_managed_router = RadioField("*Do they have a managed router?",
                choices=[(1, 'Yes'), (0, 'No')], coerce=int,
                validators=[InputRequired()])
                

    