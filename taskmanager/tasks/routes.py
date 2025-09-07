from flask import Blueprint, render_template,redirect, url_for,request,jsonify
from flask_login import current_user,login_required
from taskmanager.dbase.base import Session
from taskmanager.dbase.model import Task
from taskmanager.auth.register import RegisterForm
from .taskform import TaskForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename
session=Session()
task = Blueprint('task', __name__, template_folder='templates')
@task.route('/tasks/view', methods=['GET','POST'])
@login_required
def list_tasks():
    tasks = session.query(Task).filter_by(user=current_user.username).all()
    return render_template("listtask.html", tasks=tasks)
@task.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.task.data,
            user=current_user.username,
            date=form.duedate.data,
            description=form.description.data,
            priority=form.priority.data,
            status=form.status.data
        )
        if datetime.now() > new_task.date:
            new_task.status = "Missed"
        session.add(new_task)
        session.commit()
        return redirect(url_for('task.list_tasks'))
    return render_template("addtask.html", form=form)
@task.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = session.query(Task).filter_by(id=task_id, user=current_user.username).first()
    if task:
        session.delete(task)
        session.commit()
    return redirect(url_for('task.list_tasks'))
@task.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = session.query(Task).filter_by(id=task_id, user=current_user.username).first()
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.task.data
        task.date = form.duedate.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.id = task_id
        if datetime.now() > task.date:
            task.status = "Missed"
        session.commit()
        return redirect(url_for('task.list_tasks'))
    return render_template("edittask.html", form=form)
@login_required
@task.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    task = session.query(Task).get(task_id)
    if task:
        task.status = "Missed"
        session.commit()
        return {"success": True}
    return {"success": False}, 404
@login_required
@task.route('/mark_complete/<int:task_id>', methods=['GET'])
def mark_complete(task_id):
    task = session.query(Task).get(task_id)
    if task:
        task.status = "Completed"
        session.commit()
        return redirect(url_for('task.list_tasks'))
    return redirect(url_for('task.list_tasks'))
@login_required
@task.route('/mark_missed/<int:task_id>', methods=['GET'])
def mark_missed(task_id):
    task = session.query(Task).get(task_id)
    if task:
        task.status = "Missed"
        session.commit()
        return redirect(url_for('task.list_tasks'))
    return redirect(url_for('task.list_tasks'))