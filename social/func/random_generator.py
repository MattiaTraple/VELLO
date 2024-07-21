import random
import json

# Range di età che vengono usati, con le relative probabilità(specificare la provenienza dei dati)
range_age = [(range(13, 17), 0.049), (range(18, 24), 0.226), (range(25, 34), 0.296), (range(35, 44), 0.19), (range(45, 54), 0.113),(range(55,64), 0.071), (range(65, 100), 0.113)]
# Inseme dei topic di interesse
interest_list=json.load(open("/data/homes_data/mattiatrapletti/SimPy/social/data/topic.json", "r"))



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
def personality_activity(età):
    # Dictionary della personalità dell'agent -> basata su valori che ne orientano i tratti in base al peso
    personality=big_five_generator()
    
    # Definire il tempo medio speso sui social media per ciascun range di età
    tempo_medio_social = {
        (16, 24): 2.46,
        (25, 34): 2.40,
        (35, 44): 2.19,
        (45, 54): 2.01,
        (55, 64): 1.39
    }

    # Trova il tempo medio corretto per l'età dell'utente
    tempo_base = 0
    for range_eta, tempo in tempo_medio_social.items():
        if range_eta[0] <= età <= range_eta[1]:
            tempo_base = tempo
            break
    
    # Assicurati che personality sia tra 0.01 e 1
    personality = max(0.01, min(personality, 1))  

    # Calcola il grado di attività basato sul tempo medio e sul livello di estroversione
    grado_attivita = (tempo_base / 2.5) * personality
    grado_attivita = max(0.01, min(grado_attivita, 1))  # Limita tra 0.01 e 1
    
    # Aggiungi una componente di casualità controllata
    casualita = random.uniform(-0.1, 0.1)  # Varianza controllata da -0.1 a 0.1
    grado_attivita += casualita
    grado_attivita = max(0.01, min(grado_attivita, 1))  # Limita tra 0.01 e 1

    return grado_attivita
    
    


    # Prima ritorno il grado di activity, poi la personality
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



# Dict che viene poi salvato nel rispettivo attributo del agente
big_five = {}

# Fun per generazione dei 5 valori per i 5 big five di ogni agents
def big_five_generator():
    deviazione_standard = 0.2
    
    # Generazione iniziale dei valori 
    for trait in ["apertura_mentale", "coscienziosità", "estroversione", "gradevolezza", "nevroticismo"]:
        value = round(random.gauss(0.5, deviazione_standard), 2)
        value = max(min(value, 1), 0.01)  # Limitiamo i valori nell'intervallo da 0.01 a 1
        big_five[trait] = value
    
    balance_function()
   
    return big_five

# Fun aus per eseguire opportuni bilanciamenti agli indici estratti
def balance_function():
    # Vero e prorpio bilanciamento
    # Bilancio la coppia e-g
    big_five["estroversione"],big_five["gradevolezza"]=couple_balancer(big_five["estroversione"],big_five["gradevolezza"])
    # Bilancio la coppia n-c
    big_five["nevroticismo"],big_five["estroversione"]=couple_balancer(big_five["nevroticismo"],big_five["estroversione"])
    # Bilancio la coppia c-g
    big_five["coscienziosità"],big_five["gradevolezza"]=couple_balancer(big_five["coscienziosità"],big_five["gradevolezza"])


# Fun aus a cui passo due campi e li bilnacio
def couple_balancer(big_1, big_2):
    # Differenza tra i campi dopo la quale viene iniziato il bilanciaento
    soglia=0.3
    # Se il || della differenza è sopra la soglia, quindi troppa differneza
    if abs(big_1-big_2) > soglia:
        if big_1>big_2:
            big_2+=0.1
        else:
            big_1+=0.1
    return round(big_1,2),round(big_2,2)
