# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 09:43:07 2024

@author: andre
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ruta para mostrar el formulario
@app.route('/')
def index():
    return render_template('register.html')

# Ruta para procesar los datos del formulario
@app.route('/register', methods=['POST'])
def register():
    # Obtener los datos del formulario
    name = request.form.get('name')
    vehicle = request.form.get('vehicle') == 'on'  # El checkbox devuelve 'on' si está marcado
    seats = request.form.get('seats')

    # Mostrar los datos en la consola (puedes reemplazar esto con una base de datos u otro procesamiento)
    print(f"Nombre: {name}, Tiene vehículo: {vehicle}, Plazas disponibles: {seats}")

    # Después de procesar los datos, redirigir al usuario de vuelta al formulario o a otra página
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return "¡Registro exitoso!"


if __name__ == '__main__':
    app.run(debug=True)



