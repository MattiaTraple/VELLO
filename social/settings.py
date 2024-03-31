# Questo file è dedicato ai settings della simulazione e a tutte le librerie comuni
from collections import namedtuple
#from social.func.req_openia_llm import gen_define_news

class Config:
    # Numero di agenti che verranno ccreati
    NUM_AGENTS = 5
    # Durata della simulazione
    SIM_TIME = 600
    # Limite iniziale di amici fissati
    NUM_FRIEND = 10

    # Notizia di prova fornita
    News = namedtuple('News', ['name', 'topics'])
    NEWS = News(name="Sale il valore di Bitcoin, di conseguenza l'inquinamento aumenta", topics=["Criptovalute", "Ambiente e cambiamenti climatici", ""])
    # Versione ancora non provata
    #nam,tpc=gen_define_news()
    #NEWS = News(name=nam, topics=["Criptovalute", "Ambiente e cambiamenti climatici", ""])

    # Post Presenti nel feed
    NUM_FEED = 10
    # Lista momentanea in cui salvo i post di tutti gli utenti
    POST_DATABASE = []

# Creazione dell'oggetto di configurazione
config = Config()

