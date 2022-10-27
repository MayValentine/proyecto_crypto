# Proyecto de criptomonedas

Programa hecho en python, Flask, html y jinja para el intercambio de euros a criptomonedas y viceversa.

## Instalacion

- Obtener la apikey en http://www.coinapi.io
- Obtener la secret key en http://randomkeygen.com/
- Hacer una coipa del fichero `config_template.py` y en la clave apikey poner tu clave
```
apikey = "ADA95444-BFEA-4B00-AC1D-ACDC35E02A4B"
```
```
Secret_key = "Bbf6GMtBYbI04bEdpER3FzVUEzlNx9wj"
```
- Instalar los siguientes programas:
    - flask
    - python_dotenv
    - wtforms
- Renombrar el fichero copia como `config.py`
- Hacer una copia del fichero `.env_template` y cambiar el FLASK_DEBUG a conveniencia
- Renombrar el fichero `.env_template` a `.env`
- Descargar una app para crear bases de datos como SQlite

### Instalacion de dependencias

- Ejecutar pip install -r requirements.txt
Por ultimo ejecutar
´´´
flask run
´´´
- Si no entra en el servidor cambiarlo a otro, por ejemplo:
´´´
flask run -p 5001
´´´