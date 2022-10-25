from registros import app
from flask import render_template, flash, request, url_for, redirect
import sqlite3
from registros.models import select_all, peticion_crypto, validador, insert
from registros.forms import Moneda
from wtforms import HiddenField
from config import apikey
from datetime import datetime


@app.route("/")
def index():
    try:
        registros = select_all()
        return render_template("index.html", pageTitle = "CryptoTrades", data =registros, encabezado = 'index.html')
    except sqlite3.Error as e:
        flash("Se ha producido error en la base datos, inténtelo de nuevo más tarde")
        return render_template("index.html", pageTitle="Todos", data = [])
    

@app.route("/purchase", methods= ["GET", "POST"])
def purchase():
    moneda = Moneda()
    valorCantidad = request.values.get("inputCantidad") 
    valorCantidad2 = HiddenField
    if request.method == "GET":
        return render_template("/purchase.html", PageTitle = "Cambiar", formulario = moneda, encabezado = 'purchase.html', cantidad = "input")
    
    else:
        try:
            if request.values.get("Calcular"):
                
                try:
                    if moneda.inputCantidad.data == None:
                        flash("Introduce un numero entero o si es decimal separado por un punto.")
                        return redirect(url_for("comprar"))
                    resultado = peticion_crypto(moneda.lista_from.data, moneda.lista_to.data, apikey)
                    total = resultado['rate'] * float(valorCantidad)
                    total = ("{:.8f}".format(total))
                    tasa = resultado['rate']
                    tasa = ("{:.8f}".format(tasa))
                    valorCantidad2._value = valorCantidad
                    
                    return render_template("/purchase.html", resultado = total, Tasa = tasa, formulario = moneda, cabecera = "purchase.html", cantidad = "texto", valorinput = valorCantidad )
                except Exception as e:
                    print(e)
                    flash("Error de conexión, inténtelo de nuevo mas tarde")
                    return redirect(url_for("index"))
        
      
            elif request.values.get("Cambio"):
                
                try:
                    validat = validador()
                    if validat != []:
                        return redirect (url_for('comprar'))
                   
                    if moneda.validate():
                        resultado = peticion_crypto(moneda.lista_from.data, moneda.lista_to.data, apikey)
                        total = resultado['rate'] * float(valorCantidad)
                        insert([datetime.now().date().isoformat(), str(datetime.now().time().isoformat())[:8], resultado["asset_id_base"], valorCantidad, resultado["asset_id_quote"], total])
                        flash("Compra realizada con exito")
                        return redirect(url_for('index'))
                except sqlite3.Error as e:
                    print(e)
                    flash("Se produjo un error en la base datos")
                    return redirect(url_for('index'))
                
                
            else:
                flash('Error inesperado, intentelo de nuevo más tarde')
                return redirect(url_for('index'))
        
        except Exception as e:
            print(e)
            flash("Error, inténtelo de nuevo mas tarde")
            return redirect(url_for("index"))
   
        
"""
@app.route("/status")
def status():
       
"""