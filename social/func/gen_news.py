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
            root = ET.fromstring(response.content)
            news_titles = []
            # Trova tutti gli elementi `<item>`
            for item in root.findall('.//item'):
                # Trova il titolo all'interno di ciascun `<item>` e aggiungilo alla lista con il relativo testo
                title = item.find('title').text
                news_titles.append(title)

            # Salvataggio della lista nelle notizie e categorizzazione di essa
            config.NEWS=topic_finder(news_titles)
            print("SYS ----> Raccolta delle ultime norizie da ANSA andata a buon fine", response.status_code)

        else:
            print("SYS ----> Errore nella richiesta HTTP per la richiesta delle notizie:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("SYS ----> Si è verificato un errore durante la richiesta:", e)

# Funzione che in base al titolo e il testo della news che gli viene data, restituisce per ognuno nome della news e tre cateregorie topic inerenti
def topic_finder(news_titles):
    news_list=[]
    for titles in news_titles:
        # Mi aspetto come risultato una stringa, che io divido in 3 basandomi sulle virgole in 3, cche salvo poi in una lista
        topics_res=["h","r","dd"]#(topic_llm_request(titles)).replace(" e ", ",").split(",")
        news_list.append({"name":titles,"topics":topics_res})

    return news_list