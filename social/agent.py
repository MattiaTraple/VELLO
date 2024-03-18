import random
from social.func.random_generator import age_gen, post_gen_prob
from social.func.random_generator import interest_gen
from social.func.random_generator import activity_gen
from social.func.req_openia_llm import gen_post, req_follow

#classe dedicata alla generazione ddegli agents e alle funzioni ad essi dedicati
class Agent:
    
    id_counter = 0
    
    #inizializzare un nuovo agents
    def __init__(self):
      #inizialmente lo uso al posto del nome
      Agent.id_counter += 1
      self.id = Agent.id_counter
      self.age=age_gen()
      self.interest=interest_gen()
      self.activity=activity_gen()
      #campo che mi dovrebbe servire per tenere traccia di ciò che ga l'agent
      self.history=[]
      

    #funzione usata per iniizare a seguire altri agents, basando la scelta su una combo di età e interessi
    def start_follow(self,agent_candidate):
        #per ogni agent che riceve vado a realizzare una richiesta che poi inoltro ad OpenIA
        req_follow(self.age,self.interest,self.history)



    #funzione dedicata alla creazione e generazione del post

    #news andrà a contenere una notizia sulla quale voglio fargli pubblicare il post che devo ancora decidere
    def generate_post(self,news):
      #datatime di generazione
      if post_gen_prob(self.activity):
         #fare richiesta a API di GPT per generare post a riguardo (vengono fornite caratteristiche utente in mdoo da personalizzare in base a quelle il contenuto)
         #potrei eseguire una ristrutturazione della domanda usando i temi o qui o in unafunzione tra questa e quella in openia
         gen_post(self.id, self.interest, self.age, news)
         return "SYS---> "+self.nome+" ha postato"
      return "SYS---> "+agent.nome+" non ha postato nulla"


    # L'utente decide se e come interagire con un post
    def intWithPost(self):
        
        #in base all'activity dell'utente, ogni tot tempo gli verrà posta la scelta se ccreare o meno un post su un determinato contenuto 
        

#GENERARE CSV AGENTI CASUALI 
"""     
def generate_agents(n):
    agents = []
    for _ in range(n):
        agent = Agent()
        agents.append(agent)
    return agents

def write_agents_to_csv(agents, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Age', 'Interest', 'Activity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for agent in agents:
            writer.writerow({'ID': agent.id, 'Age': agent.age, 'Interest': agent.interest, 'Activity': agent.activity})


agents = generate_agents(100)
write_agents_to_csv(agents, 'agents.csv')
"""