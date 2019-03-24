import requests

# List all trades in the database
all_trades = requests.get('http://127.0.0.1:8000/trades/')

# Create a new trade in the database
requests.post('http://127.0.0.1:8000/trades/', {'sell_currency': 'USD', 'buy_currency': 'ARS', 'sell_amount': 100})

# Get the exchange rate from USD to ARS
usd_to_ars_rate = requests.get('http://127.0.0.1:9000/rate/', params={'sell_currency': 'USD', 'buy_currency': 'ARS'})
