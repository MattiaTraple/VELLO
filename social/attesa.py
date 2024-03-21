import random
from func.random_generator import age_gen, post_gen_prob, interest_gen, activity_gen
from func.req_openia_llm import gen_post, req_follow
from collections import defaultdict


#classe dedicata alla generazione ddegli agents e alle funzioni ad essi dedicati
class Agent:
    
    id_counter = 0
    
    #inizializzare un nuovo agents
    def __init__(self):
      # Inizialmente lo uso al posto del nome
      Agent.id_counter += 1
      self.id = Agent.id_counter
      self.age=age_gen()
      self.interest=interest_gen()
      self.activity=activity_gen()
      # Campo che mi dovrebbe servire per tenere traccia di ciò che ga l'agent
      self.history=[]
      # Quando decide di aggiungere qualcuno, viene rimosso poi dalla lista dei consigliati
      self.pos_frind=[]
      
    def ff(self,agents_candidates):   
      ag_cd=agents_candidates     
      del ag_cd[self.id]
      print(order_by_degree(ag_cd,self.age,self.interest))




def order_by_degree(ag_cd, age, interest):
    agent_gr_dic={}
    # Calcola il grado di ogni utente e salvalo nel dizionario gradi_utenti
    for ag_id,ag in ag_cd.items():
        gr = cal_degree_friend(ag.age, ag.interest, age, interest)
        print(gr)
        agent_gr_dic[ag_id] = {'grade': gr, 'agent': ag}
        
    return(sorted(agent_gr_dic.items(), key=lambda x: x[1]['grade'], reverse=True))


agents_dict = {idx: Agent() for idx in range(1, 41)}
for ag in agents_dict.values():
  ag.ff(agents_dict)
  break