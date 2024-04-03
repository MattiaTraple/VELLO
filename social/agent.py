import itertools
import json
import os
import random
from func.random_generator import age_gen, content_interaction_gen_prob, interest_gen, activity_gen
from func.req_openia_llm import gen_post, req_follow
from settings import config



# Classe dedicata alla generazione degli agents e alle funzioni ad essi dedicati
class Agent:
    
    id_counter = 0
    
    # Inizializzare un nuovo agents
    def __init__(self,env):
      # Permette ddi tenera a conatto con il riferimento dell'agent nella simulazione
      self.env = env  
      # Inizialmente lo uso al posto del nome
      Agent.id_counter += 1
      self.id = Agent.id_counter
      self.age=age_gen()
      self.interest=interest_gen()
      self.activity=activity_gen()
      # Campo che mi dovrebbe servire per tenere traccia di ciò che ga l'agent
      self.history=[]
      # Quando decide di aggiungere qualcuno, viene rimosso poi dalla lista dei consigliati
      self.friends=[]
      self.feed=[]
      # Lista post pubblicati
      self.published=[]

    # Versione c 
    def find_friends(self,agents_candidates):   
        # Possi limitare in caso gli amici che voglio fare aggiugnere   
        # if len(self.friends)==config.NUM_FRIEND:return              
        
        ag_ca=self.order_by_degree(agents_candidates)
        for ag_id in ag_ca:
                # Questa funzione fa una richiesta a OpenIa che restituisce True/False se è interessato o meno all'amicizia
                #if(req_follow(self.age,self.interest,inner['grade'],inner['agent'].interest,inner['agent'].age)): #---> possibile implementare .selfhistory in futuro
                    # Escludi l'agente corrente e gli agenti già presenti nella lista degli amici
                    if ag_id != self.id and ag_id not in self.friends and len(self.friends) < config.NUM_FRIEND:
                        self.friends.append(ag_id)
                        print(f'LOG "{self.env.now}" ----> Agent {self.id} ha aggiunto Agent {ag_id} come amico.')
                
       


    # Funi dedicata alla creazione e generazione del post
    # News andrà a contenere una notizia sulla quale voglio fargli pubblicare il post che devo ancora decidere
    def generate_post(self):
      #datatime di generazione
        if content_interaction_gen_prob(self.activity):
            #fare richiesta a API di GPT per generare post a riguardo (vengono fornite caratteristiche utente in mdoo da personalizzare in base a quelle il contenuto)
            #potrei eseguire una ristrutturazione della domanda usando i temi o qui o in unafunzione tra questa e quella in openia
            new_p=gen_post(self.env,self.id, self.interest, self.age, config.NEWS)
            self.published.append(new_p)
            config.POST_DATABASE.append(new_p)
            print(f'LOG "{self.env.now}" ----> {str(self.id)} ha postato')
        print(f'LOG "{self.env.now}" ----> {str(self.id)} non ha postato')
        
    # L'utente decide se e come interagire con un post
    def intWithPost(self,post):
        #in base all'activity dell'utente, ogni tot tempo gli verrà posta la scelta se ccreare o meno un post su un determinato contenuto 
        #come ordino 
        
        # Deccide se commentare basato su activiti dell'utente
        if content_interaction_gen_prob(self.activity):
            post.create_comment(self)
        

        
    # Fun chiamata da order_by_degree per restituire il grado di un agents
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
        

    # Fun chiamata da find_friends per restituire una lista di agent ordinati per grado di coerenza
    def order_by_degree(self,ag_cd):
        agent_gr_dic={}
        # Calcola il grado di ogni utente e salvalo nel dizionario gradi_utenti
        for ag in ag_cd:
            gr = self.cal_degree_friend(ag.age,ag.interest)
            agent_gr_dic[ag.id] = {'grade': gr}
        # Versione corta    
        # agent_gr_dic = {ag_id: {'grade': self.cal_degree_friend(ag.age, ag.interest), 'agent': ag} for ag_id, ag in ag_cd.items()}
        return dict(sorted(agent_gr_dic.items(), key=lambda x: x[1]['grade'], reverse=True))
                   
            
    # Fun che verrà chiamata dopo che sono stati creati un po di post che popola (e aggiorna) periodicamente il feed dell'utente personalizzandolo in base a:

    # mod1 -> 1 post randomico per i primi 10 amici della lista di persone che segue
    def polulate_feed1(self,agent_list):
        # Se per qualche motivo il feed non è stato riempito correttamente, vado a riempirlo in modo randomico, ex uni non ha abbasatnza amici alloraa devo andare a riempirgli il feed in altro modo
        #while len(self.feed) != config.NUM_FEED:
            for ag in itertools.islice(self.friends, config.NUM_FEED):
                if ag!=self.id:
                    agent=(next((agent for agent in agent_list if agent.id == ag), None))
                    if agent.published:
                        # Prende un post randomico tra quelli di un amico
                        post=random.choice(agent.published)
                        if post.id is not self.feed:
                            self.feed.append(post.id)
                            print(f'LOG "{self.env.now}" ----> Il post {post.id} è stato aggiunto')
            print(f'SYM "{self.env.now}" ----> il feed dell Agent {self.id} è stato aggiornato')

            
                        
    # mod2 -> 1 post più recente i primi 10 amici della lista di persone che segue
    def polulate_feed2(self,agents_dict):
        for ag in itertools.islice(agents_dict.values(), config.NUM_FEED):
            if ag.id!=self.id:
                if ag.published:
                    # Prende l'ultimo post dell'amico
                    self.feed.append(ag.published[-1])

    # mod3 -> basa la raccolta dei primi 10 post del feed basandosi sul tema post, andando in ordine 
    def polulate_feed3(self):
        count=1
        # Uso shuffle così da dare i post da analizzare per la selezioen in ordine casuale e non in ordine di creazione, do più variabilità
        for post in random.shuffle(config.POST_DATABASE):
            if count==10: break
            #solo il post non è dell'agent di cui stiamo ccreando il feed e se c'è un matching tra topic posso andare ad aggiungerlo al feed
            if post.agent_id!=self.id and set(post.topic) & set(self.interest):
                self.feed.append(post)
                count+=1         
            

'''
# Generate post e riempi feed3
agents_dict = {idx: Agent() for idx in range(1, NUM_AGENTS+1)}
count=0
for ag in agents_dict.values():
        ag.generate_post()    
        ag.find_friends(agents_dict) 
        if count==10:break
        count+=1
count=0
for ag in agents_dict.values():
    ag.polulate_feed3()
    if count==1:break
    count+=1
'''

# Test per follower relation
"""
agents_dict = {idx: Agent() for idx in range(1, NUM_AGENTS+1)}
count=0
for ag in agents_dict.values():
         #dopo che tutti gli utentei sono stati ccreati,propongo liste di amici papabili che l'agent sceglie se seguire o meno
         
         ag.find_friends(agents_dict)
         if count==1:break
         count+=1
"""         


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