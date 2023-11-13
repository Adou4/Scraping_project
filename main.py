# I import my project libraries

import requests
from bs4 import BeautifulSoup
import time

# J'utilise la bibliothèque requests pour récupérer le contenu HTML d'une page web

url = 'https://example.com'
response = requests.get(url)

# Vérifiez si la requête a réussi
if response.status_code == 200:
    html_content = response.content

else:
    print(f'Erreur {response.status_code} lors de la récupération de contenu.')


# J'utilise beautiful Soup pour analyser le contenu HTML et extraire les données souhaitées
soup = BeautifulSoup(html_content, 'html.parser')

# Exemple d'extration de texte
title = soup.title.text
print(f'Titre de la page : {title}')

# Extration de données
# exemple
links = soup.find_all('a')
for link in links:
    print(link['href'])


# Stockage des données
all_links = [link['href'] for link in links]

# Ajouter des délais entre les requêtes pour éviter d'être bloqué par les serveurs
# attendez quelques secondes avant de faire la prochaine requête
time.sleep(5)