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
        return redirect(url_for('register', downwind_name=downwind_name))

    return render_template('create_downwind.html')

# Página para seleccionar un downwind existente
@app.route('/select_downwind')
def select_downwind():
    return render_template('select_downwind.html', downwinds=downwinds)

# Página para registrar un participante
@app.route('/register', methods=['POST'])
def register():
    downwind_name = request.form.get('downwind_name')
    name = request.form.get('name')
    vehicle = request.form.get('vehicle') == 'on'
    seats = request.form.get('seats')

    # Asegurarse de que el downwind_name no esté vacío
    if not downwind_name:
        return "Error: No downwind selected", 400

    if downwind_name not in participants:
        participants[downwind_name] = []

    participants[downwind_name].append({
        'name': name,
        'vehicle': vehicle,
        'seats': seats
    })

    # Redirigir manualmente a la URL
    redirect_url = f"/participants/{downwind_name}"
    print(f"Redirigiendo a {redirect_url}")
    return redirect(redirect_url)

    downwind_name = request.args.get('downwind_name')
    return render_template('register.html', downwind_name=downwind_name)

# Página para mostrar los participantes de un downwind específico
@app.route('/participants/<downwind_name>')
def show_participants(downwind_name):
    downwind_participants = participants.get(downwind_name, [])
    return render_template('participants.html', downwind_name=downwind_name, participants=downwind_participants)

if __name__ == '__main__':
    app.run(debug=True)



