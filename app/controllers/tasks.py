from flask import Blueprint, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from ..models.task import Task
from ..models.project import Project
from ..models import db
from ..forms.task_forms import TaskForm
import bleach

bp = Blueprint("tasks", __name__, template_folder="../views/tasks")

def _ensure_project_owner(project_id: int):
    """Levanta 404 se não existe e 403 se não é do usuário logado."""
    project = Project.query.get_or_404(project_id)
    if getattr(project, "user_id", None) != current_user.id:
        abort(403)
    return project

@bp.route("/tasks", methods=["POST"])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        project_id = int(form.project_id.data)
        _ensure_project_owner(project_id) 

        t = Task(
            title=form.title.data.strip(),
            description=bleach.clean(form.description.data or "", strip=True),
            project_id=project_id,
            status="todo",
            position=0,
        )
        db.session.add(t)
        db.session.commit()
        flash("Tarefa criada.", "success")
    else:
        flash("Erro ao criar tarefa.", "danger")

    return redirect(url_for("projects.project_board", project_id=form.project_id.data))

@bp.route("/tasks/<int:task_id>/move", methods=["PATCH"])
@login_required
def move_task(task_id):
    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    new_pos = data.get("position", 0)

    if new_status not in ("todo", "doing", "done"):
        return jsonify({"error": "status inválido"}), 400

    task = Task.query.get_or_404(task_id)

    project = Project.query.get_or_404(task.project_id)
    if getattr(project, "user_id", None) != current_user.id:
        abort(403)

    try:
        task.status = new_status
        task.position = int(new_pos)
        db.session.commit()
        return jsonify({"ok": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "não foi possível mover a tarefa"}), 400
