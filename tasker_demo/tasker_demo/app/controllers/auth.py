from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import db
from ..models.user import User
from ..forms.auth_forms import LoginForm, RegisterForm, ChangePasswordForm

bp = Blueprint("auth", __name__, template_folder="../views/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password_hash, form.password.data):
            flash("Credenciais inválidas.", "danger")
            return render_template("auth/login.html", form=form)
        login_user(user)
        flash("Bem-vindo!", "success")
        return redirect(url_for("projects.list_projects"))
    return render_template("auth/login.html", form=form)

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email já cadastrado.", "warning")
            return render_template("auth/register.html", form=form)
        user = User(name=form.name.data, email=form.email.data,
                    password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash("Conta criada. Faça login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("auth.login"))

@bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, form.current_password.data):
            flash("Senha atual incorreta.", "danger")
            return render_template("auth/change_password.html", form=form)
        from werkzeug.security import generate_password_hash
        current_user.password_hash = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash("Senha alterada com sucesso.", "success")
        return redirect(url_for("projects.list_projects"))
    return render_template("auth/change_password.html", form=form)
