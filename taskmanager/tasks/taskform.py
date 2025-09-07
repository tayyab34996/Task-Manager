from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField, TextAreaField, SubmitField,DateTimeLocalField,SelectField
from wtforms.validators import DataRequired, Length,optional, ValidationError
from datetime import datetime

class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired(), Length(max=100)])
    duedate = DateTimeLocalField('Due Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(),optional(), Length(max=500)])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[DataRequired()])
    status = SelectField("Status", choices=[("pending", "Pending"), ("In Progress", "In Progress"), ("completed", "Completed"), ("Missed", "Missed")], default="pending")
    submit = SubmitField('Add Task')
    def validate_deadline(self, field):
        if field.data < datetime.now():
            raise ValidationError("Deadline cannot be in the past.")