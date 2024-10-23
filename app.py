# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 09:43:07 2024

@author: andre
"""

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Crear la base de datos y tabla si no existe
def init_db():
    conn = sqlite3.connect('participants.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS participants
                 (name TEXT, has_vehicle BOOLEAN, seats INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    has_vehicle = 'vehicle' in request.form  # Si el checkbox está marcado
    seats = request.form['seats'] if has_vehicle else 0

    # Guardar los datos en la base de datos
    conn = sqlite3.connect('participants.db')
    c = conn.cursor()
    c.execute("INSERT INTO participants (name, has_vehicle, seats) VALUES (?, ?, ?)", (name, has_vehicle, seats))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
