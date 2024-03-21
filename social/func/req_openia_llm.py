import json
from openai import OpenAI
import os
from social.settings import CLIENT


#func dedicata alla generazioen dei post
def gen_post(id,interest,age,news):
    #scrivo bene le richeiste per openia
    #se uso 3.5 turbo specifico anche il sys, senno uso solo lo user
    sys_cont="Il contesto è questo, tu sei un utente di un social media, hai un età di "+age+" anni e i temi che ti interessano sono :"" ".join(interest)+". Hai appena letto della notizia "+news+" e decidi di reagire creando un post a riguardo, tenendo conto dell'e informazioni demografiche e di interessi che ti ho dato in precedenza,  quale sarebbe il testo di questo post?(scrivi solo quello che metteresti nel post, senza commenti o appunti agiguntivi)"#contino la richiesta
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    #quando verrà aggiunta la parte emotiva del bot gli verrà cheisto di tenerne conto nella creazione nel post
    
    #setto il nuovo post
    post = {
        "nome_utente": id,
        "risposta": request(sys_cont, user_cont),
        "commenti": [] 
    }
    
    # Leggi JSON
    with open('data/post.json', 'r') as file:
        contenuto_json = json.load(file)
    
    # Aggiungo nuovo post
    if news in contenuto_json:
        contenuto_json[news].append(post)
    else:
        contenuto_json[news] = [post]
    
    # Aggiorno Json
    with open('data/post.json', 'w') as file:
        json.dump(contenuto_json, file, indent=4)
  

#funzione dedicata alla decisione di iniziare un amicizia o meno
def req_follow(my_age,my_interest,req_gr,req_int,req_age):
    sys_cont="Il contesto è questo, tu sei un utente di un social media, hai un età di "+my_age+" anni e i temi che ti interessano sono :"" ".join(my_interest)+". Hai incontrato il profilo di un altro utente e devi decidere se iniziare a seguirlo o meno considerando che ha un età di "+req_age+" anni e i temi che gli interessano sono :".join(req_int)+" , cosa decidi di fare?(rispondi solo 'True' se lo vuoi iniizare a seguire, 'False' nel caso in cui tu non voglia)"
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    return request(sys_cont,user_cont)
        
    
        
    
#richiesta generica che verrà inviata a OpenIA
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