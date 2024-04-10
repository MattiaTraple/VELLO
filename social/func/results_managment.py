# File dedicato ai salvataggi di dati ed informazioni raccolti nel corso della simulazione
import json
import os
import pymongo
from settings import config
import datetime

def save_data(post_database,agent_list):
    # In queste due prime funzioni faccio un backup dell'ultima simulazione e ddei post a lei legata che viene rinnovato ogni votla
    updateJons_post(post_database)
    updateJson_simulations(agent_list)
    # Aggiornamento database e in questo caso mi appariranno tutte le simulazioni che ho fatto
    update_mongodb()

# JSON

#POST
# Fun per trasferire contenuto POST_DATABASE nel json
def updateJons_post(post_databasse):
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
        "datatime": post.datatime,
        "comments":add_comment(post.comments)   #aggiungo dopo la lista commenti
    }

    for news_item in post_data["news"]:
        if news_item["name"] == post.news.name:
            news_item["post"].append(new_post)
            break
    else:
        post_data["news"].append({
            "name": post.news.name,
            "topic": ', '.join(post.news.topics),
            "post": [new_post]
        })
  
    # Aggiorno Json
    with open('social/data/post.json', 'w') as file:
        json.dump(post_data, file, indent=4)

# Fun aus per estrazione commenti
def add_comment(comments):
    return [{"commenter_id": com.agent, "content": com.content, "datatime": com.datetime} for com in comments]


# SIMULATIONS
# Fun che riporta tutto il database degli utenti completop di info personali, post, relazioni, ultimo feed e informazioni riguardanti la simulazione
def updateJson_simulations(agent_list):
    
    if os.path.exists('social/data/simulations.json'):
        with open('social/data/simulations.json', 'r') as f:
            data = json.load(f)
    else:
        data = {"simulations":[]}  
    
    new_simulation={
        "simulation_number": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "simulation_settings":{
                "simulation_time":config.SIM_TIME,
                "agents_number":config.NUM_AGENTS,
                "friend_limit":config.NUM_FRIEND,
                "feed_post_number":config.NUM_FEED
        },
        "news_used":[config.NEWS.name],
        "agents":[single_agent(agent) for agent in agent_list]
    }
    data["simulations"].append(new_simulation)
    

    # Aggiorno Json
    with open('social/data/simulations.json', 'w') as file:
        json.dump(data, file, indent=4)


# Fun ausiliaria, gli viene dato un agent, ne estrae tutte le info da salvare poi nel json 
def single_agent(agent):
    #setto il nuovo agent che poi vado a salvare
    return{
        "agent_id": agent.id,
        "age":agent.age,
        "interest":', '.join(agent.interest),
        "activity":agent.activity,
        "friends_list":agent.friends,
        "last_feed": agent.feed,
        "published_post":add_post(agent.published)
    }
  
    
        
# Fun aus per l'aggiunta di tutti i post corrispondenti all'utente
def add_post(posts): 
    post_format=[]
    for p in posts:
        new_post = {
            "post_id": p.id,
            "news": p.news.name,
            "topic": ', '.join(p.news.topics),
            "content": p.content,
            "datatime": p.datatime,
            "comments":add_comment(p.comments)   #aggiungo dopo la lista commenti
        }
        post_format.append(new_post)
    
    return post_format

# UPDATE DATABASE MONGODB
# Andrò ad aggiugnere dati simulazione e agenti con relativi post e commenti al database 
def update_mongodb():
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017/")
    db = client.get_database("local")
    collection = db.get_collection("Simulations")
    
    if os.path.exists('social/data/simulations.json'):
        with open('social/data/simulations.json', 'r') as f:
            data = json.load(f)
    
    # inserisco nel database tutte le informazioni di simulaizoe, agenti e post
    res=collection.insert_many(data["simulations"])
    
    # Controllo di aver inserito ddei dati
    if  res.inserted_ids:
        print("SYS ----> Aggiornamento Database MondoDB avvenuto con successo")
    else:
        print("SYS ----> Aggiornamento Database MondoDB ha riscontrato qualche problema")