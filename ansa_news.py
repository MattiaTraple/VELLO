import requests
import xml.etree.ElementTree as ET

# URL dell'RSS
url = "https://www.ansa.it/sito/ansait_rss.xml"

try:
    # Effettua la richiesta HTTP all'URL
    response = requests.get(url)

    # Verifica se la richiesta ha avuto successo (codice di stato 200)
    if response.status_code == 200:
        # Parsa il contenuto XML
        root = ET.fromstring(response.content)

        # Crea una lista vuota per salvare i titoli
        titoli = []

        # Trova tutti gli elementi `<item>`
        for item in root.findall('.//item'):
            # Trova il titolo all'interno di ciascun `<item>` e aggiungilo alla lista
            titolo = item.find('title').text
            titoli.append(titolo)

        

    else:
        print("SYS ----> Errore nella richiesta HTTP :", response.status_code)

except requests.exceptions.RequestException as e:
    print("Si è verificato un errore durante la richiesta:", e)