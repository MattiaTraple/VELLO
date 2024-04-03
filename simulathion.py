import simpy


class Agent:
    def __init__(self, env, agent_id):
        self.env = env
        self.agent_id = agent_id
        self.friends = set()  # Lista degli amici
        self.published_content = []  # Contenuti pubblicati

    # Aggiunge un amico alla lista degli amici
    def add_friend(self, friend_id):
        self.friends.add(friend_id)

    # Pubblica un contenuto
    def publish_content(self, content):
        self.published_content.append(content)
        print(f"Agent {self.agent_id} ha pubblicato: {content}")

    # Commenta un contenuto di un amico
    def comment_content(self, friend_id, content):
        print(f"Agent {self.agent_id} ha commentato il contenuto di Agent {friend_id}: {content}")






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
    #yield env.process(feed_update(env,agent))
    
    

# Processo che modella il comportamento di un agente nel social network
def agent_behavior(env, agent):
    # Simula il comportamento dell'agente nel social network
    while True:
        # Aggiunge un amico ogni tot tempo
        yield env.timeout(random.randint(300, 500))
        if len(agent.friends)<len(AGENT_LIST)-1: # Se segue già tutti non ha senso aggiungergli follower
        #qua viene generato a caso, voglio che inizi a seguire un altro agente obbligaotriamente, segue l'elenco finchè non ne trova uno he gloi interessa  
        #faccio restituire dalla funzione l'id dell'agent di cui è diventato amico
            agent.find_friends(AGENT_LIST)
        
        # Genera post
        yield env.timeout(random.randint(50, 100))
        agent.generate_post()
        
        # Aggiorna il feed
        yield env.timeout(random.randint(500, 500))
        env.process(feed_update(env, agent))
        
        # Commenta un contenuto
        #env.process(comment_content(env, agent))
               
      


def feed_update(env,agent):
    yield env.timeout(random.randint(50,100))
    agent.polulate_feed1(AGENT_LIST)
    




def comment_content(env,agent):
    #  Ogni tot tempo gli viene data la possibilità di commentare un contenuto
        # da modificare perchè si basa sull feed, non sugli amici
        if agent.friends:
            yield env.timeout(random.randint(30, 50))
            friend_id = random.choice(list(agent.friends))
            content = f"Commento casuale su un contenuto di {friend_id}"
            agent.comment_content(friend_id, content)
            print(f"LOG ---->Agent {agent.agent_id} e ha commentato il post  di Agent {friend_id}.")





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