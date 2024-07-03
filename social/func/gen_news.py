import requests
import xml.etree.ElementTree as ET
from settings import  config
from func.req_ollama_llm import topic_llm_request


# Eseguo la richiesta ad ANSA per le news, cche poi immagazzino ed utilizzo per lampubblicazione degli articoli
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
            news_titles = []
            # Trova tutti gli elementi `<item>`
            for item in root.findall('.//item'):
                # Trova il titolo all'interno di ciascun `<item>` e aggiungilo alla lista con il relativo testo
                title = item.find('title').text
                # tratto la lista di notizie come un dictionary
                news_item = {
                    'news_title': title,
                    'topic': []  # Inizialmente vuoto, sarà aggiornato manualmente
                }
                news_titles.append(title)    

            # Salvataggio della lista nelle notizie e categorizzazione di essa, l'LLM mi restituirà in formato Json la lista dei titoli con le categorizzazioni
            config.NEWS=topic_llm_request(news_titles)
            print("SYS ----> NEWS: categorization and savings completed")
        else:
            print("SYS ----> NEWS: Error during news collections - ", response.status_code)

    except requests.exceptions.RequestException as e:
        print("SYS ----> NEWS: Error during news rewuest - ", e)