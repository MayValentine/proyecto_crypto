from registros import app
from flask import render_template, flash
import sqlite3
from registros.models import select_all


@app.route("/")
def index():
    try:
        registros = select_all()
        return render_template("index.html", pageTitle = "CryptoTrades", data =registros, encabezado = 'index.html')
    except sqlite3.Error as e:
        flash("Se ha producido error en la base datos, inténtelo de nuevo más tarde")
        return render_template("index.html", pageTitle="Todos", data = [])
    

"""
@app.route("/purchase", methods= ["GET", "POST"])
def purchase():
        

@app.route("/status")
def status():
       
"""