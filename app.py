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

participants = {}

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

   # Verificar que se obtengan los participantes existentes
    downwind_participants = participants.get(downwind_name, [])
    print(f"Mostrando participantes para {downwind_name}: {downwind_participants}")

    return render_template('register.html', downwind_name=downwind_name, participants=downwind_participants)


# Página para mostrar los participantes de un downwind específico
@app.route('/participants/<downwind_name>')
def show_participants(downwind_name):
    downwind_participants = participants.get(downwind_name, [])
    return render_template('participants.html', downwind_name=downwind_name, participants=downwind_participants)

if __name__ == '__main__':
    app.run(debug=True)
    
    
# Codigo para añadir la posibilidad de eliminar un participante
@app.route('/delete_participant/<downwind_name>/<participant_name>', methods=['POST'])
def delete_participant(downwind_name, participant_name):
    try:
        # Buscar los participantes del downwind
        downwind_participants = participants.get(downwind_name, [])

        # Filtrar la lista de participantes para eliminar al participante específico
        new_participants = [p for p in downwind_participants if p['name'] != participant_name]

        # Actualizar la lista de participantes para ese downwind
        participants[downwind_name] = new_participants

        print(f"Participante {participant_name} eliminado de {downwind_name}.")
        
        # Redirigir a la página de registro para el mismo downwind
        return redirect(url_for('register', downwind_name=downwind_name))

    except Exception as e:
        print(f"Error eliminando participante: {e}")
        return "Internal Server Error", 500

# def delete_participant(downwind_name, participant_name):
#     try:
#         # Buscar los participantes del downwind
#         downwind_participants = participants.get(downwind_name, [])

#         # Filtrar la lista de participantes para eliminar al participante seleccionado
#         new_participants = [p for p in downwind_participants if p['name'] != participant_name]

#         # Actualizar la lista de participantes para ese downwind
#         participants[downwind_name] = new_participants

#         print(f"Participante {participant_name} eliminado de {downwind_name}.")
        
#         # Redirigir a la página de registro para el mismo downwind
#         return redirect(url_for('register', downwind_name=downwind_name))

#     except Exception as e:
#         print(f"Error eliminando participante: {e}")
#         return "Internal Server Error", 500

#Confirmación de que todos los participantes estan inscritos
@app.route('/confirm_participants/<downwind_name>', methods=['POST'])
def confirm_participants(downwind_name):
    try:
        # Confirmar que todos los participantes están inscritos
        print(f"Confirmación recibida: Todos los participantes para {downwind_name} están inscritos.")
        
        # Redirigir a la siguiente fase o página
        return redirect(url_for('logistics_planning', downwind_name=downwind_name))
    
    except Exception as e:
        print(f"Error durante la confirmación: {e}")
        return "Internal Server Error", 500


@app.route('/logistics_planning/<downwind_name>')
def logistics_planning(downwind_name):
    return render_template('logistics_planning.html', downwind_name=downwind_name)
