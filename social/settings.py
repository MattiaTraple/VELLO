# Questo file è dedicato ai settings della simulazione e a tutte le librerie comuni
from collections import namedtuple
#from social.func.req_openia_llm import gen_define_news

class Config:
    # Numero di agenti che verranno ccreati
    NUM_AGENTS = 10
    # Durata della simulazione
    SIM_TIME =1400
    # Limite iniziale di amici fissati
    NUM_FRIEND = 3

    # Lista notizie con notizia di defaul riportata
    NEWS = [{"name": "Sale il valore di Bitcoin, di conseguenza l'inquinamento aumenta", "topics": ["Criptovalute", "Ambiente e cambiamenti climatici", ""]}]

    # Post Presenti nel feed
    NUM_FEED = 5
    # Lista momentanea in cui salvo i post di tutti gli utenti
    POST_DATABASE = []

# Creazione dell'oggetto di configurazione
config = Config()

