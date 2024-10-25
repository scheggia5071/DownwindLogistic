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

#Confirmación de que todos los participantes estan inscritos
@app.route('/confirm_participants/<downwind_name>', methods=['POST'])
def confirm_participants(downwind_name):
    try:
        print(f"Confirmación de que todos los participantes están inscritos para {downwind_name}.")
        
        # Aquí puedes añadir lógica adicional si es necesario, como actualizar el estado de un downwind
        
        # Redirigir a la página de logística
        return redirect(url_for('logistics', downwind_name=downwind_name))

    except Exception as e:
        print(f"Error durante la confirmación: {e}")
        return "Internal Server Error", 500

@app.route('/logistics/<downwind_name>', methods=['GET'])
def logistics(downwind_name):
    # Verifica que la clave del downwind exista en los participantes
    if downwind_name in participants:
        downwind_participants = participants[downwind_name]
    else:
        downwind_participants = []

    # Separar a los participantes en dos listas: con coche y sin coche
    with_vehicle = [p for p in downwind_participants if p['vehicle']]
    without_vehicle = [p for p in downwind_participants if not p['vehicle']]

    # Calcular el total de plazas disponibles
    total_seats_available = sum(int(p['seats']) for p in with_vehicle)

    # Renderizar la página de logística
    return render_template('logistics.html', downwind_name=downwind_name, with_vehicle=with_vehicle, without_vehicle=without_vehicle, total_seats_available=total_seats_available)

@app.route('/update_transport/<downwind_name>', methods=['POST'])
def update_transport(downwind_name):
    # Obtener los participantes registrados
    downwind_participants = participants.get(downwind_name, [])

    # Vehículos en la llegada y en la salida
    vehicles_to_llegada = []
    vehicles_to_salida = []

    # Revisar las decisiones de transporte enviadas por el formulario
    for participant in downwind_participants:
        if participant['vehicle']:
            vehicle_choice = request.form.get(f'vehicle_{participant["name"]}')
            if vehicle_choice == "llegada":
                vehicles_to_llegada.append(participant)
            elif vehicle_choice == "salida":
                vehicles_to_salida.append(participant)

    # Total de plazas disponibles en los coches que van a la llegada
    total_seats_llegada = sum(int(p['seats']) for p in vehicles_to_llegada)

    # Verificar si hay suficientes plazas para los participantes sin vehículo
    participants_without_vehicle = [p for p in downwind_participants if not p['vehicle']]
    total_participants_without_vehicle = len(participants_without_vehicle)

    if total_seats_llegada >= total_participants_without_vehicle:
        message = "Hay suficientes plazas disponibles para todos los participantes sin vehículo."
    else:
        message = "No hay suficientes plazas disponibles. Plazas faltantes: " + str(total_participants_without_vehicle - total_seats_llegada)

    return render_template('logistics_result.html', downwind_name=downwind_name, vehicles_to_llegada=vehicles_to_llegada, vehicles_to_salida=vehicles_to_salida, message=message)

@app.route('/confirm_transport_plan/<downwind_name>', methods=['POST'])
def confirm_transport_plan(downwind_name):
    # Obtener los participantes registrados
    downwind_participants = participants.get(downwind_name, [])
    
    if not downwind_participants:
        return "No participants found", 404

    # Filtrar los participantes con y sin vehículo
    with_vehicle = [p for p in downwind_participants if p['vehicle']]
    without_vehicle = [p for p in downwind_participants if not p['vehicle']]

    # Ordenar los vehículos por número de plazas disponibles de mayor a menor
    sorted_with_vehicle = sorted(with_vehicle, key=lambda x: int(x['seats']), reverse=True)

    # Etapa 1: Asignar pasajeros para el viaje a la salida
    seats_assignments_salida = []
    total_seats_salida = 0
    remaining_passengers = downwind_participants.copy()  # Todos los participantes necesitan ir a la salida

    for vehicle in sorted_with_vehicle:
        if total_seats_salida < len(downwind_participants):  # Aún hay pasajeros por asignar
            vehicle_passengers = remaining_passengers[:int(vehicle['seats'])]  # Asignar los primeros disponibles
            seats_assignments_salida.append({'vehicle': vehicle, 'passengers': vehicle_passengers})
            total_seats_salida += int(vehicle['seats'])
            remaining_passengers = remaining_passengers[int(vehicle['seats']):]  # Actualizar pasajeros restantes
        else:
            break

    # Etapa 2: Asignar pasajeros para la recuperación de los coches (todos los participantes, no solo conductores)
    seats_assignments_llegada = []
    total_seats_llegada = 0
    remaining_passengers = downwind_participants.copy()  # Todos los participantes necesitan volver

    for vehicle in sorted_with_vehicle:
        if total_seats_llegada < len(remaining_passengers):  # Aún hay pasajeros por asignar
            vehicle_passengers = remaining_passengers[:int(vehicle['seats'])]  # Asignar los primeros disponibles
            seats_assignments_llegada.append({'vehicle': vehicle, 'passengers': vehicle_passengers})
            total_seats_llegada += int(vehicle['seats'])
            remaining_passengers = remaining_passengers[int(vehicle['seats']):]  # Actualizar pasajeros restantes
        else:
            break

    # Verificar si hay suficientes plazas para todos los participantes (no solo conductores)
    if total_seats_llegada >= len(downwind_participants):
        message = "Hay suficientes plazas disponibles para que todos los participantes regresen a la salida y puedan recuperar los coches."
    else:
        message = f"No hay suficientes plazas para que todos los participantes regresen. Plazas faltantes: {len(downwind_participants) - total_seats_llegada}"

    # Renderizar la página de resultados
    return render_template('logistics_result.html', 
                           downwind_name=downwind_name, 
                           seats_assignments_salida=seats_assignments_salida, 
                           seats_assignments_llegada=seats_assignments_llegada, 
                           message=message)
