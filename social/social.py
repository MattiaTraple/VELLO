import random
import simpy as si
import numpy as np
from social.func.random_generator import post_gen_prob
from social.func.req_openia_llm import o
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
   
   #news andrà a contenere una notizia sulla quale voglio fargli pubblicare il post che devo ancora decidere
   def generate_post(topic, agent,news):
      #datatime di generazione
      if post_gen_prob(agent.activity):
         #fare richiesta a API di GPT per generare post a riguardo (vengono fornite caratteristiche utente in mdoo da personalizzare in base a quelle il contenuto)
         #potrei eseguire una ristrutturazione della domanda usando i temi o qui o in unafunzione tra questa e quella in openia
         openia_generate(topic, agent,news)
         return "SYS---> "+agent.nome+" ha postato"
      return "SYS---> "+agent.nome+" non ha postato nulla"
      