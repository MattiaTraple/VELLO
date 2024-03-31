import random
import simpy as si
from func.results_managment import update_database_npost
from settings import  config


#generazione degli agents
#----->agents_dict = {idx: Agent() for idx in range(1, NUM_AGENTS+1)}

# Funzione per la generazione degli agenti
def generate_agents(env, num_agents):
   from agent import Agent
   agent = Agent(env)
   print(f'SYM ----> è stato creato l agent {agent.id} - activiti: {agent.activity}')
   #devo scegliere quando inizializzare il feed
      
   # Qui puoi fare altre inizializzazioni per gli agenti se necessario
   yield env.process(agent_behavior(env, agent))

# Processo che modella il comportamento di un agente nel social network
def agent_behavior(env, agent):
    while True:
        # Simula il comportamento dell'agente nel social network
        
        # Aggiunge un amico ogni tot tempo
        #yield env.timeout(random.randint(10, 30))
        #if len(agent.friend)!=NUM_FRIEND: # Se segue già tutti non ha senso aggiungergli follower
          #  while friend_id == agent.agent_id:
           #    friend_id = random.randint(0, NUM_AGENTS - 1)
            #agent.add_friend(friend_id)
            # Viene fatto nella classe perché gli faccio eseguire in lbocco 
            #print(f"LOG ---->Agent {agent.agent_id} e ha aggiunto Agent {friend_id} come amico.")
        

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

# Salvataggio di tutti i post in un json Recap
update_database_npost(config.POST_DATABASE)
