import json
from openai import OpenAI
import os
CLIENT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))



# Fun dedicata alla generazioen dei post
def gen_post(id,interest,age,news):
    #scrivo bene le richeiste per openia
    #se uso 3.5 turbo specifico anche il sys, senno uso solo lo user
    sys_cont="Il contesto è questo, tu sei un utente di un social media, hai un età di "+str(age)+" anni e i temi che ti interessano sono :"" ".join(interest)+". Hai appena letto della notizia "+news+" e decidi di reagire creando un post a riguardo, tenendo conto dell'e informazioni demografiche e di interessi che ti ho dato in precedenza,  quale sarebbe il testo di questo post?(scrivi solo quello che metteresti nel post, senza commenti o appunti agiguntivi)"#contino la richiesta
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    #quando verrà aggiunta la parte emotiva del bot gli verrà cheisto di tenerne conto nella creazione nel post
    
    
    
    
    
    
    #verisone senza classe post
    """
    #setto il nuovo post
    post = {
        "nome_utente": id,
        "risposta": "prova123456789",#request(sys_cont, user_cont),
        "commenti": [] 
    }
    """
    
    
    
    # Leggi JSON
    if os.path.exists('social/data/post.json'):
        with open('social/data/post.json', 'r') as f:
            con_json = json.load(f)
    else:
        con_json = {}
    
    # Aggiungo nuovo post
    if news in con_json:
        con_json[news].append(post)
    else:
        con_json[news] = [post]
    
    # Aggiorno Json
    with open('social/data/post.json', 'w') as file:
        json.dump(con_json, file, indent=4)
  

# Fun dedicata alla decisione di iniziare un amicizia o meno
def req_follow(my_age,my_interest,req_gr,req_int,req_age):
    sys_cont="Il contesto è questo, tu sei un utente di un social media, hai un età di "+str(my_age)+" anni e i temi che ti interessano sono :"" ".join(my_interest)+". Hai incontrato il profilo di un altro utente e devi decidere se iniziare a seguirlo o meno considerando che ha un età di "+str(req_age)+" anni e i temi che gli interessano sono :".join(req_int)+" , cosa decidi di fare?(rispondi solo 'True' se lo vuoi iniizare a seguire, 'False' nel caso in cui tu non voglia)"
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    return request(sys_cont,user_cont)
                 
    
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


# Fun dedicata alla generazione di un commento
# req_comment():
    
