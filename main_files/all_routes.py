#!/usr/bin/python3

"""
Starts a Flash web Application for a rabbit marketplace

"""
from datetime import datetime
from main_files.db_models import Project, Role, User, Issues
from main_files import app
from main_files.db_models import db
from flask import render_template, url_for, redirect, request, flash,jsonify
from flask_login import login_user, logout_user, login_required, current_user
from main_files.forms_input import Project_Details, Edit_Project_Details, SearchForm, SearchForm3, User_Details, SearchForm2, Edit_User_details, Issue_Details, Edit_Issue_Details


@app.route('/')
@app.route('/home')
def home_page():
    """a route to return the website homepage"""
    return render_template('home.html')

@app.route('/logout')
def logout_page():
    """a route to return the website logout"""
    # logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))


@app.route('/dashboard')
def dashboard_page():
    """a route to return the website dashboard"""
    return render_template('dashboard.html')


@app.context_processor
def base():
    form3 = SearchForm()
    return dict(form=form3)


@app.route('/projects', methods=['GET', 'POST'])
def projects_page():
    """a route to return the website projects"""

    form3 = SearchForm()
    all_projects = Project.query.order_by(Project.date_created.desc()).limit(20)
    searched_projects = Project.query

    if form3.validate_on_submit():
        ad_search = form3.searched.data
        searched_projects = searched_projects.filter(Project.project_description.like('%' + ad_search + '%'))
        searched_projects = searched_projects.order_by(Project.project_name).all()
        flash("your search returned listed projects", category='info')
        return render_template('projects.html', all_projects=all_projects, form3=form3, searched=ad_search, searched_projects=searched_projects)
    return render_template('projects.html', all_projects=all_projects, form3=form3)


@app.route('/project-details', methods=['GET', 'POST'])
def project_details_page():
    """a route to return the website project details"""
    form = Project_Details()
    if request.method == 'POST':
        if form.validate_on_submit():
            project_to_create = Project(project_name=form.project_name.data,
                                  start_date=form.start_date.data,
                                  project_description=form.project_description.data,
                                  target_end_date=form.target_end_date.data)
            db.session.add(project_to_create)
            db.session.commit()
            flash("project added Sucessfully", category='info')
            return redirect(url_for('projects_page')) 
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash("Error: {}".format(err_msg), category='danger')
    return render_template('project-details.html', form=form)


