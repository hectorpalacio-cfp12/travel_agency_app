# Sistema de Gestión para Agencia de Viajes (Flask + SQLite)

Aplicación web mínima para gestionar usuarios, tours y reservas con registro y login.

## Características
- Registro e inicio de sesión con contraseñas hasheadas (Werkzeug).
- Roles: `admin` (gestiona tours) y `user` (realiza reservas).
- CRUD de tours (solo admin).
- Listado de reservas del usuario y de todos si es admin.
- SQLite (`app.db`) por defecto.
- Plantillas Jinja2 simples (sin dependencias de UI).

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # opcional, o crea tu propio .env
python seed_admin.py   # crea un usuario admin
flask --app app run --debug
```
La app estará en http://127.0.0.1:5000

## Variables de entorno (.env)
```
FLASK_SECRET_KEY= cambia-esto
DATABASE_URL= sqlite:///app.db
ADMIN_EMAIL= admin@demo.com
ADMIN_PASSWORD= admin123
ADMIN_NAME= Admin
```

## Estructura
```
travel_agency_app/
  app.py
  models.py
  seed_admin.py
  requirements.txt
  .env.example
  templates/
    base.html, login.html, register.html, dashboard.html, tours_*.html, bookings_*.html
  static/
    styles.css
```

## Nota de seguridad
- Cambia la `FLASK_SECRET_KEY` en producción.
- Usa HTTPS y una base de datos productiva si despliegas públicamente.
