from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Accepts a nickname and a receiver."""
    name = StringField('Name', validators=[DataRequired()])
    receiver = StringField('receiver', validators=[DataRequired()])
    submit = SubmitField('Enter Chatroom')
