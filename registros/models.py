from config import ORIGIN_DATA
import sqlite3

def filas_to_diccionario(filas, columnas):
    resultado = []
    for fila in filas:
        posicion_columna = 0
        d = {}
        for campo in columnas:
            d[campo[0]] = fila[posicion_columna]
            posicion_columna += 1
        resultado.append(d)



def select_all():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()
    cur.execute("SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, (cantidad_from/cantidad_to) as PU from movements order by date;")
    resultado = filas_to_diccionario(cur.fetchall(), cur.description)
    conn.close()
    return resultado