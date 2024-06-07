#!/usr/bin/python3

"""
"""
from . import db  # login_manager
from datetime import datetime

# from main_files import bcrypt, app
# from flask_login import UserMixin, current_user


class Project(db.Model):
    __table_args__ = {"extend_existing": True}
    """class that defines the fields to store projects info in the database 
    """
    project_id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String(255), unique=True, nullable=False)
    project_description = db.Column(db.String(3000), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    target_end_date = db.Column(db.DateTime, nullable=False)
    actual_end_date = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    date_modified_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    record_created_by = db.Column(db.String(100), nullable=False, default="admin")
    record_modified_by = db.Column(db.String(100), nullable=False, default="admin")

    def __repr__(self):
        return "{}".format(self.project_name)

    @property
    def only_date(self):
        """ """
        datetime_element = self.target_end_date
        date_element = datetime_element.strftime("%d/%m/%Y")
        return date_element

    @property
    def start_only_date(self):
        """ """
        datetime_element = self.start_date
        date_element = datetime_element.strftime("%d/%m/%Y")
        return date_element

    @property
    def actual_date(self):
        """ """
        if self.actual_end_date is None:
            return "-"
        else:
            datetime_element = self.actual_end_date
            date_element = datetime_element.strftime("%d/%m/%Y")
            return date_element

    @property
    def create_date(self):
        """ """
        datetime_element = self.date_created
        date_element = datetime_element.strftime("%d/%m/%Y")
        return date_element

    @property
    def modify_date(self):
        """ """
        datetime_element = self.date_modified_on
        date_element = datetime_element.strftime("%d/%m/%Y")
        return date_element


class User(db.Model):
    __table_args__ = {"extend_existing": True}
    """class that defines the fields to store users in the database """
    user_id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(14), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    assigned_project = db.Column(db.String(250), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    date_modified_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    record_created_by = db.Column(db.String(100), nullable=False, default="admin")
    record_modified_by = db.Column(db.String(100), nullable=False, default="admin")
    user_roles = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return "{}".format(self.username)


class Role(db.Model):
    __table_args__ = {"extend_existing": True}
    """class that defines the fields which roles users are 
    assigned to in the database """
    id = db.Column(db.Integer(), primary_key=True)
    assigned_role = db.Column(db.String(10), nullable=False)
    user_role = db.Column(db.String(25), db.ForeignKey("user.user_id"))
    assigned_project_to_user = db.Column(
        db.String(250), db.ForeignKey("project.project_id")
    )


class Issues(db.Model):
    __table_args__ = {"extend_existing": True}
    """class that defines the fields which issues users are 
    assigned to in the database """
    id = db.Column(db.Integer(), primary_key=True)
    issue_summary = db.Column(db.String(300), nullable=False)
    issue_description = db.Column(db.String(5000), nullable=False)
    identified_by_person_id = db.Column(db.String(50), nullable=False)
    identified_date = db.Column(db.DateTime, nullable=False)
    related_project = db.Column(db.String(255), nullable=False)
    assigned_to = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    priority = db.Column(db.String(30), nullable=False)
    traget_resolution_date = db.Column(db.DateTime, nullable=False)
    progress = db.Column(db.String(4000), nullable=False)
    actual_resolution_date = db.Column(db.DateTime, nullable=True)
    resolution_summary = db.Column(db.String(4000), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    date_modified_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    record_created_by = db.Column(db.String(100), nullable=False, default="admin")
    record_modified_by = db.Column(db.String(100), nullable=False, default="admin")

    @property
    def iden_date(self):
        """ """
        datetime_element = self.identified_date
        date_element = datetime_element.strftime("%d/%m/%Y")
        return date_element

    @property
    def resolute_date(self):
        """ """
        datetime_element = self.traget_resolution_date
        date_element = datetime_element.strftime("%d/%m/%Y")
        return date_element

    @property
    def f_resolute_date(self):
        """ """
        datetime_element = self.actual_resolution_date
        date_element = datetime_element.strftime("%d/%m/%Y")
        return date_element

    @property
    def assigned_or_not(self):
        """ """
        if self.assigned_to == "None":
            return "Unassigned"
        else:
            return self.assigned_to
