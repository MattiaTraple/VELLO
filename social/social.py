import os
import random
import simpy as si
from func.results_managment import save_data
from settings import  config

# Lista oin cui vengono salvati tutti gli agenti
AGENT_LIST=[]
# Cancello i file dove salvo i dati per resettarli
if os.path.exists("social/data/post.json"):os.remove("social/data/post.json")
if os.path.exists("social/data/agents.json"):os.remove("social/data/agents.json")



# Funzione per la generazione degli agenti
def generate_agents(env):
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
    # Simula il comportamento dell'agente nel social network
    while True:
        # Aggiunge un amico ogni tot tempo
        yield env.timeout(random.randint(200,300))
        if len(agent.friends)<len(AGENT_LIST)-1: # Se segue già tutti non ha senso aggiungergli follower
        #qua viene generato a caso, voglio che inizi a seguire un altro agente obbligaotriamente, segue l'elenco finchè non ne trova uno he gloi interessa  
        #faccio restituire dalla funzione l'id dell'agent di cui è diventato amico
            agent.find_friends(AGENT_LIST)
        
        # Genera post
        yield env.timeout(random.randint(50, 100))
        agent.generate_post()
        
        yield env.timeout(random.randint(500, 600))
        agent.polulate_feed1(AGENT_LIST)
    
        # Commenta un contenuto
        agent.new_comment(AGENT_LIST)
           
 
# Funzione principale di simulazione
def start_social_simu(env, num_agents):
   # Generazione degli agenti
   for _ in range(num_agents):
        env.process(generate_agents(env))
   # Esegui la simulazione per un certo periodo di tempo
   env.run(until=config.SIM_TIME)


#MAIN
# Creazione della simulazione
env = si.Environment()
# Run simulazione
start_social_simu(env, config.NUM_AGENTS)

# Salvataggio dei dati della simulazione
save_data(config.POST_DATABASE,AGENT_LIST)
