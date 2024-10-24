#############   FINANCE    #################

import requests
from datetime import datetime, timedelta

# Remplace 'YOUR_API_KEY' par ta clé API Alpha Vantage
API_KEY = 'MAOLRUZM8WBP605B'
SYMBOL = 'AAPL'  # Exemple : Apple Inc.

# URL de l'API pour récupérer les données quotidiennes de l'action
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}&outputsize=compact'

response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    data = response.json()
    time_series = data.get('Time Series (Daily)')

    if time_series:
        # Obtenir la date d'hier et d'avant-hier
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        day_before_yesterday = today - timedelta(days=2)

        # Formatage des dates pour correspondre au format de l'API
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        day_before_yesterday_str = day_before_yesterday.strftime('%Y-%m-%d')

        # Récupérer les données des deux derniers jours
        yesterday_data = time_series.get(yesterday_str)
        day_before_yesterday_data = time_series.get(day_before_yesterday_str)

        # Affichage des résultats
        if yesterday_data:
            print(f"Prix d'ouverture le {yesterday_str}: {yesterday_data['1. open']} USD")
            print(f"Prix de fermeture le {yesterday_str}: {yesterday_data['4. close']} USD")
        else:
            print(f"Aucune donnée disponible pour le {yesterday_str}.")

        if day_before_yesterday_data:
            print(f"Prix d'ouverture le {day_before_yesterday_str}: {day_before_yesterday_data['1. open']} USD")
            print(f"Prix de fermeture le {day_before_yesterday_str}: {day_before_yesterday_data['4. close']} USD")
        else:
            print(f"Aucune donnée disponible pour le {day_before_yesterday_str}.")
    else:
        print("Aucune donnée disponible pour cette action.")
else:
    print(f"Erreur lors de la requête : {response.status_code}")
    
    
    
    