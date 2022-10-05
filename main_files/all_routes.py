#!/usr/bin/python3

"""
Starts a Flash web Application for a rabbit marketplace

"""
from datetime import datetime
from main_files.db_models import Project
from main_files import app
from main_files.db_models import db
from flask import render_template, url_for, redirect, request, flash,jsonify
from flask_login import login_user, logout_user, login_required, current_user
from main_files.forms_input import Project_Details, Edit_Project_Details, SearchForm

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
        searched_projects = searched_projects.filter(Project.project_name.like('%' + ad_search + '%'))
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



@app.route('/issues')
def issues_page():
    """a route to return the projects issues"""
    return ('<h5> issues_page </h5>')

@app.route('/reports')
def reports_page():
    """a route to return the projects reports on issues opened or closed"""
    return ('<h5> reports_page </h5>')

@app.route('/users')
def users_page():
    """a route to return the all users"""
    return ('<h5> users_page </h5>')
