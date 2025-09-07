from flask import Blueprint,flash
from taskmanager.dbase.base import Session
from taskmanager.dbase.model import NewUser
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
from .login import LoginForm
from .register import RegisterForm
authen = Blueprint('auth', __name__,template_folder='templates')
session=Session()
def register_user(username, fullname, email, password):
    new_user = NewUser(username=username, fullname=fullname, email=email, password=password)
    session.add(new_user)
    session.commit()
    return new_user
@authen.route('/', methods=['GET', 'POST'])
@authen.route('/register', methods=['GET', 'POST'])
def registera():
    form= RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        fullname = form.fullname.data
        email = form.email.data
        password = form.password.data
        user=session.query(NewUser).filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.registera'))
        register_user(username, fullname, email, password)
        return redirect(url_for('auth.logina'))
    print("Errors:", form.errors)
    return render_template('register.html', form=form)

@authen.route('/login', methods=['GET', 'POST'])
def logina():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = session.query(NewUser).filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=True)
            flash('Login successful!')
            return redirect(url_for('main.home'))
        flash('Invalid username or password')
        return redirect(url_for('auth.logina'))
    return render_template('login.html', form=form)
@authen.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.logina'))
