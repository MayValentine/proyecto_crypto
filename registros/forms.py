from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.validators import InputRequired, NumberRange, DataRequired



class Moneda(FlaskForm):
    lista_from = SelectField('From', choices=[('EUR', 'EUR - EURO'), ('BTC', 'BTC - Bitcoin'), ('ETH', 'ETH - Ether'), ('USDT', 'USDT - Tether'), ('BNB', 'BNB - Binance Coin'), ('XRP', 'XRP - Ripple'), ('ADA', 'ADA - Cardano'),('SOL', 'SOL - Solana'), ('DOT', 'DOT - Polkadot'), ('MATIC', 'MATIC - Polygon')])
    lista_to = SelectField('To', choices=[('EUR', 'EUR - EURO'), ('BTC', 'BTC - Bitcoin'), ('ETH', 'ETH - Ether'), ('USDT', 'USDT - Tether'), ('BNB', 'BNB - Binance Coin'), ('XRP', 'XRP - Ripple'), ('ADA', 'ADA - Cardano'),('SOL', 'SOL - Solana'), ('DOT', 'DOT - Polkadot'), ('MATIC', 'MATIC - Polygon')])
    inputCantidad = FloatField('Cantidad', validators=[InputRequired(), NumberRange(min=0.00001, max=99999999), DataRequired()])

    Calcular = SubmitField('Calculate''Calcular')
    Cambio = SubmitField('done_outline''Aceptar')