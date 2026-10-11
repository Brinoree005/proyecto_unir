from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Parámetros del Sistema (Requerimientos 4 y 5) ---
TARIFA_ENERGIA = 536
TARIFA_AGUA = 730

# Base de datos simulada en memoria (para el prototipo)
registros = []

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        referencia = request.form.get('referencia')
        servicio = request.form.get('servicio')
        consumo_str = request.form.get('consumo')

        try:
            # Requerimiento 3: Validar que sea numérico
            consumo = float(consumo_str)
            
            # Requerimiento 1: Cálculo
            if servicio == 'Agua':
                total = consumo * TARIFA_AGUA
            else:
                total = consumo * TARIFA_ENERGIA
                
            # Guardar el registro
            registros.append({
                'nombre': nombre,
                'referencia': referencia,
                'servicio': servicio,
                'consumo': consumo,
                'total': total
            })
            return redirect(url_for('index'))
            
        except ValueError:
            error = "El consumo debe ser un número válido."

    return render_template('index.html', registros=registros, 
                           t_agua=TARIFA_AGUA, t_energia=TARIFA_ENERGIA, error=error)

@app.route('/limpiar')
def limpiar():
    registros.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # El host '0.0.0.0' permite que la app sea visible en tu red local
    app.run(host='0.0.0.0', port=5000, debug=True)