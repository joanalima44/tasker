from . import db

class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    is_archived = db.Column(db.Boolean, default=False)

    tasks = db.relationship("Task", backref="project", cascade="all, delete-orphan")
