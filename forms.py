from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, BooleanField, RadioField
from wtforms import validators
from wtforms.validators import DataRequired, InputRequired, Length


class UserForm(FlaskForm):

        username = StringField("Billmax Username",
                validators=[InputRequired()])
        password = PasswordField("A password of your choosing",
                validators=[Length(min=6, message="Password must be at least six characters long")])


class NewAccQuest(FlaskForm):

        account_number = IntegerField("*Account Number",
                validators=[InputRequired()])

        account_name = StringField("*Account Name",
                validators=[InputRequired()])

        phone_number = StringField("Best Callback",
                validators=[InputRequired()])
        
        old_account_num = IntegerField("Old Account Number")

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
        transfer_when = StringField("*When would the customer like for us to complete the transfer? Please take into account when they will be physically in the house tob verify connection",
                validators=[InputRequired(message="Please put n/a if not known")])

        cx_wants_router = RadioField("*Does this customer want a Nextlink Managed Router?",
                choices=[(1, 'Yes'), (0, 'No')], coerce=int,
                validators=[InputRequired()])
        need_router_ship = RadioField("*Do we need to ship a router? Please review old account and see if a managed router is there already", 
                choices=[(1, 'Yes'), (0, 'No')], coerce=int)
        wifi_ssid = StringField("*What would they like their Wi-Fi network to be called?")

        wifi_pw = StringField("*What would they like their Wi-Fi password to be?")

class OldAccQuest(FlaskForm):

        account_number = IntegerField("*Account Number",
                validators=[InputRequired()])

        account_name = StringField("*Account Name",
                validators=[InputRequired()])
        new_account_num = IntegerField("New Account Number, if available")
                        
        phone_number = StringField("Best Callback",
                validators=[InputRequired()])
    
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
                

    