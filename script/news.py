#############   NEWS    #################

import requests
# Remplace 'YOUR_API_KEY' par ta clé API NewsAPI
API_KEY = 'cff3a3ac11184449a740a0fc30a70611'
QUERY = 'apple'  # Le mot-clé de recherche

# URL de l'API pour rechercher des articles
url = f'https://newsapi.org/v2/everything?q={QUERY}&apiKey={API_KEY}'

response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    articles = response.json().get('articles')
    
    if articles:
        for i, article in enumerate(articles):
            print(f"{i + 1}. {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   URL: {article['url']}")
            print(f"   Published At: {article['publishedAt']}\n")
    else:
        print("Aucun article trouvé.")
else:
    print(f"Erreur lors de la requête : {response.status_code}")