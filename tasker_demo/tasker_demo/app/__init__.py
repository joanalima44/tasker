from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from .models import db
from .models.user import User

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__, template_folder="views", static_folder="static")
    app.config.from_object("config.Config")

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from .controllers.auth import bp as auth_bp
    from .controllers.projects import bp as projects_bp
    from .controllers.tasks import bp as tasks_bp
    from .controllers.api import bp as api_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        from flask_login import current_user
        from flask import redirect, url_for
        if current_user.is_authenticated:
            return redirect(url_for("projects.list_projects"))
        return redirect(url_for("auth.login"))

    return app
