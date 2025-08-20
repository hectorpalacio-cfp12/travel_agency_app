# seed_tours.py
from app import create_app
from models import db, Destination, Tour

app = create_app()

with app.app_context():
    # Crear destinos
    destinos_data = [
        {"name": "Bariloche", "description": "Ciudad de lagos y montañas en la Patagonia."},
        {"name": "Puerto Iguazú", "description": "Ciudad cercana a las Cataratas del Iguazú."},
        {"name": "Mendoza", "description": "Región vitivinícola de Argentina."},
        {"name": "Buenos Aires", "description": "Capital de Argentina, mezcla de historia y modernidad."},
        {"name": "El Calafate", "description": "Ciudad turística en Santa Cruz, puerta al Glaciar Perito Moreno."},
    ]

    destinos = []
    for d in destinos_data:
        destino = Destination.query.filter_by(name=d["name"]).first()
        if not destino:
            destino = Destination(**d)
            db.session.add(destino)
        destinos.append(destino)

    db.session.commit()

    # Crear tours asociados a cada destino
    tours_data = [
        ("Aventura en Bariloche", "Excursión de 3 días por lagos y montañas en la Patagonia.", 350.0, 20, "Bariloche"),
        ("Cataratas del Iguazú", "Tour de 2 días para visitar las cataratas, una de las maravillas naturales del mundo.", 280.0, 25, "Puerto Iguazú"),
        ("Viñedos de Mendoza", "Experiencia enoturística con visita a bodegas y degustación de vinos.", 150.0, 30, "Mendoza"),
        ("Buenos Aires Cultural", "Recorrido por los barrios históricos de San Telmo, La Boca y Recoleta.", 100.0, 40, "Buenos Aires"),
        ("Glaciar Perito Moreno", "Excursión de un día completo para conocer el impresionante glaciar en El Calafate.", 320.0, 15, "El Calafate"),
    ]

    for name, desc, price, capacity, dest_name in tours_data:
        destino = Destination.query.filter_by(name=dest_name).first()
        if destino:
            if not Tour.query.filter_by(name=name).first():
                tour = Tour(
                    name=name,
                    description=desc,
                    price=price,
                    capacity=capacity,
                    destination=destino
                )
                db.session.add(tour)

    db.session.commit()
    print("✅ Destinos y tours iniciales creados exitosamente.")

