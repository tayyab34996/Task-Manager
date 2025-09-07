from flask import Flask
from flask_login import LoginManager
from taskmanager.main.routes import main
from taskmanager.tasks.routes import task
from taskmanager.auth.routes import authen
from taskmanager.dbase.model import NewUser
from taskmanager.dbase.base import Session, create_tables
import os
from datetime import timedelta
def create_app():
    app= Flask(__name__)
    app.secret_key= '2342ersdfae368564asdfgwerw36853549583dgdgs'
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "taskmanager_uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    create_tables()
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.logina'
    @login_manager.user_loader
    def load_user(user_id):
        db = Session()
        try:
            return db.get(NewUser, int(user_id))
        finally:
            db.close()

        db.close()

    app.register_blueprint(main)
    app.register_blueprint(authen)
    app.register_blueprint(task)
    return app