from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.fields import EmailField 
from wtforms.validators import DataRequired, Email,EqualTo
from email_validator import validate_email
class LoginForm(FlaskForm):
    username = StringField(label='Username' ,validators=[DataRequired()]) 
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')
    def email_validator(self, email):
        try:
            valid = validate_email(email)
            return valid.email
        except Exception as e:
            raise ValueError(f"Invalid email: {e}")