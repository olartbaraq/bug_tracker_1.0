from db_models import Project, Role, User, Issues
from db_models import db
import sqlite3
from sqlalchemy import text


def do_query(my_query):

    my_query = text('SELECT firstname, lastname, assigned_project, email, username, role FROM User INNER JOIN Role ON User.username = Role.user')
    result = db.session.execute(my_query)
    names = [row[0] for row in result]
    print(names)