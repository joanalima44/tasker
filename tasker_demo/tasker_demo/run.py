from app import create_app
from app.models import db 

from app.models.user import User
from app.models.project import Project
from app.models.task import Task

from werkzeug.security import generate_password_hash

app = create_app()

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        if not User.query.filter_by(email="admin@example.com").first():
            admin = User(
                name="Admin",
                email="admin@example.com",
                password_hash=generate_password_hash("admin123"),
            )
            db.session.add(admin)
            db.session.commit()

        print("\n✅ Banco recriado com sucesso!")
        print("   Usuário opcional: admin@example.com / admin123")

if __name__ == "__main__":
    app.run(debug=True)
