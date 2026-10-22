from flask import Flask, render_template, request, redirect, url_for
import uuid
from datetime import datetime

app = Flask(__name__)

# Tarifas fijas
TARIFA_ENERGIA = 536  # $ / kWh
TARIFA_AGUA = 730     # $ / m3

registros = []

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            referencia = request.form.get('referencia')
            servicio = request.form.get('servicio')
            consumo = float(request.form.get('consumo'))

            # Bloqueo estricto de valores negativos en el servidor
            if consumo < 0:
                raise ValueError("El consumo no puede ser negativo.")

            if servicio == 'Energía':
                total = consumo * TARIFA_ENERGIA
            else:
                total = consumo * TARIFA_AGUA

            registros.append({
                'id': str(uuid.uuid4())[:8], # Genera un ID único para la factura
                'fecha': datetime.now().strftime("%Y-%m-%d"),
                'nombre': nombre,
                'referencia': referencia,
                'servicio': servicio,
                'consumo': consumo,
                'total': total
            })
        except ValueError as ve:
            error = str(ve)
        except Exception as e:
            error = f'Error en los datos ingresados: {str(e)}'

    return render_template(
        'index.html',
        registros=registros,
        t_energia=TARIFA_ENERGIA,
        t_agua=TARIFA_AGUA,
        error=error
    )

@app.route('/factura/<id>')
def factura(id):
    # Busca el registro por su ID para generar la factura
    registro = next((r for r in registros if r['id'] == id), None)
    if not registro:
        return "Factura no encontrada", 404
    return render_template('factura.html', reg=registro, t_energia=TARIFA_ENERGIA, t_agua=TARIFA_AGUA)

@app.route('/limpiar')
def limpiar():
    registros.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
