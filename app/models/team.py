from . import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User")

class TeamMembership(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), primary_key=True)
    role = db.Column(db.String(20), default="member")
