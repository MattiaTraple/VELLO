import json
from openai import OpenAI
import os

CLIENT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))



# Fun dedicata alla generazioen dei post
def gen_post(id,interest,age,news):
    # Se lasciata sopra dava problemi di importazione circolare
    from post import Post
    # Faccio questo per escludere il terzo topic se non è presente
    topics = [topic for topic in news.topics if topic]
    #scrivo bene le richeiste per openia
    #se uso 3.5 turbo specifico anche il sys, senno uso solo lo user
    sys_cont=f"Il contesto è questo, tu sei un utente di un social media, hai un età di {str(age)} anni e i temi che ti interessano sono :{', '.join(interest)}. Hai appena letto della notizia {news.name} e decidi di reagire creando un post a riguardo, tenendo conto delle informazioni demografiche e di interessi che ti ho dato in precedenza, considerando che i topic della notizia rientrano in:{', '.join(topics)} ,in  quale sarebbe il testo di questo post?(scrivi solo quello che metteresti nel post, senza commenti o appunti agiguntivi)"#contino la richiesta
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    #quando verrà aggiunta la parte emotiva del bot gli verrà cheisto di tenerne conto nella creazione nel post
    
    #mettere request(sys_cont, user_cont) al posto di "bulaeivwribviwr"
    post=Post("bulaeivwribviwr",news,id)
    new_post = {
        "post_id": post.id,
        "agent_id":post.agent_id,
        "content": post.content,
        "datatime": post.datatime.strftime("%Y-%m-%d %H:%M:%S"),
        "comments": []
    }

    
    
    if os.path.exists('social/data/post.json'):
        with open('social/data/post.json', 'r') as f:
            con_json = json.load(f)
    else:
        con_json = {}
    
    # Aggiunta del nuovo post
    if news.name in con_json:
        con_json[news.name].append(new_post)
    else:
        con_json[news.name] = [new_post]
    
    # Aggiorno Json
    with open('social/data/post.json', 'w') as file:
        json.dump(con_json, file, indent=4)
        
    return post
 
# Fun dedicata alla decisione di iniziare un amicizia o meno
def req_follow(my_age,my_interest,req_gr,req_int,req_age):
    sys_cont="Il contesto è questo, tu sei un utente di un social media, hai un età di "+str(my_age)+" anni e i temi che ti interessano sono :"" ".join(my_interest)+". Hai incontrato il profilo di un altro utente e devi decidere se iniziare a seguirlo o meno considerando che ha un età di "+str(req_age)+" anni e i temi che gli interessano sono :".join(req_int)+" , cosa decidi di fare?(rispondi solo 'True' se lo vuoi iniizare a seguire, 'False' nel caso in cui tu non voglia)"
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    return request(sys_cont,user_cont)
                 

# Fun dedicata alla generazione di un opportuno comment oad un post
# Agent può servire o meno in base al metodo che uso per fargli deccidere se postare, se uso cativity+random non lo devo nenache passarenj 
def gen_com(news,content,agent):
    sys_cont=f"Il contesto è questo, tu sei un utente di un social media che deve commentare un post che parla di questa notizia :{news}, il post ha il seguente contenuto: {content} "#contino la richiesta
    user_cont="Sei un utente di un social media che dopo aver letto della notizia "#contino la richiesta
    return(request(sys_cont,user_cont))
  
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
    
