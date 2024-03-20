import random
import simpy as si
import numpy as np
from agent import Agent


#Simulations Settings
NUM_AGENTS=40
SIM_TIME=120
#inizialmente la notizia su cui si baseranno i post sarà questa
NEWS="Elon Musk ha rubato un cucchiaino in un ristorante"

"""
class Social:
   #adefinizione agents
   def __init(self,env):
      self.env=env
      self.agents=[Agent() for _ in range(40)]
"""      
   
def simulation_social(env,agents_list):
   while True:
      for ag in agents_list:
         #dopo che tutti gli utentei sono stati ccreati,propongo liste di amici papabili che l'agent sceglie se seguire o meno
         ag.find_friends(agents_list)
         
         #in base all'activity dell'utente, ogni tot tempo gli verrà posta la scelta se ccreare o meno un post su un determinato contenuto 
         env.process(ag.generate_post(NEWS))
         #stesso ragionamento, in base a dati demo*grafici
         #da pensare ancora come gestire il feed
         env.process(ag.intWithPost())



#MAIN
#generazione degli agents
agents_dict = {idx: Agent() for idx in range(1, NUM_AGENTS+1)}


for ag in agents_dict:
      #gli elenco tutti gli utenti e gli cheido man mano se è interessato a seguirli
      ag.start_follow()

#avvio della simulazione
env = si.Environment()
env.process(simulation_social(env,agents_dict))
#momentanemente attiva per 5 minuti
env.run(until=300)

   
   
   
   
   
   
   
   

   

'''      
   #WORK IN PROGRESS
   
      
       def pubblica_contenuto(self):
      while True:
         yield self.env.timeout(random.randint(1, 5))  # Intervallo casuale tra le pubblicazioni
         print(f"{self.nome} ha pubblicato un nuovo contenuto al tempo {self.env.now}")



      
      #risorsa condivisa, quando esaurisce gli altri devono aspettare
      self.risorsa_codivisa=si.Resource(env, risorsa_condivisa)

   
   
   
   def support_function(self, customer):
      #distribuzione normale è a campana, quindi i valori più centrali sono più probaiblemnte estratti, 1 è perchè non vogliam ovalori sotto l'1, 4 è la deviaione standars
      random_time=max(1,np.random.normal(self.*, 4))
      #yield è un generatore di processi
      #con timeout ho settato un periodo di attesa
      yield self.env.timeout(random_time)
      print("stampo il risultato")
 '''  
   
   