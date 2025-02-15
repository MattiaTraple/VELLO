import json
import os
import random
import re
import requests
import xml.etree.ElementTree as ET
from settings import  config
from func.req_ollama_llm import topic_llm_request

# Lista delle diverse fonti di info di ANSA
news_source_list={"WORLD":"https://www.ansa.it/sito/notizie/mondo/mondo_rss.xml",
                  "SPORT":"https://www.ansa.it/sito/notizie/sport/sport_rss.xml",
                  "TOPNEWS":"https://www.ansa.it/sito/notizie/topnews/topnews_rss.xml",
                  "CULTURE":"https://www.ansa.it/sito/notizie/cultura/cultura_rss.xml",
                  "CRONICHLE":"https://www.ansa.it/sito/notizie/cronaca/cronaca_rss.xml",
                  "CINEMA":"https://www.ansa.it/sito/notizie/cultura/cinema/cinema_rss.xml",
                  "FOOD":"https://www.ansa.it/canale_terraegusto/notizie/terraegusto_rss.xml",
                  "TECHNOLOGY":"https://www.ansa.it/canale_tecnologia/notizie/tecnologia_rss.xml",
                  "SCIENCE":"https://www.ansa.it/canale_scienza_tecnica/notizie/scienzaetecnica_rss.xml",
                  "TRIP":"https://www.ansa.it/canale_viaggi/notizie/viaggiart_rss.xml",
                  "ANIMALS":"https://www.corriere.it/dynamic-feed/rss/section/Animali.xml",
                  "VIDEOGAME":"https://www.everyeye.it/feed/feed_news_rss.asp",
                  "FITNESS":"https://www.ilsole24ore.com/rss/sport24--fitness-e-wellness.xml",
                  "MUSIC":"https://www.rtl.it/feed/notizie/spettacoli/musica/"}


def request_news():
    # Vuoi rieseguire la selezione delle news?
    reload=config.RELOAD_NEWS
    # Mi assicuro di nn voler rifare la ricerca, di avere un ile e che questo contenga qualcosa
    if reload==False and os.path.exists(config.DATA_POSITION + "news_classification.json") and os.path.getsize(config.DATA_POSITION + "news_classification.json") > 0:
        with open(config.DATA_POSITION + "news_classification.json", "r") as f:
            config.NEWS=json.load(f)
        print("SYS ----> NEWS: categorization and collection was already done")
        return
    
    res = []
    for field,url in news_source_list.items():
        res.extend(single_news(field,url))  # Estende la lista invece di aggiungere una lista nidificata
    random.shuffle(res)
    
    n = len(res)
    chunks = [res[i:i + n // 5] for i in range(0, n, n // 5)]

    # Inizializza le variabili per i risultati finali
    classified_news_total = []
    topic_list_total = []

    # Itera attraverso ogni chunk e processa separatamente
    for chunk in chunks:
        classified_news, topic_list = topic_llm_request(chunk)
        response = response_cleaner(classified_news)

        # Aggiungi i risultati parziali a quelli totali
        classified_news_total.extend(response)
        topic_list_total.extend(topic_list)

    config.NEWS = detect_miss_classification(classified_news_total, topic_list_total)
    
    # Salva il risultato combinato nel file JSON
    with open(config.DATA_POSITION + "news_classification.json", "w") as f:
        json.dump(config.NEWS, f, indent=4)
    
    
    print("SYS ----> NEWS: categorization and savings completed")

# Eseguo la richiesta ad ANSA per le news, cche poi immagazzino ed utilizzo per lampubblicazione degli articoli
def single_news(field, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"SYS ----> NEWS: news collected form {field} - ", response.status_code)
            root = ET.fromstring(response.content)
            news_list = []
            #Voglio limitare a 4 news per tipo da aggiungere alla lista generale
            count=0
            for item in root.findall('.//item'):
                if count==config.NEWSXCATEGORY:
                    break
                title = item.find('title').text
                    
                # Sistemo gli encoding presenti con la corrispondente
                unicode_pattern = re.compile(r'\\u[0-9a-fA-F]{4}')
                # Sostituisci ogni sequenza con il corrispondente carattere
                title = unicode_pattern.sub(lambda match: chr(int(match.group(0)[2:], 16)), title)
                news_item = {
                    'title': title,
                    'topics': []  # Inizialmente vuoto, sarà aggiornato manualmente
                }
                news_list.append(news_item)  # Aggiunge direttamente il dizionario alla lista
                count+=1
            return news_list
        else:
            print("SYS ----> NEWS: Error during news collections - ", response.status_code)

    except requests.exceptions.RequestException as e:
        print("SYS ----> NEWS: Error during news rewuest - ", e)
    
    
# Fun per pulire la risposta ricevuta dall'llm per la categorizzazione delle notizie
def response_cleaner(res):
    # Escludo il testo ch l'llm aggiunge prima e dopo la stringa
    start_index = res.find('[')
    end_graf = res.rfind('}')+1

    # Estraggo il contenuto tra le quadre ed escludo tutto ciò che c'è tra l'ultima graffa dell'ultimo oggetto e l'ultima quadra
    extracted_data = res[start_index:end_graf]+"]"

    # Rimuovi caratteri di troppo e cambia alcune lettere con accenti e apostrofi
    cleaned_data = extracted_data.replace('\n', '').replace("è", "e'").replace('ò',"o'").replace('à',"a'").replace('ù',"u'")
    cleaned_data = re.sub(r'\s+', ' ', cleaned_data)  # Rimuove spazi extra
    cleaned_data = re.sub(r'\"(.*?)\"', r'"\1"', cleaned_data)  # Mantiene le virgolette corrette
    cleaned_data = cleaned_data.replace('\\\"', "\'")  # Sostituisce \\" con '

    try:
        # Converti la stringa pulita in una lista di dizionari
        data_list = json.loads(cleaned_data)
        # Escludo quelli che non hanno categorizzazione
        data_list = [item for item in data_list if item.get('topics')]
        return(data_list)
    except json.JSONDecodeError as e:    
        print(f"An error occurred: {e}")
        return res
    
def detect_miss_classification(response,topic_list):
    res=[]
    for item in response:
    
        if item['title'] not in topic_list:
            if len(item['topics'])!=0:
                res.append(item)
    return res