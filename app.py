import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Tour, Booking
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "cambia-esto")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()


    # Rutas de autenticación
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form.get("name","").strip()
            email = request.form.get("email","").strip().lower()
            password = request.form.get("password","")
            if not name or not email or not password:
                flash("Completa todos los campos", "error")
                return redirect(url_for("register"))
            if User.query.filter_by(email=email).first():
                flash("Ese email ya está registrado", "error")
                return redirect(url_for("register"))
            user = User(name=name, email=email, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Registro exitoso. Ahora inicia sesión.", "success")
            return redirect(url_for("login"))
        return render_template("register.html")

    @app.route("/login", methods=["GET","POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email","").strip().lower()
            password = request.form.get("password","")
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash("Bienvenido/a", "success")
                return redirect(url_for("dashboard"))
            flash("Credenciales inválidas", "error")
        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Sesión cerrada", "info")
        return redirect(url_for("login"))

    @app.route("/")
    @login_required
    def dashboard():
        tours = Tour.query.order_by(Tour.start_date.asc()).limit(5).all()
        my_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).limit(5).all()
        return render_template("dashboard.html", tours=tours, bookings=my_bookings)

    # ---- TOURS (solo admin) ----
    def admin_required():
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Requiere rol administrador.", "error")
            return False
        return True

    @app.route("/tours")
    @login_required
    def tours_list():
        tours = Tour.query.order_by(Tour.start_date.desc()).all()
        return render_template("tours_list.html", tours=tours)

    @app.route("/tours/new", methods=["GET","POST"])
    @login_required
    def tours_new():
        if not admin_required():
            return redirect(url_for("tours_list"))
        if request.method == "POST":
            name = request.form.get("name","").strip()
            destination = request.form.get("destination","").strip()
            description = request.form.get("description","").strip()
            price = float(request.form.get("price","0") or 0)
            start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date()
            end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date()
            capacity = int(request.form.get("capacity","0") or 0)
            tour = Tour(name=name, destination=destination, description=description, price=price,
                        start_date=start_date, end_date=end_date, capacity=capacity)
            db.session.add(tour)
            db.session.commit()
            flash("Tour creado", "success")
            return redirect(url_for("tours_list"))
        return render_template("tour_form.html", tour=None)

    @app.route("/tours/<int:tour_id>/edit", methods=["GET","POST"])
    @login_required
    def tours_edit(tour_id):
        if not admin_required():
            return redirect(url_for("tours_list"))
        tour = Tour.query.get_or_404(tour_id)
        if request.method == "POST":
            tour.name = request.form.get("name","").strip()
            tour.destination = request.form.get("destination","").strip()
            tour.description = request.form.get("description","").strip()
            tour.price = float(request.form.get("price","0") or 0)
            tour.start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date()
            tour.end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date()
            tour.capacity = int(request.form.get("capacity","0") or 0)
            db.session.commit()
            flash("Tour actualizado", "success")
            return redirect(url_for("tours_list"))
        return render_template("tour_form.html", tour=tour)

    @app.route("/tours/<int:tour_id>/delete", methods=["POST"])
    @login_required
    def tours_delete(tour_id):
        if not admin_required():
            return redirect(url_for("tours_list"))
        tour = Tour.query.get_or_404(tour_id)
        db.session.delete(tour)
        db.session.commit()
        flash("Tour eliminado", "info")
        return redirect(url_for("tours_list"))

    # ---- RESERVAS ----
    @app.route("/bookings")
    @login_required
    def bookings_list():
        if current_user.is_admin():
            bookings = Booking.query.order_by(Booking.created_at.desc()).all()
        else:
            bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
        return render_template("bookings_list.html", bookings=bookings)

    @app.route("/bookings/new/<int:tour_id>", methods=["POST"])
    @login_required
    def bookings_new(tour_id):
        tour = Tour.query.get_or_404(tour_id)
        pax = int(request.form.get("pax","1") or 1)
        # Validación simple de capacidad
        booked = sum(b.pax for b in tour.bookings if b.status != "cancelada")
        if booked + pax > tour.capacity:
            flash("No hay cupos suficientes para este tour", "error")
            return redirect(url_for("tours_list"))
        booking = Booking(user_id=current_user.id, tour_id=tour_id, pax=pax, status="confirmada")
        db.session.add(booking)
        db.session.commit()
        flash("Reserva creada", "success")
        return redirect(url_for("bookings_list"))

    @app.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
    @login_required
    def bookings_cancel(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        if (booking.user_id != current_user.id) and (not current_user.is_admin()):
            flash("No autorizado", "error")
            return redirect(url_for("bookings_list"))
        booking.status = "cancelada"
        db.session.commit()
        flash("Reserva cancelada", "info")
        return redirect(url_for("bookings_list"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
