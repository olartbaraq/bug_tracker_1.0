from ast import Delete
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Length, DataRequired, ValidationError
from main_files.db_models import User


class Project_Details(FlaskForm):
    project_name = StringField(label="Project Name", validators=[Length(min=2, max=255), DataRequired()])
    start_date = DateField(label='Start Date', validators=[DataRequired()])
    target_end_date = DateField(label='Target End Date', validators=[DataRequired()])
    create = SubmitField()
    

class Edit_Project_Details(FlaskForm):
    actual_end_date = DateField(label='Actual End Date', validators=[DataRequired()])
    Apply_Changes = SubmitField()

class Delete_Project_Details(FlaskForm):
    Delete = SubmitField()