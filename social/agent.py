import random
from random_generator import age_gen
from random_generator import interest_gen
from random_generator import activity_gen


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
def start_follow(agent):
  #per ogni agent che riceve vado a realizzare una richiesta che poi inoltro ad OpenIA
  richiesta(agent.age,agent.interest,history)




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