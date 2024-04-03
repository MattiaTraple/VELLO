import os
import random
import simpy as si
from func.results_managment import updateJons_post, updateJson_agent
from settings import  config

# Lista oin cui vengono salvati tutti gli agenti
AGENT_LIST=[]
# Cancello i file dove salvo i dati per resettarli
if os.path.exists("social/data/post.json"):
    # Cancella il file
    os.remove("social/data/post.json")
if os.path.exists("social/data/agents.json"):
    # Cancella il file
    os.remove("social/data/agents.json")



# Funzione per la generazione degli agenti
def generate_agents(env, num_agents):
    from agent import Agent
    agent = Agent(env)
    # Tengo una lista degli agent che mi servirà per le varie interazioni
    AGENT_LIST.append(agent)
    print(f'SYM ----> è stato creato l agent {agent.id} - activity: {agent.activity}')
    #devo scegliere quando inizializzare il feed
    #-----
    # Qui puoi fare altre inizializzazioni per gli agenti se necessario
    yield env.process(agent_behavior(env, agent))

# Processo che modella il comportamento di un agente nel social network
def agent_behavior(env, agent):
    while True:
        # Simula il comportamento dell'agente nel social network
        
        # Aggiunge un amico ogni tot tempo
        yield env.timeout(random.randint(200, 300))
        #print(f"agent: {agent.friends}, ng: {num_agents} ")
        if len(agent.friends)<len(AGENT_LIST)-1: # Se segue già tutti non ha senso aggiungergli follower
            #qua viene generato a caso, voglio che inizi a seguire un altro agente obbligaotriamente, segue l'elenco finchè non ne trova uno he gloi interessa  
            #faccio restituire dalla funzione l'id dell'agent di cui è diventato amico
            id_agent_start_follow=agent.find_friends(AGENT_LIST)
            # Viene fatto nella classe perché gli faccio eseguire in lbocco 
            if id_agent_start_follow:print(f"LOG ---->Agent {agent.id} ha aggiunto Agent {id_agent_start_follow} come amico.")
        

        # Ogni tot tempo gli viene data la possibilità di pubblicare contenuto
        yield env.timeout(random.randint(50, 100))
        agent.generate_post()

        #  Ogni tot tempo gli viene data la possibilità di commentare un contenuto
        # da modificare perchè si basa sull feed, non sugli amici
        #if agent.friends:
            #yield env.timeout(random.randint(30, 50))
            #friend_id = random.choice(list(agent.friends))
            #content = f"Commento casuale su un contenuto di {friend_id}"
            #agent.comment_content(friend_id, content)
            #print(f"LOG ---->Agent {agent.agent_id} e ha commentato il post {} di Agent {friend_id}.")


# Funzione principale di simulazione
def start_social_simu(env, num_agents):
   # Generazione degli agenti
   for _ in range(num_agents):
        env.process(generate_agents(env, 1))
   # Esegui la simulazione per un certo periodo di tempo
   env.run(until=config.SIM_TIME)


#MAIN
# Creazione della simulazione
env = si.Environment()
# Run simulazione
start_social_simu(env, config.NUM_AGENTS)

# Salvataggi dello stato ddel social al momento della conclusione della simulaizione
updateJons_post(config.POST_DATABASE)
updateJson_agent(AGENT_LIST)
