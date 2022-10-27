import sqlite3
from wtforms import HiddenField
import requests
from config import *
from datetime import *
from registros.routes import *
from flask import request

def filas_to_diccionario(filas, columnas):
    resultado = []
    for fila in filas:
        posicion_columna = 0
        d = {}
        for campo in columnas:
            d[campo[0]] = fila[posicion_columna]
            posicion_columna += 1
        resultado.append(d)
    return resultado



def select_all():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, (cantidad_from/cantidad_to) as PU from trades order by date;")
    resultado = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return resultado

def insert(registro):
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("INSERT INTO trades (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) values(?,?,?,?,?,?)", registro)
    conn.commit()
    conn.close()

def peticion_crypto(moneda_from_data, moneda_to_data, apikey):
    url = requests.get(f"https://rest.coinapi.io/v1/exchangerate/{moneda_from_data}/{moneda_to_data}?&apikey={apikey}")
    resultado = url.json()
    return resultado

def invertido():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT SUM(cantidad_from) as cantidad_from FROM trades WHERE moneda_from = 'EUR'")
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result

def recuperado():
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT (CASE WHEN SUM(cantidad_to) IS NULL THEN 0 ELSE SUM(cantidad_to) end) as cantidad_to FROM trades WHERE moneda_to = 'EUR'")
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result


def cartera(moneda):
    consulta = f"SELECT ((SELECT (case when (SUM(cantidad_to)) is null then 0 else SUM(cantidad_to) end) as COMPRAR FROM trades WHERE moneda_to = '{moneda}') - (SELECT (case when (SUM(cantidad_from)) is null then 0 else SUM(cantidad_from) end) as GASTAR FROM trades WHERE moneda_from = '{moneda}')) AS {moneda}"
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute(consulta)
    result = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return result  


def traerTodasCartera(crypto):
    cryptosMonedas = {}
    conn= sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    for moneda in crypto:
        consulta = f"SELECT ((SELECT (case when (SUM(cantidad_to)) is null then 0 else SUM(cantidad_to) end) as tot FROM trades WHERE moneda_to = '{moneda}') - (SELECT (case when (SUM(cantidad_from)) is null then 0 else SUM(cantidad_from) end) as ee FROM trades WHERE moneda_from = '{moneda}')) AS {moneda}"
        cur.execute(consulta)
        fila =cur.fetchall() 
        cryptosMonedas[moneda] = fila[0][0]
    conn.close()
     
    return cryptosMonedas

def totalActivo_una_consulta():    
    total = 0
    monederoActual = traerTodasCartera(cryptos)
    url = requests.get(f"https://rest.coinapi.io/v1/exchangerate/EUR?&apikey={apikey}")
    resultado = url.json()

    for a in monederoActual.keys(): 
        for b in resultado['rates']: 
            if b['asset_id_quote'] == a: 
                total += 1/b['rate'] * monederoActual[a]
                
    return total


def validador():
    error = [] 
    registros = select_all() 
    valorCantidad = request.values.get("inputCantidad") 
    valorMonedaFrom = request.values.get('lista_from') 
    valorMonedaTo = request.values.get('lista_to') 
    valorCantidad2 = HiddenField 

    if registros == [] and valorMonedaFrom != "EUR": 
        show_error = flash("Sólo pueden comprar con Euros") 
        error.append(show_error)
        return error
       
    if valorMonedaFrom == valorMonedaTo:
        show_error = flash("Tiene que usar monedas distintas")
        error.append(show_error)
        return error

    if valorCantidad2._value != valorCantidad: 
        show_error = flash("Por favor de a 'Calcular' antes de comprar")
        error.append(show_error)
        return error

    monedero = cartera(valorMonedaFrom)
    if (valorMonedaFrom != 'EUR' and monedero[0][valorMonedaFrom] < float(valorCantidad)):
        show_error = flash(f"No hay saldo suficiente de la moneda {valorMonedaFrom}")
        error.append(show_error)
        return error
    
    return error