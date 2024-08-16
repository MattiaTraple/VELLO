
import json
import re
import requests
import xml.etree.ElementTree as ET


def request_news():
    # URL dell'RSS
    url = "https://www.ansa.it/sito/ansait_rss.xml"

    try:
        # Effettua la richiesta HTTP all'URL
        response = requests.get(url)

        # Verifica se la richiesta ha avuto successo (codice di stato 200)
        if response.status_code == 200:
            # Parsa il contenuto XML
            print("SYS ----> NEWS: news collected - ", response.status_code)
            root = ET.fromstring(response.content)
            news_list = []
            # Trova tutti gli elementi `<item>`
            for item in root.findall('.//item'):
                # Trova il titolo all'interno di ciascun `<item>` e aggiungilo alla lista con il relativo testo
                title = item.find('title').text
                # tratto la lista di notizie come un dictionary
                news_item = {
                    'title': title,
                    'topics': []  # Inizialmente vuoto, sarà aggiornato manualmente
                }
                return news_list.append(news_item)
           
                
        else:
            print("SYS ----> NEWS: Error during news collections - ", response.status_code)

    except requests.exceptions.RequestException as e:
        print("SYS ----> NEWS: Error during news rewuest - ", e)


print(request_news)