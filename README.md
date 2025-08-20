# Travel Agency App

Sistema de gestión para una agencia de viajes y tours. Permite gestionar **usuarios**, **tours**, **destinos** y **reservas**, con login y dashboard dinámico.

---

## 🛠 Tecnologías

- Python 3.11  
- Flask  
- Flask-Login  
- Flask-Migrate / SQLAlchemy  
- SQLite (base de datos)  
- Bootstrap 5 (interfaz)  

---

## ⚡ Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/travel_agency_app.git
cd travel_agency_app
````

2. Crear entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux / Mac
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear la base de datos y correr migraciones:

```bash
flask db upgrade
```

5. (Opcional) Cargar seeds iniciales:

```bash
python seed_destinations.py
python seed_tours.py
python seed_users.py
```

---

## 🚀 Ejecutar la app

```bash
flask --app app run --debug
```

Luego abrir en el navegador:

```
http://127.0.0.1:5000/
```

---

## 🗂 Estructura del proyecto

```
travel_agency_app/
├── app.py
├── models.py
├── templates/
│   └── dashboard.html
├── static/
│   ├── css/
│   └── js/
├── migrations/
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📝 Seeds iniciales

* **Destinos argentinos:** Bariloche, Mendoza, Iguazú, Buenos Aires, El Calafate

* **Tours ejemplo:**

  * Aventura en Bariloche
  * Cataratas del Iguazú
  * Viñedos de Mendoza
  * Buenos Aires Cultural
  * Glaciar Perito Moreno

* **Usuario administrador:**

  * Email: [admin@travel.com](mailto:admin@travel.com)
  * Contraseña: admin123

---

## 🔐 Login / Dashboard

* Login para usuarios registrados
* Dashboard con lista de **tours** y **reservas**
* Posibilidad de **crear, editar y cancelar reservas**

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

## ✉ Contacto

* Héctor Palacio
* Email: [hector.palacio@cfp12.edu.ar]

```

