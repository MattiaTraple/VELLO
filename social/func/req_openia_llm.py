import json
from openai import OpenAI
import os

CLIENT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))



# Fun dedicata alla generazioen dei post
def gen_post(env,id,interest,age,news):
    # Se lasciata sopra dava problemi di importazione circolare
    from post import Post
    # Faccio questo per escludere il terzo topic se non è presente
    topics = [topic for topic in news["topics"] if topic]
    #scrivo bene le richeiste per openia
    #se uso 3.5 turbo specifico anche il sys, senno uso solo lo user
    sys_cont=f"Il contesto è questo, tu sei un utente di un social media, hai un età di {str(age)} anni e i temi che ti interessano sono :{', '.join(interest)}. Hai appena letto della notizia {news["name"]} e decidi di reagire creando un post a riguardo, tenendo conto delle informazioni demografiche e di interessi che ti ho dato in precedenza, considerando che i topic della notizia rientrano in:{', '.join(topics)} ,in  quale sarebbe il testo di questo post?(scrivi solo quello che metteresti nel post, senza commenti o appunti agiguntivi)"#contino la richiesta
    user_cont="... "
    #quando verrà aggiunta la parte emotiva del bot gli verrà cheisto di tenerne conto nella creazione nel post
    #mettere request(sys_cont, user_cont) al posto di "bulaeivwribviwr"
    post=Post(env,"bulaeivwribviwr",news,id)
    return post
 
# Fun dedicata alla decisione di iniziare un amicizia o meno
def req_follow(my_age,my_interest,req_gr,req_int,req_age):
    sys_cont="Il contesto è questo, tu sei un utente di un social media, hai un età di "+str(my_age)+" anni e i temi che ti interessano sono :"" ".join(my_interest)+". Hai incontrato il profilo di un altro utente e devi decidere se iniziare a seguirlo o meno considerando che ha un età di "+str(req_age)+" anni e i temi che gli interessano sono :".join(req_int)+" , cosa decidi di fare?(rispondi solo 'True' se lo vuoi iniizare a seguire, 'False' nel caso in cui tu non voglia)"
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    return request(sys_cont,user_cont)
                 

# Fun dedicata alla generazione di un opportuno comment oad un post
# Agent può servire o meno in base al metodo che uso per fargli deccidere se postare, se uso cativity+random non lo devo nenache passarenj 
def gen_com(news,content,agent):
    sys_cont=f"Il contesto è questo, tu sei un utente di un social media con interessi:{', '.join(agent.interest)}, che deve commentare un post che parla di questa notizia :{news}, il post ha il seguente contenuto: {content}, genere il commento"
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    #return(request(sys_cont,user_cont))
    return "commentovavvweuiv"
    
# Fun usata per generare le notizie ed estrarne quelli che sono i topic, vengono usati per generazione feed, offerta agli utenti
def gen_define_news():  
    # Richiesta usata per la generazione del contenuto del commento
    sys_cont1=f"Primo messaggio al sistema:"
    user_cont1="Primo messaggio allo userSei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    req1=request(sys_cont1,user_cont1)
    
    # Richiesta usata per l'estrazione delle categorie a cui può essere associata la news appena generata
    sys_cont1=f"Secno:"
    user_cont1=f"Secondo messaggio allo user: consideranto la precedente risposta, dato il contenuto del seguente elenco di categorie: {print_topic_json()}, riesci a restituirmi un elenco delle tre categorie che più rispecchiano la news che mi hai generato? l'elenco ddelle 3 categorie estratte deve essere divio solamente da virgole tra le diverse categorie, rispettando le maiuscole dei nomi di come ti sono state inoltrate"
    req2=[elemento.strip() for elemento in request(sys_cont1,user_cont1).split(",")]
 
    return req1,req2
  
# Richiesta generica che verrà inviata a OpenIA
def request(sys_cont,user_cont):
    # Example OpenAI Python library request
    MODEL = "gpt-3.5-turbo"
    response = CLIENT.chat.completions.create(
        model=MODEL,
        messages=[
            #The system message can be used to prime the assistant with different personalities or behaviors.
            #attenzione, in gpt-3.5-turbo-0301 on viene prestata tanta attenzione a system, meglio specificare tutto in user 
            {"role": "system", "content": sys_cont},
            {"role": "user", "content": user_cont},
            ],
        temperature=0,
    )
    return response.json()['choices'][0]['message']['content']


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

# Fun che utilizzo per categorizzare le notizie che ricevo da ANSA, in modo da avere i topic che poi vado ad usare per decidere l'interesse degli uteinti riguardo a una determinartraa notizia/ post che ricevono
def topic_llm_request():
    # Ricordo di passare sia il nome della notizia che la lista dei topic dal quale può attingere per la categorizzazione
    
    
    return