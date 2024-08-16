import json
import os
import requests


# Fun dedicata alla generazioen dei post
def gen_post(env,id,interest,age,news,counter,personality):
    # Se lasciata sopra dava problemi di importazione circolare
    from post import Post
    
    # Faccio questo per escludere il terzo topic se non è presente
    topics = [topic for topic in news["topics"] if topic]
    
    # Personalizzazione del tono del commento in base ai suoi big 5
    from func.random_generator import big_five_personalizer
    big5_per=big_five_personalizer(personality)
    
    #scrivo bene le richeiste per ollama
    user_cont=f"Il contesto è questo, sei un utente di un social media, hai un età di {str(age)} anni e i topic che ti interessano sono :{', '.join(interest)}. Hai appena letto della notizia {news['title']} e di cui i topic sono:{', '.join(topics)}, considerando le informazioni che ti ho fornito, quale sarebbe il testo di questo post?(scrivi solo quello che metteresti nel post, senza commenti o appunti agiguntivi e fai in modo di {big5_per})"
    print(f'LOG "{env.now}" ----> LLM_GEN_POST: agent {id} start richiesta')
    #quando verrà aggiunta la parte emotiva del bot gli verrà cheisto di tenerne conto nella creazione nel post
    response=request(user_cont)
    print(f'LOG "{env.now}" ----> LLM_GEN_POST: agent {id} end richiesta')
    post=Post(env,response,news,id,counter)
    return post
 
# Fun dedicata alla decisione di iniziare un amicizia o meno
def req_follow(my_age,my_interest,req_gr,req_int,req_age):
    sys_cont="Il contesto è questo, tu sei un utente di un social media, hai un età di "+str(my_age)+" anni e i temi che ti interessano sono :"" ".join(my_interest)+". Hai incontrato il profilo di un altro utente e devi decidere se iniziare a seguirlo o meno considerando che ha un età di "+str(req_age)+" anni e i temi che gli interessano sono :".join(req_int)+" , cosa decidi di fare?(rispondi solo 'True' se lo vuoi iniizare a seguire, 'False' nel caso in cui tu non voglia)"
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    return request(sys_cont,user_cont)
                 

# Fun dedicata alla generazione di un opportuno comment oad un post
# Viene deciso se l'agent commenta in base al suo grado di interattivita e se i suoi interessi sono parte del post
def gen_com(news,content,agent):
    
    # Personalizzazione del tono del commento in base ai suoi big 5
    from func.random_generator import big_five_personalizer
    big5_per=big_five_personalizer(agent.personality)
    
    user_cont=f"Ora sei un utente che ha come interessi:{', '.join(agent.interest)}. Devi commentare un post che parla di questa notizia :'{news}' ed ha il seguente contenuto: {content}; genere il commento basandoti anche su tono con il quale è stato scritto l0'articolo del post (scrivi solo quello che metteresti nel post, senza commenti o appunti agiguntivi, inoltre fai in modo di {big5_per})"
    return(request(user_cont))


# Fun usata ad inizio simulazione per categorizzare le notizie estratte da ANSA (i topic vengono presi dalla lista che ho creato con i casi base + generici)
def topic_llm_request(starting_news_dic):  
    # Recupero le categorie
    with open('data/topic.json', 'r', encoding='utf-8') as file:
        topic_data_tot = json.load(file)
    # Considero solo le sottocategorie
    topic_data = [item for sublist in topic_data_tot.values() for item in sublist]

    # Richiesta usata per la generazione del contenuto del commento
    user_cont=f"Sei in un social media e queste sono le notizie sulle quali poi gli utenti andranno a creare poste e a commentare:{json.dumps(starting_news_dic)}; devi restituirmi il contenuto precedente come lo hai trovato, completando però il campo topic: all'intenro devi inserire come attributi delle liste di topic, almeno due topic presenti all'interno della seguente lista {topic_data} che rispecchino i temi trattati dalla notizia, restituisci il json facendo la classificazione per tutte le notizie che ti ho inviato"
    print("SYS ----> NEWS: categorization and savings start")
    req=request(user_cont)
    return req,topic_data
  
# Richiesta generica che verrà inviata a Ollama
def request(user_cont):
    # URL dell'endpoint
    url = "http://localhost:11434/api/chat"
    # Dati da inviare
    data = {
        "model": "llama3",
        "messages": [{"role": "user","content": user_cont}]
    }

    # Invia la richiesta POST
    raw_response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    # Controlla se la richiesta è stata eseguita con successo
    if raw_response.status_code == 200:
        try:
            json_parts = raw_response.text.strip().split("\n")
            # Decodifica ogni parte JSON e ricostruisci la risposta completa
            complete_response = ''.join(json.loads(part)['message']['content'] for part in json_parts)
            complete_response=complete_response[1:-1]
            return complete_response
            
        except json.JSONDecodeError:
            # Se la risposta non è un JSON valido, stampa il contenuto grezzo della risposta
            print("Risposta non è un JSON valido. Contenuto grezzo della risposta:")
            print(response.text)
    else:
        print(f"Errore nella richiesta: {response.status_code}, {response.text}")
    


# Fun ausiliaria che permette di estrarre i topic dal file json e renderli un elenco da conseganre alla fun chiamante così da poterli usare per la richiesta di riconoscimento di categoria
def print_topic_json():
    res=""
    sotto_categorie=[]
    if os.path.exists('social/data/topic.json'):
        with open('social/data/topic.json', 'r') as f:
            topic_json = json.load(f)

    sotto_categorie.extend(sub for sot in topic_json.values() for sub in sot)
    for sotto_cat in sotto_categorie:
        res += sotto_cat+", "  
    return res