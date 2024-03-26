# File dedicato ai salvataggi di dati ed informazioni raccolti nel corso della simulazione
import json
import os

# JSON

#POST
# Fun per trasferire contenuto POST_DATABASE nel json
def update_database_npost(post_databasse):
    for post in post_databasse:
        single_post(post)
# Fun ausiliaria, gli viene dato il post e lo salva sotto la rispettiva notizia nel file json
def single_post(post):
    
    if os.path.exists('social/data/post.json'):
        with open('social/data/post.json', 'r') as f:
            post_data = json.load(f)
    else:
        post_data = {"news":[]}
    
    #setto il nuovo post che poi vado a salvare
    new_post = {
        "post_id": post.id,
        "agent_id":post.agent_id,
        "content": post.content,
        "datatime": post.datatime.strftime("%Y-%m-%d %H:%M:%S"),
        "comments":add_comment(post.comments)   #aggiungo dopo la lista commenti
    }

    for news_item in post_data["news"]:
        if news_item["name"] == post.news:
            news_item["post"].append(new_post)
            break
    else:
        post_data["news"].append({
            "name": post.news,
            "topic": post.topic,
            "post": [new_post]
        })
  
    # Aggiorno Json
    with open('social/data/post.json', 'w') as file:
        json.dump(post_data, file, indent=4)

# Fun aus per estrazione commenti
def add_comment(comments):
    res=[]
    for com in comments:
        res.append({"commenter_id":com.agent,"content":com.content})
    
    return res