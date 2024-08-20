# Questo file è dedicato ai settings della simulazione e a tutte le librerie comuni

class Config:
    # Numero di agenti che verranno ccreati
    NUM_AGENTS = 5
    # Durata della simulazione
    SIM_TIME =1000
    # Limite iniziale di amici fissati
    NUM_FRIEND = 5

    # Lista notizie con categorizzazione
    NEWS = []

    # Post Presenti nel feed
    NUM_FEED = 4
    # Lista momentanea in cui salvo i post di tutti gli utenti
    POST_DATABASE = []

    #Percorso per posizione file json che raccolgono info sulla sim e servono per il funzionamento
    DATA_POSITION="/data/homes_data/mattiatrapletti/SimPy/social/data/"
    
    # Decido se rieseguire la classificazione delle news
    RELOAD_NEWS=True
    
# Creazione dell'oggetto di configurazione
config = Config()

