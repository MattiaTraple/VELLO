from func.random_generator import age_gen, post_gen_prob, interest_gen, activity_gen
from func.req_openia_llm import gen_post, req_follow

# Classe dedicata alla generazione ddegli agents e alle funzioni ad essi dedicati
class Agent:
    
    id_counter = 0
    
    # Inizializzare un nuovo agents
    def __init__(self):
      #inizialmente lo uso al posto del nome
      Agent.id_counter += 1
      self.id = Agent.id_counter
      self.age=age_gen()
      self.interest=interest_gen()
      self.activity=activity_gen()
      #campo che mi dovrebbe servire per tenere traccia di ciò che ga l'agent
      self.history=[]
      #quando decide di aggiungere qualcuno, viene rimosso poi dalla lista dei consigliati
      self.pos_frind={}


    # Funzione usata per iniizare a seguire altri agents, basando la scelta su una combo di età e interessi
    def start_follow(self):
        #per ogni agent che riceve vado a realizzare una richiesta che poi inoltro ad OpenIA
        req_follow(self.age,self.interest,self.history)


    # Riceve la lista di tutti gli agents, rimuove l'utente che ha chiamato la funzione, infine procede per l'assegnazione dei gradi
    def find_friends(self,agents_candidates):      
        #rimuovo quello che ha vhiamato la funzione, considderando che la lista poi la utilizzero sempre e la salvo in pos_frind
        ag_cd=agents_candidates     
        del ag_cd[self.id]
        self.pos_frind=self.order_by_degree(ag_cd)


    # Funzione dedicata alla creazione e generazione del post
    # News andrà a contenere una notizia sulla quale voglio fargli pubblicare il post che devo ancora decidere
    def generate_post(self,news):
      #datatime di generazione
      if post_gen_prob(self.activity):
         #fare richiesta a API di GPT per generare post a riguardo (vengono fornite caratteristiche utente in mdoo da personalizzare in base a quelle il contenuto)
         #potrei eseguire una ristrutturazione della domanda usando i temi o qui o in unafunzione tra questa e quella in openia
         gen_post(self.id, self.interest, self.age, news)
         return "SYS---> "+self.id+" ha postato"
      return "SYS---> "+self.id+" non ha postato nulla"


    # L'utente decide se e come interagire con un post
    #def intWithPost(self):
        
        #in base all'activity dell'utente, ogni tot tempo gli verrà posta la scelta se ccreare o meno un post su un determinato contenuto 
        
        
    # Funzione chiamata da order_by_degree per restituire il grado di un agents
    def cal_degree_friend(self, ag_age, ag_int):
        grado = 0
        diff_eta = abs(self.age - ag_age)
        if diff_eta <= 3:
            grado += 0.5
        elif diff_eta <= 5:
            grado += 0.2
        elif diff_eta <= 10:
            grado += 0.08
        elif diff_eta <= 10:
            grado += 0.04
        
        # Calcola il grado dell'utente in base agli interessi in comune
        grado+=sum(0.5 for int1 in self.interest for int2 in ag_int if int1 == int2)
        return grado


    # Funzione chiamata da find_friends per restituire una lista di agent ordinati per grado di coerenza
    def order_by_degree(self,ag_cd):
        agent_gr_dic={}
        # Calcola il grado di ogni utente e salvalo nel dizionario gradi_utenti
        for ag_id,ag in ag_cd.items():
            gr = self.cal_degree_friend(ag.age,ag.intrest)
            agent_gr_dic[ag_id] = {'grade': gr, 'agent': ag}
        # Versione corta    
        # agent_gr_dic = {ag_id: {'grade': self.cal_degree_friend(ag.age, ag.interest), 'agent': ag} for ag_id, ag in ag_cd.items()}
        return(sorted(agent_gr_dic.items(), key=lambda x: x[1]['grade'], reverse=True))


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