@app.route('/project-details/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_projects(project_id):
    """a route to edit individual project page"""
    
    indy_project = Project.query.get_or_404(project_id)
    form = Project_Details()
    form2 = Edit_Project_Details()
         
    if request.method == 'POST':
        if form2.validate_on_submit():
            indy_project.project_name=form.project_name.data
            indy_project.start_date=form.start_date.data
            indy_project.target_end_date=form.target_end_date.data
            indy_project.actual_end_date=form2.actual_end_date.data
            indy_project.date_modified_on=datetime.utcnow()
            db.session.add(indy_project)
            db.session.commit()
            flash("Project Updated Sucessfully", category='info')
            return redirect(url_for('projects_page'))
    form.project_name.data = indy_project.project_name
    form.start_date.data = indy_project.start_date
    form.target_end_date.data = indy_project.target_end_date
    form2.actual_end_date.data = indy_project.actual_end_date
    all_projects = Project.query.order_by(Project.date_created)
    return render_template('edit-individual-project.html', form=form, form2=form2, indy_project=indy_project, project_id=indy_project.project_id, all_projects=all_projects)


@app.route('/projects/delete/<int:project_id>', methods=['GET', 'DELETE'])
def delete_project(project_id):
    """Delete a project"""
    indy_project = Project.query.get_or_404(project_id)
    try:
        db.session.delete(indy_project)
        db.session.commit()
        flash('Project Deleted successfully', category='info')
        # all_projects = Project.query.order_by(Project.date_created)
        return render_template('projects.html') # all_projects=all_projects)

    except:
        flash("whoops! There was a problem deleting the project from database")
        # all_projects = Project.query.order_by(Project.date_created)
        return render_template('projects.html') # all_projects=all_projects)


@app.route('/reports')
def reports_page():
    """a route to return the projects reports on issues opened or closed"""
    return ('<h5> reports_page </h5>')


@app.context_processor
def base_user():
    form3 = SearchForm2()
    return dict(form=form3)


@app.route('/users', methods=['GET', 'POST'])
def users_page():
    """a route to return the all users"""
    form3 = SearchForm2()
    all_users = User.query.order_by(User.date_created.desc()).limit(20)
    searched_users = User.query
      
    if form3.validate_on_submit():
        ad_search = form3.searched.data
        searched_users = searched_users.filter(User.assigned_project.like('%' + ad_search + '%'))
        searched_users = searched_users.order_by(User.username).all()
        flash("your search returned listed users on the project", category='info')
        return render_template('users.html', all_users=all_users, form3=form3, searched=ad_search, searched_users=searched_users)
    return render_template('users.html', all_users=all_users, form3=form3)


@app.route('/User-Details', methods=['GET', 'POST'])
def user_info_page():
    """a route to return the website users details"""
    form = User_Details()
    # form.assigned_project.choices = [(project.project_id, project.project_name) for project in Project.query.order_by(Project.project_name).all()]
    if request.method == 'POST':
        if form.validate_on_submit():
            # user_answer = request.form['role_taken']
            user_to_create = User(firstname=form.firstname.data,
                                    lastname=form.lastname.data,
                                    email=form.email.data,
                                    username=form.username.data,
                                    phone=form.phone.data,
                                    assigned_project=form.assigned_project.data.__repr__(),
                                    user_roles=form.user_roles.data)

            role_to_create = Role(assigned_role=user_to_create.user_roles,
                                  user_role=user_to_create.username,
                                  assigned_project_to_user=user_to_create.assigned_project)
            db.session.add_all([user_to_create, role_to_create])
            db.session.commit()
            flash("User added Sucessfully", category='info')
            return redirect(url_for('users_page')) 
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash("Error: {}".format(err_msg), category='danger')
    return render_template('user-info.html', form=form)


@app.route('/user-info/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """a route to edit individual project page"""

    each_user = User.query.get_or_404(user_id)
    form = User_Details()
    form2 = Edit_User_details()

    if request.method == 'POST':
        if form2.validate_on_submit():
            each_user.lastname=form.lastname.data
            each_user.firstname=form.firstname.data
            each_user.email=form.email.data
            each_user.username=form.username.data
            each_user.phone=form.phone.data
            each_user.assigned_project=form2.assigned_project.data.__repr__()
            each_user.user_roles=form2.user_roles.data
            db.session.add(each_user)
            db.session.commit()
            flash("User Updated Sucessfully", category='info')
            return redirect(url_for('users_page'))
    elif form.errors != {}:
        for err_msg in form.errors.values():
            flash("Error: {}".format(err_msg), category='danger')
    
    form.lastname.data =  each_user.lastname
    form.firstname.data =  each_user.firstname
    form.email.data =  each_user.email
    form.username.data =  each_user.username
    form.phone.data =  each_user.phone
    form2.assigned_project.data =  each_user.assigned_project
    form2.user_roles.data =  each_user.user_roles

    return render_template('edit-user-page.html', form=form, form2=form2, user_id=each_user.user_id, each_user=each_user)


@app.route('/users/delete/<int:user_id>', methods=['GET', 'DELETE'])
def delete_user(user_id):
    """Delete a project"""
    each_user = User.query.get_or_404(user_id)
    try:
        db.session.delete(each_user)
        db.session.commit()
        flash('Project Deleted successfully', category='info')
        all_users = User.query.order_by(User.date_created)
        return render_template('users.html', all_users=all_users, each_user=each_user)

    except:
        flash("whoops! There was a problem deleting the project from database")
        all_users = User.query.order_by(User.date_created)
        return render_template('users.html', all_users=all_users, each_user=each_user)

    finally:
        return render_template('users.html', all_users=all_users, each_user=each_user)


@app.context_processor
def base_issue():
    form = SearchForm3()
    return dict(form=form)


@app.route('/issues', methods=['GET', 'POST'])
def issues_page():
    """ page to display all issues related to assigned project"""

    form = SearchForm3()
    all_issues = Issues.query.order_by(Issues.date_created.desc()).limit(20)
    searched_issues = Issues.query
      
    if form.validate_on_submit():
        ad_search = form.searched.data
        searched_issues = searched_issues.filter(Issues.issue_summary.like('%' + ad_search + '%'))
        searched_issues = searched_issues.order_by(Issues.status).all()
        flash("your search returned listed issues by status", category='info')
        return render_template('issues.html',  all_issues=all_issues, form=form, searched=ad_search, searched_issues=searched_issues)
    return render_template('issues.html', all_issues=all_issues, form=form)


@app.route('/Isssue-Details', methods=['GET', 'POST'])
def issue_info_page():
    """a route to return the website users details"""
    form = Issue_Details()
    
    form.related_project.choices = [(project.project_id, project.project_name) for project in Project.query.all()]
    form.assigned_to.choices = [(user.user_id, user.username) for user in User.query.all()]
    # form.assigned_to.choices = [(user.user_id, user.username) for user in User.query.filter_by(assigned_project=form.related_project.data.__repr__()).all()]
    print(form.assigned_to.choices)
    if request.method == 'POST':
        Issue_proj = Project.query.filter_by(project_id=form.related_project.data).first()
        Issue_name = User.query.filter_by(user_id=form.assigned_to.data).first()

        if form.validate_on_submit():
            issue_to_create = Issues(issue_summary=form.issue_summary.data,
                                     issue_description=form.issue_description.data,
                                     identified_by_person_id=form.identified_by.data.__repr__(),
                                     identified_date=form.identified_date.data,
                                     related_project=Issue_proj.project_name,
                                     assigned_to=Issue_name.username,
                                     status=form.status.data,
                                     priority=form.priority.data,
                                     traget_resolution_date=form.target_resolution_date.data,
                                     progress=form.progress_report.data)
            db.session.add(issue_to_create)
            db.session.commit()
            flash("Issue added Sucessfully", category='info')
            return redirect(url_for('issues_page')) 
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash("Error: {}".format(err_msg), category='danger')
    return render_template('issue-details.html', form=form)


@app.route('/issues/<project>')
def issue(project):
    allUsers = User.query.filter_by(assigned_project=project).all()
    userArray = []
    for user in allUsers:
        userObj = {}
        userObj['user_id'] = user.user_id
        userObj['username'] = user.username
        userArray.append(userObj)
    return jsonify({'allUsers': userArray})


@app.route('/issue-info/edit/<int:issue_id>', methods=['GET', 'POST'])
def edit_issue_page(issue_id):
    """a route to edit individual project page"""

    each_issue = Issues.query.get_or_404(issue_id)
    form = Issue_Details()
    form2 = Edit_Issue_Details()

    if request.method == 'POST':
        if form2.validate_on_submit():
            each_issue.issue_summary=form.issue_summary.data
            each_issue.issue_description=form.issue_description.data
            each_issue.identified_by_person_id=form.identified_by.data.__repr__()
            each_issue.identified_date=form.identified_date.data
            each_issue.related_project=form.related_project.data.__repr__()
            each_issue.assigned_to=form.assigned_to.data.__repr__()
            each_issue.status=form.status.data
            each_issue.priority=form.priority.data
            each_issue.traget_resolution_date=form.target_resolution_date.data
            each_issue.progress=form.progress_report.data
            each_issue.actual_resolution_date=form2.actual_resolution_date.data
            each_issue.resolution_summary=form2.resolution_summary.data
            db.session.add(each_issue)
            db.session.commit()
            flash("Issue Updated Sucessfully", category='info')
            return redirect(url_for('issues_page'))
    elif form.errors != {}:
        for err_msg in form.errors.values():
            flash("Error: {}".format(err_msg), category='danger')
    
    form.issue_summary.data=each_issue.issue_summary
    form.issue_description.data=each_issue.issue_description
    form.identified_by.data = User.query.filter_by(username=each_issue.identified_by_person_id).first()
    form.identified_date.data=each_issue.identified_date
    form.related_project.data=Project.query.filter_by(project_name=each_issue.related_project).first()
    form.assigned_to.data=User.query.filter_by(username=each_issue.assigned_to).first()
    form.status.data=each_issue.status
    form.priority.data=each_issue.priority
    form.target_resolution_date.data=each_issue.traget_resolution_date
    form.progress_report.data=each_issue.progress

    return render_template('issue-summary-by-project.html', form=form, form2=form2, issue_id=each_issue.id, each_issue=each_issue)


@app.route('/issues/delete/<int:issue_id>', methods=['GET', 'DELETE'])
def delete_issue_page(issue_id):
    """Delete a project"""
    each_issue = Issues.query.get_or_404(issue_id)
    try:
        db.session.delete(each_issue)
        db.session.commit()
        flash('Issue Deleted successfully', category='info')
        all_issues = Issues.query.order_by(Issues.date_created).all()
        return render_template('issues.html', all_issues=all_issues, each_issue=each_issue)

    except:
        flash("whoops! There was a problem deleting the project from database")
        all_issues = Issues.query.order_by(Issues.date_created).all()
        return render_template('issues.html', all_issues=all_issues, each_issue=each_issue)