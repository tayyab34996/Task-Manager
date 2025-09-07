from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, DateField, SelectField
from wtforms.fields import EmailField 
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email,EqualTo
from email_validator import validate_email
class RegisterForm(FlaskForm):
    username = StringField(label='Username' ,validators=[DataRequired()]) 
    fullname = StringField(label='Full Name', validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    dateofbirth = DateField(label='Date of Birth', format='%Y-%m-%d')
    gender = SelectField(label='Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    about_me = TextAreaField(label='About Me')
    address = StringField(label='Address')
    profilepic = FileField(label='Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirmPassword = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField(label='Create Account')
    def email_validator(self, email):
        try:
            valid = validate_email(email)
            return valid.email
        except Exception as e:
            raise ValueError(f"Invalid email: {e}")