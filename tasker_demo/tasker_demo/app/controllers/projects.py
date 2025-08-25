from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..models.project import Project
from ..models import db

bp = Blueprint("projects", __name__, template_folder="../views/projects")

def _ensure_owner(project_id: int) -> Project:
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        abort(403)
    return project

@bp.route("/projects")
@login_required
def list_projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template("projects/index.html", projects=projects)

@bp.route("/projects/<int:project_id>")
@login_required
def project_board(project_id):
    from ..models.task import Task
    project = _ensure_owner(project_id)
    tasks = Task.query.filter_by(project_id=project_id).order_by(Task.status, Task.position).all()
    columns = {"todo": [], "doing": [], "done": []}
    for t in tasks:
        columns[t.status].append(t)
    return render_template("projects/board.html", project=project, columns=columns)

@bp.post("/projects")
@login_required
def create_project():
    name = (request.form.get("name") or "").strip()
    if not name:
        flash("Nome do projeto é obrigatório.", "danger")
        return redirect(url_for("projects.list_projects"))

    p = Project(name=name, user_id=current_user.id)
    db.session.add(p)
    db.session.commit()
    flash("Projeto criado.", "success")
    return redirect(url_for("projects.project_board", project_id=p.id))
