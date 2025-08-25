from flask import Blueprint, request, jsonify, current_app
from ..models.user import User
from werkzeug.security import check_password_hash
import jwt, datetime

bp = Blueprint("api", __name__)

@bp.post("/login")
def api_login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401
    payload = {
        "sub": user.id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        "iss": "tasker-demo"
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")
    return jsonify({"token": token})
