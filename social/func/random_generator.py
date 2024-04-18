import os
import random
import json

from personality_managment import big_five_generator

# Range di età che vengono usati, con le relative probabilità
range_age = [(range(13, 17), 0.066), (range(17, 24), 0.171), (range(25, 34), 0.385), (range(35, 49), 0.207), (range(50, 102), 0.171)]
# Inseme dei topic di interesse
interest_list=json.load(open("SimPy/social/data/topic.json", "r"))



# In base ai dati degli utentei medi estrapolati da twitter, vado a generare l'eta dell'agent (mi baso su ddei dati di partenza reali)
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


# Fun per la generazione degli interessi per ognuno degli agent
def interest_gen():

    # Estrai due sottoargomenti casuali dalla stessa macrocategoria
    cat_mac1 = random.choice(list(interest_list.keys()))
    topic_res = random.sample(interest_list[cat_mac1], 2)

    # Estrai quattro sottoargomenti casuali da macrocategorie diverse
    other_cat_mac = [mc for mc in interest_list if mc != cat_mac1]
    topic_res.extend([random.choice(interest_list[m]) for m in random.sample(other_cat_mac, 4)])

    return topic_res


# Fun per generare la personalità dell'agent e stabilire l'activity in base ad essa
def personality_activity():
    # Dictionary della personalità dell'agent -> basata su valori che ne orientano i tratti in base al peso
    personality=big_five_generator()
    
    activity=round(((personality["apertura mentale"]+personality["estroversione"])/2),2)

    #0.8=active, 0.5=intermediate, 0.2 inactive
    #return random.choice([0.8, 0.5, 0.2])  

    # Prima ritorno il grado di activity, poi la perosnality
    return activity,personality

# Funzione usata per stabilire in base al livello ddi attività di un utente, se questo andrà a compiere o meno un azione
def content_interaction_gen_prob(prob):
    rand = random.random()
    #in base a ciò che ho estratto, l'utente vorra pubblicare o meno
    if rand < prob:
        return True  # L'utente pubblica
    else:
        return False

# Fun dedicata alla gestione e decisione dei tratti della personalità dell'agent, basandol sui big five
def personality_manager():
    # Al momento le personalità sono molto estreme, potrei usare una gaussiana per mitigare i valori e tenerli il più possibile nella media
    return