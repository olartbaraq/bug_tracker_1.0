
from flask_wtf import FlaskForm
from flask import request
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateField, RadioField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Length, DataRequired, ValidationError
from main_files.db_models import User, Project



class Project_Details(FlaskForm):
    project_name = StringField(label="Project Name", validators=[Length(min=2, max=255), DataRequired()])
    start_date = DateField(label='Start Date', validators=[DataRequired()])
    target_end_date = DateField(label='Target End Date', validators=[DataRequired()])
    project_description = TextAreaField(label="Description", validators=[DataRequired()])
    create = SubmitField()
    

class Edit_Project_Details(FlaskForm):
    actual_end_date = DateField(label='Actual End Date', validators=[DataRequired()])
    Apply_Changes = SubmitField()

class SearchForm(FlaskForm):
    """ """
    searched = StringField(label="searched")
    Search = SubmitField(label="Search")

class User_Details(FlaskForm):
    """This creates a form to be stored in the database as a sign-up form details for users """

    # This function checks if the unique field email in the register form
    # to be filled by the user in the sign-up page of the website has
    # already stored an existing email address in the database

    def validate_email(self, email_to_check):
        """checks if email already existed """
        user_email = User.query.filter_by(email=email_to_check.data).first()
        if user_email:
            raise ValidationError('Email already exists!')


    # This function checks if the unique field phone number in the register form
    # to be filled by the user in the sign-up page of the website has
    # already stored an existing phone number in the database

    def validate_phone(self, phone_to_check):
        """checks if phone is already existed """
        user_phone = User.query.filter_by(phone=phone_to_check.data).first()
        if user_phone:
            raise ValidationError('Phone Number already exists!')

    def validate_username(self, username_to_check):
        """checks if phone is already existed """
        user_username = User.query.filter_by(username=username_to_check.data).first()
        if user_username:
            raise ValidationError('Username already exists!')


    def validate_roles_for_higher_up(form, field):
        """ check if roles are assigned to CTO and Manager"""
        roledatabase=['CTO', 'Manager']
        form = User_Details()
        for role in roledatabase:
            if form.user_roles.data == role:
                if form.assigned_project.data != None:
                    raise ValidationError('CTO or Manager cannot be assigned project!')
                    
    def validate_roles_for_lower_up(form, field):
        """ check if roles are not asigned to Lead and Member"""
        roledatabase=['Lead', 'Member']
        form = User_Details()
        for role in roledatabase:
            if form.user_roles.data == role:
                if form.assigned_project.data == None:
                    raise ValidationError('Lead or Member must be assigned project!')
    

    def assigned_project_query():
        return Project.query

    

    firstname = StringField(label="First Name", validators=[Length(min=2, max=255), DataRequired()])
    lastname = StringField(label="Last Name", validators=[Length(min=2, max=255), DataRequired()])
    email = StringField(label="Email", validators=[Length(min=2, max=50), DataRequired()])
    username = StringField(label="Username", validators=[Length(min=2, max=20), DataRequired()])
    phone = StringField(label="Phone", validators=[Length(min=11, max=14, message='Phone number must be between 11 and 14 characters'), DataRequired()])
    assigned_project = QuerySelectField(query_factory=assigned_project_query, allow_blank=True, get_label='project_name', validators=[validate_roles_for_lower_up])
    user_roles = RadioField(choices=[('CTO','CTO'),('Manager','Manager'),('Lead','Lead'),('Member','Member')],validators=[DataRequired(), validate_roles_for_higher_up])
    create = SubmitField()


class Edit_User_details(FlaskForm):
    """ """
    user_roles = RadioField(choices=[('CTO','CTO'),('Manager','Manager'),('Lead','Lead'),('Member','Member')], validators=[DataRequired(), User_Details.validate_roles_for_higher_up, User_Details.validate_roles_for_lower_up])
    assigned_project = QuerySelectField(query_factory=User_Details.assigned_project_query, allow_blank=True, get_label='project_name')
    save = SubmitField()
    

class SearchForm2(FlaskForm):
    """ """
    searched = StringField(label="searched")
    Search = SubmitField(label="Search")

