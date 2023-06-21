from wtforms import Form, StringField, EmailField, validators, SubmitField
from wtforms.validators import DataRequired


class UserForm(Form):
    name = StringField('Name', [validators.length(min=4, max=25)] )
    username = StringField('Username', [validators.length(min=4, max=25)])
    email = EmailField('Email', [validators.Email()])
    submit = SubmitField('Submit')