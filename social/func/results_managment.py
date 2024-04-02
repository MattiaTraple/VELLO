# File dedicato ai salvataggi di dati ed informazioni raccolti nel corso della simulazione
import json
import os

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
        "datatime": post.datatime.strftime("%Y-%m-%d %H:%M:%S"),
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




# AGENTS
# Fun che riporta tutto il database degli utenti completop di info personali, post, relazioni, ultimo feed
def updateJson_agent(agent_list):
    for agent in agent_list:
        single_agent(agent)

# Fun ausiliaria, gli viene dato un agent, ne estrae tutte le info da salvare poi nel json 
def single_agent(agent):
    
    if os.path.exists('social/data/agents.json'):
        with open('social/data/agents.json', 'r') as f:
            agg_data = json.load(f)
    else:
        agg_data = {"agents":[]}  
    
    #setto il nuovo agent che poi vado a salvare
    new_ag = {
        "agent_id": agent.id,
        "age":agent.age,
        "interest":', '.join(agent.interest),
        "activity":agent.activity,
        "friends_list":agent.friends,  #aggiungo dopo la lista commenti
        "last_feed": agent.feed,
        "published_post":add_post(agent.published)
    }
    
    agg_data["agents"].append(new_ag)
  
    # Aggiorno Json
    with open('social/data/agents.json', 'w') as file:
        json.dump(agg_data, file, indent=4)
        
# Fun aus per estrazione post, solo id, data e contenuto
def add_post(posts): 
    return [{"post_id": p.id, "content": p.content, "datatime": p.datatime.strftime("%Y-%m-%d %H:%M:%S")} for p in posts]

