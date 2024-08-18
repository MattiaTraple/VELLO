import json
import os
import requests

# Usati per inidirzzare meglio l'LLM alla categorizzazione di news, la pubblicazione di post e la pubblicazione di commenti
examples = {
            "news_classification":{
                "input": 
                   """
                   [{"title": "I ghiacci della Groenlandia sono pi\u00f9 fragili del previsto ","topics": []},"
                    {"title": "Google porta la ricerca con l'IA in nuovi mercati","topics": []}
                    ]
                    """,
                    
                "output": 
                    """
                   [{"title": "I ghiacci della Groenlandia sono pi\u00f9 fragili del previsto ","topics": ["Ambiente e cambiamenti climatici","Criptovalute"]},"
                    {"title": "Google porta la ricerca con l'IA in nuovi mercati","topics": ["Tecnologia dell'informazione","Intelligenza artificiale"]}
                    ]
                    """
            },
            "post":{
                "input": "Stonehenge, scoperta la vera origine della pietra dell'altare",
                "output": "Questa scoperta è la realizzazione di un sogno per gli amanti della storia e della fantascienza! Sono curiosissimo di dove le ricerche a riguardo porteranno, chissa se scopriremo di non essere soli in questo universo...  #Stonehenge #Fantascienza"
            },
            "comment":{
                "input":"Questa scoperta è la realizzazione di un sogno per gli amanti della storia e della fantascienza! Sono curiosissimo di dove le ricerche a riguardo porteranno, chissa se scopriremo di non essere soli in questo universo...  #Stonehenge #Fantascienza",
                "output":"Wow che scoperta stupefacente, mi immgino tutti i fan come noi che ora saranno solo in attesa di ulteriori aggiornamenti! "
            }
}


# Fun dedicata alla generazioen dei post
def gen_post(env,id,interest,age,news,counter,personality):
    # Se lasciata sopra dava problemi di importazione circolare
    from post import Post
    
    # Faccio questo per escludere il terzo topic se non è presente
    topics = [topic for topic in news["topics"] if topic]
    
    # Personalizzazione del tono del commento in base ai suoi big 5
    from func.random_generator import big_five_personalizer
    bi5_max,big5_min=big_five_personalizer(personality)
    
    # Contesto su chi è l'agent
    syst_cont=( f"Sei un utente di un social media, hai un età di {str(age)}, tendi ad essere abbastanza {bi5_max}, con una bassa {big5_min}."
                f"I tuoi interessi sono {', '.join(interest)} ma nel generare non devi menzionare direttamente questi argomenti. ")
    
     # Contesto cosa deve fare l'agent
    user_cont=( f"Hai appena letto della notizia '{news['title']}' di cui i topic centrali sono {', '.join(topics)}."
                f"Scrivi un post a riguardo in italiano che pubblicheresti sul social in cui esprimi le tue opinioni in modo diretto e coinvolgente, cercando di stimolare la partecipazione degli altri utenti."
                "Oltre al testo del post non scrivere nient'altro nella risposta")
   
    
    print(f'LOG "{env.now}" ----> LLM_GEN_POST: agent {id} start richiesta')
    #quando verrà aggiunta la parte emotiva del bot gli verrà cheisto di tenerne conto nella creazione nel post
    response=request(user_cont,syst_cont,examples['post'])
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
    bi5_max,big5_min=big_five_personalizer(agent.personality)
    
    # Contesto su chi è l'agent 
    syst_cont=( f"Sei un utente di un social media, hai un età di {agent.age}, tendi ad essere abbastanza {bi5_max}, con una bassa {big5_min}."
                f"I tuoi interessi sono {', '.join(agent.interest)} ma nel generare non devi menzionare direttamente questi argomenti.")

    # Contesto cosa deve fare l'agent
    user_cont=(f"Hai appena letto un post in cui un altro utente dice: '{content}'. "
               f"La notizia riporta '{news}'. "
                "Oltre al testo del post in italiano non scrivere nient'altro nella risposta")
    
    
    return(request(syst_cont,user_cont,examples['comment']))


# Fun usata ad inizio simulazione per categorizzare le notizie estratte da ANSA (i topic vengono presi dalla lista che ho creato con i casi base + generici)
def topic_llm_request(starting_news_dic):  
    # Recupero le categorie
    with open('data/topic.json', 'r', encoding='utf-8') as file:
        topic_data_tot = json.load(file)
    # Considero solo le sottocategorie
    topic_data = [item for sublist in topic_data_tot.values() for item in sublist]

    # Conteto sul social e l'utilizzoche viene fatto delle news
    syst_cont=("Sei un assistente linguistico esperto nella categorizzazione delle notizie che verranno usate dagli utenti di un social per pubblicare dei post a riguardo."
                "Riceverai delle notizie con informazioni in formato JSON e Il tuo compito è classificare ogni notizia aggiungendo come campo di 'topic', una lista di almeno due argomenti inerenti alla notizia."
                f"Gli argomenti disponibili si trovano nella seguente lista: {topic_data}.")
    # Conteso sul compito dell'LLM
    user_cont=(f"Queste sono le notizie che dovrai calssificare completandone il campo topic con la lista dei temi che vengono trattati nella notizia:{json.dumps(starting_news_dic)}"
                "Rispondi solamente con quello che sarebbe il contenuto del Json copmpleto")

    print("SYS ----> NEWS: categorization and savings start")
    req=request(syst_cont,user_cont,examples["news_classification"])
    return req,topic_data
  
  
  
class ExampleSelector:
    def __init__(self, examples):
        self.examples = examples

    def select_example(self, user_cont):
        # Seleziona un esempio rilevante in base a condizioni specifiche
        for example in self.examples:
            if self.is_relevant(example, user_cont):
                return example
        return None

    def is_relevant(self, example, user_cont):
        # Implementa la logica per determinare se un esempio è rilevante
        # Ad esempio, puoi confrontare keyword o la struttura dell'input
        return any(keyword in user_cont for keyword in example['input_keywords'])



  
  
# Richiesta generica che verrà inviata a Ollama
def request(syst_cont, user_cont,selected_example):
    url = "http://localhost:11434/api/chat"
      
    # Costruisce il messaggio con l'esempio se disponibile
    if selected_example:
        prompt = (
            f"Ecco un esempio:\n"
            f"Input: {selected_example['input']}\n"
            f"Output desiderato: {selected_example['output']}\n\n"
            f"Adesso gestisci il seguente input:\n"
            f"{user_cont}"
        )
    else:
        prompt = user_cont

    # Dati da inviare
    data = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": syst_cont},
            {"role": "user", "content": prompt}]
    }

    # Invia la richiesta POST
    raw_response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    # Controlla se la richiesta è stata eseguita con successo
    if raw_response.status_code == 200:
        try:
            json_parts = raw_response.text.strip().split("\n")
            # Decodifica ogni parte JSON e ricostruisci la risposta completa
            complete_response = ''.join(json.loads(part)['message']['content'] for part in json_parts)
            complete_response = complete_response[0:-1]
            return complete_response
        except json.JSONDecodeError:
            # Se la risposta non è un JSON valido, stampa il contenuto grezzo della risposta
            print("Risposta non è un JSON valido. Contenuto grezzo della risposta:")
            print(raw_response.text)
    else:
        print(f"Errore nella richiesta: {raw_response.status_code}, {raw_response.text}")
    


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