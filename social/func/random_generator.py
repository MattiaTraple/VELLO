import random
import json

#RANGE E INTERESSI
range_age = [(range(13, 17), 0.066), (range(17, 24), 0.171), (range(25, 34), 0.385), (range(35, 49), 0.207), (range(50, 102), 0.171)]
interest_list = [
    ("Viaggi e avventure", ["Escursioni in montagna", "Viaggi in camper", "Turismo culturale", "Viaggi low-cost", "Destinazioni esotiche"]),("Cucina e ricette", ["Cucina italiana", "Ricette vegetariane/vegane", "Cucina gourmet", "Dessert e dolci", "Cucina internazionale"]),("Fitness e benessere", ["Allenamento a corpo libero", "Yoga e meditazione", "Alimentazione sana", "Programmi di dimagrimento", "Allenamento funzionale"]),("Arte e creatività", ["Pittura ad olio", "Fotografia di paesaggi", "Scultura", "Disegno e illustrazione", "Arte digitale"]),("Musica e concerti", ["Rock", "Hip hop", "Jazz", "Musica classica", "Indie"]),("Tecnologia e innovazione", ["Intelligenza artificiale", "Criptovalute", "App per la produttività", "Fotografia digitale", "Nuove app e software"]),("Film e serie TV", ["Fantascienza", "Drammi", "Commedie romantiche", "Thriller psicologici", "Anime"]),("Libri e lettura", ["Romanzi storici", "Fantasy epico", "Saggi di divulgazione scientifica", "Poesia contemporanea", "Libri d'arte"]),("Fotografia e editing", ["Fotografia di viaggio", "Ritratti in studio", "Fotografia di architettura", "Editing di paesaggi", "Fotografia naturalistica"]),("Politica e attualità", ["Politica internazionale", "Economia", "Ambiente e cambiamenti climatici", "Diritti umani", "Attualità locali"]),("Ambiente e sostenibilità", ["Riduzione della plastica", "Energia rinnovabile", "Agricoltura biologica", "Mobilità sostenibile", "Conservazione della biodiversità"]),("Moda e stile", ["Moda streetwear", "Stile vintage", "Alta moda", "Abbigliamento sostenibile", "Consigli di abbinamento"]),("Fai da te e progetti manuali", ["Lavorazione del legno", "Cucito e ricamo", "Falegnameria", "Fai da te per la casa", "Progetti di bricolage"]),("Sport e competizioni", ["Calcio", "Tennis", "Surf", "Pallavolo", "Maratone e corsa"]),("Giochi e videogiochi", ["Giochi di ruolo (RPG)", "Sparatutto in prima persona (FPS)", "Strategia in tempo reale (RTS)", "Giochi indie", "Giochi per dispositivi mobili"]),("Animali domestici e cura degli animali", ["Addestramento dei cani", "Cura dei gatti", "Acquariologia", "Allevamento di animali esotici", "Protezione degli animali"]),("Psicologia e benessere mentale", ["Gestione dello stress", "Crescita personale", "Mindfulness", "Terapia cognitivo-comportamentale (TCC)", "Psicologia positiva"]),    ("Educazione e apprendimento", ["Corsi online", "Lingue straniere", "Sviluppo personale", "Corsi accademici", "Tecnologia dell'informazione"]),("Finanza personale e investimenti", ["Risparmio", "Investimenti azionari", "Criptovalute", "Pianificazione pensionistica", "Immobiliare"]),("Relazioni interpersonali e consigli sentimentali", ["Consigli di relazione", "Amicizia", "Consigli per appuntamenti", "Gestione dei conflitti", "Crescita delle relazioni di coppia"])
]


#AGE GENERATOR ---> START
def age_gen():
    # Calcola la somma delle probabilità
    totale_probabilita = sum(probabilita for _, probabilita in range_age)
    
    # Genera un numero casuale tra 0 e la somma delle probabilità
    numero_casuale = random.uniform(0, totale_probabilita)
    
    # Seleziona il range di età basato sul numero casuale
    accumulatore_probabilita = 0
    for eta, probabilita in range_age:
        accumulatore_probabilita += probabilita
        
        if numero_casuale < accumulatore_probabilita:
            # Genera un'età casuale all'interno del range selezionato
            eta_generata = random.randint(eta.start, eta.stop - 1)
            return eta_generata


#INTEREST GENERATOR ---> START
def interest_gen():
    #_,sottotopi_1 = random.choice(interest_list)
    #sottotopi_scelti_1 = random.sample(sottotopi_1, 2)
    sottotopi_scelti_4=[]
    while len(sottotopi_scelti_4) < 4:
        _,sottotipo_scelto = random.choice(interest_list)
        sotto=random.sample(sottotipo_scelto, 1)
        if sotto not in sottotopi_scelti_4:
            sottotopi_scelti_4.extend(sotto)
    #interst_topic=sottotopi_scelti_1+sottotopi_scelti_4
    return(sottotopi_scelti_4)


#ACTIVITY GENERATOR
def activity_gen():
    #0.8=active, 0.5=intermediate, 0.2 inactive
    return random.choice([0.8, 0.5, 0.2])  


#POST-PROBABILITY GENERATOR ---> START
def post_gen_prob(prob):
    rand = random.random()
    #in base a ciò che ho estratto, l'utente vorra pubblicare o meno
    if rand < prob:
        return True  # L'utente pubblica
    else:
        return False
