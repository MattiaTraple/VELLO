import json
import os
import re
import requests
from func.rag_vector_managment import add_agent_action, get_agent_action 

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


# Usato per cambiare il prompting in presenza di un utente malicious
def malicious_or_not(type,malicious):
    if type=="post":
        if malicious==True:
            malicious_syst=("Sei estremamente critico, sarcastico e cattivo,inoltre ti piace creare caos e conflitto senza un confronto costruttivo")                
            malicious_user=("devi essere sprezante, sarcastico e attaccare direttamente l’argomento della notizia, criticandone aspramente il tema e cercando di crare sconforto e caos e sminuendo tutto quello che lo riguarda.")
        else:
            malicious_syst=""
            malicious_user="esprimi le tue opinioni in modo diretto e coinvolgente, cercando di stimolare la partecipazione degli altri utenti."
    else:
        if malicious==True:
            malicious_syst=("Esprimi le tue opinioni critiche e polemiche in modo cattivo e tendi a voler creare conflitto con gli altri utenti denigrandoli e sminuendoli."
                            "Puoi essere anche politicaly in-correct, senza curarti dei sentimenti delle altre persone")
    return malicious_syst,malicious_user

# Fun dedicata alla generazion dei post
def gen_post(agent,news):
    # Se lasciata sopra dava problemi di importazione circolare
    from post import Post
    
    # Faccio questo per escludere il terzo topic se non è presente
    topics = [topic for topic in news["topics"] if topic]
    
    # Personalizzazione del tono del commento in base ai suoi big 5
    from func.random_generator import big_five_personalizer
    bi5_max,big5_min=big_five_personalizer(agent.personality)
    
    # In base alla malevolità dell'agente o meno il prompting varierà    
    mal_sys,mal_usr=malicious_or_not("post",agent.malicious)
    
    # Contesto su chi è l'agent
    syst_cont=( f"Sei un utente di un social media, hai un età di {str(agent.age)}, tendi ad essere abbastanza {bi5_max}, con una bassa {big5_min}."
                f"I tuoi interessi sono {', '.join(agent.interest)} ma nel generare non devi menzionare direttamente questi argomenti. "
                f"{mal_sys}"
                )
    
     # Contesto cosa deve fare l'agent
    user_cont=( f"Hai appena letto della notizia '{news['title']}' di cui i topic centrali sono {', '.join(topics)}."
                f"Scrivi un post a riguardo in italiano che pubblicheresti sul social {mal_usr}."
                "- Oltre al testo del post non scrivere nient'altro nella risposta."
                "- Il post deve essere non più lungo di 200 caratteri"
                f"Qui ci sono alcuni dei tuoi commenti recenti che potrebbero essere utili per generare il post:\n\n"
                r"{'\n'.join(get_agent_action(agent.id))}\n\n")
   
    
    print(f'LOG "{agent.env.now}" ----> LLM_GEN_POST: agent {agent.id} start richiesta')
    #quando verrà aggiunta la parte emotiva del bot gli verrà cheisto di tenerne conto nella creazione nel post
    response=request(user_cont,syst_cont,None)
    print(f'LOG "{agent.env.now}" ----> LLM_GEN_POST: agent {agent.id} end richiesta')
    post=Post(agent.env,response,news,agent.id,agent.post_counter)
    add_agent_action(agent.id,response)
    return post        

# Fun dedicata alla generazione di un opportuno comment oad un post
# Viene deciso se l'agent commenta in base al suo grado di interattivita e se i suoi interessi sono parte del post
def gen_com(news,content,agent):
    
    # Personalizzazione del tono del commento in base ai suoi big 5
    from func.random_generator import big_five_personalizer
    bi5_max,big5_min=big_five_personalizer(agent.personality)

    # In base alla malevolità dell'agente o meno il prompting varierà    
    mal_sys,mal_usr=malicious_or_not("post",agent.malicious)
    
    # Contesto su chi è l'agent 
    syst_cont=( f"Sei un utente di un social media, hai un età di {agent.age}, tendi ad essere abbastanza {bi5_max}, con una bassa {big5_min}."
                f"{mal_sys}"
                f"I tuoi interessi sono {', '.join(agent.interest)} ma nel generare non devi menzionare direttamente questi argomenti.")

    # Contesto cosa deve fare l'agent
    user_cont=(f"Hai appena letto un post in cui un altro utente dice: '{content}'. "
               f"La notizia riporta '{news}'. "
                "- Oltre al testo del post in italiano non scrivere nient'altro nella risposta."
                "- Il commento deve essere non più lungo di 200 caratteri"
                f"Qui ci sono alcuni dei tuoi commenti recenti che potrebbero essere utili per generare il post:\n\n"
                r"{'\n'.join(get_agent_action(agent.id))}\n\n")
    
    res=request(syst_cont,user_cont,None)
    add_agent_action(agent.id,res)
    return()


# Fun usata ad inizio simulazione per categorizzare le notizie estratte da ANSA (i topic vengono presi dalla lista che ho creato con i casi base + generici)
def topic_llm_request(starting_news_dic):  
    # Recupero le categorie
    with open('data/topic.json', 'r', encoding='utf-8') as file:
        topic_data_tot = json.load(file)
    # Considero solo le sottocategorie
    topic_data = [item for sublist in topic_data_tot.values() for item in sublist]

    # Conteto sul social e l'utilizzoche viene fatto delle news
    syst_cont=("Sei un assistente linguistico esperto nella categorizzazione delle notizie che verranno usate dagli utenti di un social per pubblicare dei post a riguardo."
                "Riceverai delle notizie con informazioni in formato JSON e Il tuo compito è classificare ogni notizia aggiungendo come campo di 'topic', una lista di almeno un argomento inerente alla notizia."
                f"Gli argomenti disponibili si trovano nella seguente lista: {topic_data}.")
    # Conteso sul compito dell'LLM
    user_cont=(f"Queste sono le notizie che dovrai calssificare completandone il campo topic con la lista di uno o più temi che vengono trattati nella notizia:{json.dumps(starting_news_dic)}"
                "Rispondi solamente con quello che sarebbe il contenuto del Json copmpleto")

    print("SYS ----> NEWS: categorization and savings start")
    req=request(syst_cont,user_cont,examples["news_classification"])
    return req,topic_data
  
  
# Richiesta generica che verrà inviata a Ollama
def request(syst_cont, user_cont,selected_example):
    url = "http://localhost:11434/api/chat"
      
    # Costruisce il messaggio con l'esempio se disponibile
    if selected_example!=None:
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