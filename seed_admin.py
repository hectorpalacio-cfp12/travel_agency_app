import os
from getpass import getpass
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from app import create_app
from models import db, User

load_dotenv()
app = create_app()

def main():
    with app.app_context():
        db.create_all()
        email = os.getenv("ADMIN_EMAIL") or input("Email admin: ").strip().lower()
        name = os.getenv("ADMIN_NAME") or input("Nombre admin: ").strip()
        password = os.getenv("ADMIN_PASSWORD") or getpass("Password admin: ")
        if User.query.filter_by(email=email).first():
            print("Ya existe un usuario con ese email.")
            return
        user = User(name=name, email=email, role="admin", password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print("Usuario admin creado:", email)

if __name__ == "__main__":
    main()
