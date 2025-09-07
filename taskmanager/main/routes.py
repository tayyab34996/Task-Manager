from flask import Blueprint, render_template,redirect, url_for,jsonify,request, current_app,send_from_directory
from flask_login import current_user,login_required
from taskmanager.dbase.base import Session
from taskmanager.dbase.model import  NewUser, Task
from taskmanager.auth.register import RegisterForm
import requests
import os, uuid
from werkzeug.utils import secure_filename
main = Blueprint('main', __name__, template_folder='templates')
session = Session()
@main.route('/about')
@login_required
def about():
    return render_template("about.html")
@main.route('/home', methods=['GET'])
@login_required     
def home():
    tasks = session.query(Task).filter(Task.user == current_user.username).all()
    tasks_high = [task for task in tasks if task.priority == 'high' and task.status != "Completed" and task.status != "Missed"]
    tasks_midlow = [task for task in tasks if task.priority in ['medium', 'low']]
    quote = "The secret to getting ahead is getting started."
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            quote = f"{data['q']} — {data['a']}"
    except Exception as e:
        print("Quote API error:", e)

    return render_template( "home.html", tasks_midlow=tasks_midlow, tasks_high=tasks_high, tasks=tasks, quote=quote )
@main.route('/profile/<username>',methods=['GET'])
@login_required
def profile(username):
    form = RegisterForm()
    user = session.query(NewUser).filter(NewUser.username == username).first()
    if user:
     return render_template('profilepage.html', form=form, user=user)
    return redirect(url_for('main.home'))
@main.route('/api/tasks/<int:task_id>/miss', methods=['POST'])
@login_required
def mark_task_missed(task_id):
    task = session.get(Task, task_id)
    if task and task.user == current_user.username and task.status != "completed":
        task.status = "Missed"
        session.commit()
        return {"success": True}
    return {"success": False, "error": "Task not found or already completed"}
@main.route("/api/profile/<username>", methods=["POST"])
@login_required
def update_profile(username):
    user = session.query(NewUser).filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update text fields
    user.address = request.form.get("address")
    user.about_me = request.form.get("about_me")
    user.gender = request.form.get("gender")
    user.dateofBirth = request.form.get("dateofbirth")  # match your DB column

    # Handle profile picture upload
    file = request.files.get("profile_pic")  # ✅ match input name
    if file and file.filename != "":
        upload_folder = os.path.join(current_app.root_path, "uploads", "profile_pics")
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"

        filepath = os.path.join(upload_folder, unique_name)
        file.save(filepath)

        user.profilePicture = unique_name  # ✅ store correct filename

    session.commit()
    return jsonify({"message": "Profile updated!"})


@main.route("/uploads/profile_pics/<filename>")
@login_required
def get_profile_pic(filename):
    upload_folder = os.path.join(current_app.root_path, "uploads", "profile_pics")
    return send_from_directory(upload_folder, filename)