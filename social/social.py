import random
import simpy as si
import numpy as np
from social.func.random_generator import post_gen_prob
from social.func.req_openia_llm import o
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
   
def simulation_social(env):
   #generazione degli agents
   agents_list=[Agent() for _ in range(40)]

   #creazione delle connessioni di amicizia
   for ag in agents_list:
      #gli elenco tutti gli utentei e gli cheido man mano se è interessato a seguirli
      env.process(ag.start_follow(agent_candidate))
      #in base all'activity dell'utente, ogni tot tempo gli verrà posta la scelta se ccreare o meno un post su un determinato contenuto 
      env.process(ag.generate_post(NEWS))
      #stesso ragionamento, in base a dati demografici
      env.process(ag.intWithPost())
   



#avvio della simulazione
env = si.Environment()
env.process(simulation_social(env))
#momentanemente attiva per 5 minuti
env.run(until=300)
   
   
   
   
   
   
   
   
   

   

      
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
   
   
   