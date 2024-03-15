import random
import simpy as si
import numpy as np
from random_generator import post_gen_prob
from agent import Agent


#Simulations Settings
NUM_AGENTS=40
#do un limite iniziale di persone che possono essere seguite
MAX_FOLLOW=5
MIN_FOLLOW=40
SIM_TIME=120



class Social:
   #adefinizione agents
   def __init(self,env):
      self.env=env
      
   
   #WORK IN PROGRESS
   
   #funzione dedicata alla creazione e generazione del post
   def generate_post(topic, agent):
      #datatime di generazione
      if post_gen_prob(agent.activity):
         #fare richiesta a API di GPT per generare post a riguardo (vengono fornite caratteristiche utente in mdoo da personalizzare in base a quelle il contenuto)
         
         return "SYS---> "+agent.nome+" ha postato"
      return "SYS---> "+agent.nome+" non ha postato nulla"
      