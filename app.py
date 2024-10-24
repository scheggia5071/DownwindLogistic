from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de downwinds y participantes
downwinds = []
participants = {}

# Ruta principal con las dos opciones
@app.route('/')
def home():
    return render_template('index.html')

# Página para crear un nuevo downwind
@app.route('/create_downwind', methods=['GET', 'POST'])
def create_downwind():
    if request.method == 'POST':
        # Procesar los datos del formulario cuando se envía
        date = request.form.get('date')
        time = request.form.get('time')
        run = request.form.get('run')

        downwind_name = f"{run} - {date} {time}"
        downwinds.append({
            'name': downwind_name,
            'date': date,
            'time': time,
            'run': run
        })

        # Redirigir al formulario de registro
        return redirect(url_for('register', downwind_name=downwind_name))

    # Mostrar la página de creación de downwind si es un GET
    return render_template('create_downwind.html')


# Página para seleccionar un downwind existente
@app.route('/select_downwind')
def select_downwind():
    return render_template('select_downwind.html', downwinds=downwinds)

# Página para registrar un participante
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Obtener el nombre del downwind desde el formulario
            downwind_name = request.form.get('downwind_name')
            name = request.form.get('name')
            vehicle = request.form.get('vehicle') == 'on'
            seats = request.form.get('seats')

            # Imprimir los datos para depuración
            print(f"Registrando participante: downwind_name={downwind_name}, name={name}, vehicle={vehicle}, seats={seats}")

            # Verificación de downwind_name
            if not downwind_name:
                print("Error: downwind_name no está definido.")
                return "Error: No downwind selected", 400

            # Si el downwind no existe, lo inicializamos
            if downwind_name not in participants:
                participants[downwind_name] = []

            # Agregar el participante
            participants[downwind_name].append({
                'name': name,
                'vehicle': vehicle,
                'seats': seats
            })

            print(f"Participantes actualizados para {downwind_name}: {participants[downwind_name]}")

            # Redirigir correctamente a la página de participantes
            return redirect(url_for('show_participants', downwind_name=downwind_name))

        except Exception as e:
            print(f"Error during registration: {e}")
            return "Internal Server Error", 500

    # Si es una solicitud GET, obtener el downwind_name de los parámetros
    downwind_name = request.args.get('downwind_name')

    # Verificar que downwind_name no esté vacío
    if not downwind_name:
        return "Error: No downwind selected", 400

    # Renderizar la página de registro
    return render_template('register.html', downwind_name=downwind_name)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         downwind_name = request.form.get('downwind_name')
#         name = request.form.get('name')
#         vehicle = request.form.get('vehicle') == 'on'
#         seats = request.form.get('seats')

#         if downwind_name not in participants:
#             participants[downwind_name] = []

#         participants[downwind_name].append({
#             'name': name,
#             'vehicle': vehicle,
#             'seats': seats
#         })

#         return redirect(url_for('show_participants', downwind_name=downwind_name))

#     downwind_name = request.args.get('downwind_name')
#     return render_template('register.html', downwind_name=downwind_name)

# Página para mostrar los participantes de un downwind específico
@app.route('/participants/<downwind_name>')
def show_participants(downwind_name):
    downwind_participants = participants.get(downwind_name, [])
    return render_template('participants.html', downwind_name=downwind_name, participants=downwind_participants)

if __name__ == '__main__':
    app.run(debug=True)



