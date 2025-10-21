from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from controllers.comisiones_controller import comisiones_bp
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('config.Config')

    db.init_app(app)

    app.register_blueprint(comisiones_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    # Crear tablas y datos iniciales
    with app.app_context():
        from models.usuario import Usuario
        from models.venta import Venta
        db.create_all()
        insertar_datos_prueba(db)

    return app

def insertar_datos_prueba(db):
    from models.usuario import Usuario
    from models.venta import Venta

    if Usuario.query.count() == 0:
        usuarios = [
            Usuario(nombre="Juan", apellido="Pérez"),
            Usuario(nombre="Ana", apellido="Martínez"),
            Usuario(nombre="Carlos", apellido="Gómez"),
            Usuario(nombre="Lucía", apellido="Sánchez"),
            Usuario(nombre="Pedro", apellido="Ramírez")
        ]
        db.session.add_all(usuarios)
        db.session.commit()

    if Venta.query.count() == 0:
        ventas = [
            Venta(idusuario=1, monto=120.50, fecha='2025-06-01'),
            Venta(idusuario=1, monto=380.00, fecha='2025-06-02'),
            Venta(idusuario=2, monto=150.00, fecha='2025-06-03'),
            Venta(idusuario=2, monto=500.00, fecha='2025-06-05'),
            Venta(idusuario=3, monto=75.00, fecha='2025-06-07'),
            Venta(idusuario=3, monto=95.00, fecha='2025-06-09'),
            Venta(idusuario=4, monto=300.00, fecha='2025-06-10'),
            Venta(idusuario=4, monto=600.00, fecha='2025-06-12'),
            Venta(idusuario=5, monto=210.00, fecha='2025-06-15'),
            Venta(idusuario=5, monto=800.00, fecha='2025-06-17')
        ]
        db.session.add_all(ventas)
        db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
