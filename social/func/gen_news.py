import json
import re
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
                news_list.append(news_item)
            #news_list=news_list[:5]    
            #with open(config.DATA_POSITION+"news_classification.json","r")as f:
                #config.NEWS=json.load(f)
            
            # Vado a far fare la classificazioen all'LLM, la prima contiene il risultao della classificazione, la seconda mi serve per fare dei controlli previo salvataggio delle news(cntiene i topic già scorporati)
            classified_news,topic_list=topic_llm_request(news_list)
            response=response_cleaner(classified_news)
            with open(config.DATA_POSITION+"news_classification.json","w")as f:
                json.dump(response,f,indent=4)
            #se una news non è stata classificata, la rimuovo dalla lista generale
            config.NEWS=detect_miss_classification(response,topic_list)
                
            print("SYS ----> NEWS: categorization and savings completed")
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

    # Rimuovi caratteri di trippo e cambia alcune lettere con accenti e apostrofi
    cleaned_data = extracted_data.replace('\n', '').replace("e'", 'è').replace("'","")
    cleaned_data = re.sub(r'\s+', ' ', cleaned_data)
    cleaned_data = re.sub(r'\"(.*?)\"', r'"\1"', cleaned_data)
    cleaned_data = cleaned_data.replace('\\\"', "\'")
    try:
        # Converti la stringa pulita in una lista di dizionari
        data_list = json.loads(cleaned_data)
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