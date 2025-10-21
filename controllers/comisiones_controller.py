from flask import Blueprint, render_template, request
from sqlalchemy.sql import func
from datetime import datetime
from app import db
from models.usuario import Usuario
from models.venta import Venta

comisiones_bp = Blueprint('comisiones', __name__)

def calcular_comision(total):
    if total >= 1000:
        return total * 0.15
    elif total >= 800:
        return total * 0.10
    elif total >= 600:
        return total * 0.08
    elif total >= 500:
        return total * 0.06
    else:
        return 0

@comisiones_bp.route('/buscar_comisiones')
def buscar_comisiones():
    return render_template('formulario_busqueda.html')

@comisiones_bp.route('/comisiones', methods=['POST'])
def mostrar_comisiones():
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']

    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

    resultados = (
        db.session.query(
            Usuario.nombre,
            Usuario.apellido,
            func.sum(Venta.monto).label('total_ventas')
        )
        .join(Venta)
        .filter(Venta.fecha.between(fecha_inicio, fecha_fin))
        .group_by(Usuario.idusuarios)
        .all()
    )

    resumen = []
    for r in resultados:
        comision = calcular_comision(r.total_ventas)
        resumen.append({
            "nombre": r.nombre,
            "apellido": r.apellido,
            "total_ventas": r.total_ventas,
            "comision": comision
        })

    return render_template('comision.html', comision=resumen)
