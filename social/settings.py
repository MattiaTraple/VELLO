# Questo file è dedicato ai settings della simulazione e a tutte le librerie comuni
from collections import namedtuple
#from social.func.req_ollama_llm import gen_define_news

class Config:
    # Numero di agenti che verranno ccreati
    NUM_AGENTS = 2
    # Durata della simulazione
    SIM_TIME =500
    # Limite iniziale di amici fissati
    NUM_FRIEND = 2

    # Lista notizie con categorizzazione
    NEWS = []

    # Post Presenti nel feed
    NUM_FEED = 2
    # Lista momentanea in cui salvo i post di tutti gli utenti
    POST_DATABASE = []

    #Percorso per posizione file json che raccolgono info sulla sim e servono per il funzionamento
    DATA_POSITION="/data/homes_data/mattiatrapletti/SimPy/social/data/"
    
# Creazione dell'oggetto di configurazione
config = Config()

