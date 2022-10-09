
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateField
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
    # already stored an existing phone ni=umber in the database

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

    def validate_roles(self, roles_assigned, assigned_project):
        """ check if roles are not asigned to CTO and Manager"""
        user_role = User.query.filter_by(user_roles='Manager').first()
        project_check = User.query.filter_by(assigned_project=assigned_project.data)
        if user_role:
            if project_check:
                raise ValidationError('CTO and Manager cannot be assigned projects!')

    def assigned_project_query():
        return Project.query

    

    firstname = StringField(label="First Name", validators=[Length(min=2, max=255), DataRequired()])
    lastname = StringField(label="Last Name", validators=[Length(min=2, max=255), DataRequired()])
    email = StringField(label="Email", validators=[Length(min=2, max=50), DataRequired()])
    username = StringField(label="Username", validators=[Length(min=2, max=20), DataRequired()])
    phone = StringField(label="Phone", validators=[Length(min=11, max=14), DataRequired()])
    assigned_project = QuerySelectField(query_factory=assigned_project_query, allow_blank=True, get_label='project_name')
    create = SubmitField()

class SearchForm2(FlaskForm):
    """ """
    searched = StringField(label="searched")
    Search = SubmitField(label="Search")


class Role_Details(FlaskForm):
    """form to hold the roles of each user"""
    role = StringField(label="Role", validators=[Length(min=2, max=14), DataRequired()])

