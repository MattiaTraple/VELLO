import random
import json

# Range di età che vengono usati, con le relative probabilità(specificare la provenienza dei dati)
range_age = [(range(13, 17), 0.049), (range(18, 24), 0.226), (range(25, 34), 0.296), (range(35, 44), 0.19), (range(45, 54), 0.113),(range(55,64), 0.071), (range(65, 100), 0.056)]
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

    # Estrai 5 sottoargomenti casuali da macrocategorie diverse
    other_cat_mac = [mc for mc in interest_list if mc != cat_mac1]
    topic_res.extend([random.choice(interest_list[m]) for m in random.sample(other_cat_mac, 5)])

    return topic_res


# Fun per generare la personalità dell'agent e stabilire l'activity in base ad essa
def personality_activity(eta):
    # Dictionary della personalità dell'agent -> basata su valori che ne orientano i tratti in base al peso
    personality=big_five_generator()
    
    # Definire il tempo medio speso sui social media per ciascun range di età
    # Il tempo di utilizzo è convertito in proporzione per rappresentarlo in ore, ad esempio 2.46 ore equivale a 2.27, la conversione è stata eseguita sui valori presi dalle analisi fatte su alcuni social
    tempo_medio_social = {
        (16, 24): 2.27,
        (25, 34): 2.24,
        (35, 44): 2.11,
        (45, 54): 2.0,
        (55, 64): 1.23,
        (65,100) : 0.30
    }

    # Trova il tempo medio corretto per l'età dell'utente
    tempo_base = 0
    for range_eta, tempo in tempo_medio_social.items():
        if range_eta[0] <= eta <= range_eta[1]:
            tempo_base = tempo
            break

    # Calcola il grado di attività basato sul tempo medio e sul livello di estroversione
    grado_attivita = (tempo_base / 2.5) * personality["estroversione"]
    grado_attivita = max(0.01, min(grado_attivita, 1))  # Limita tra 0.01 e 1
    
    # Aggiungi una componente di casualità controllata
    casualita = random.uniform(-0.1, 0.1)  # Varianza controllata da -0.1 a 0.1
    grado_attivita += casualita
    grado_attivita = max(0.01, min(grado_attivita, 1))  # Limita tra 0.01 e 1

    # Prima ritorno il grado di activity, poi la personality
    return grado_attivita,personality

# Funzione usata per stabilire in base al livello ddi attività di un utente, se questo andrà a compiere o meno un azione
# Al momento viene un po pilotato per alzare il numeto di interazioni tra utenti/post/commenti
def content_interaction_gen_prob(prob):
    rand = random.random()
    #in base a ciò che ho estratto, l'utente vorra pubblicare o meno
    if rand < prob+15:
        return True  # L'utente pubblica
    else:
        return False


# Fun dedicata alla gestione e decisione dei tratti della personalità dell'agent, basandol sui big five
def personality_manager():
    # Al momento le personalità sono molto estreme, potrei usare una gaussiana per mitigare i valori e tenerli il più possibile nella media
    return



# Dict che viene poi salvato nel rispettivo attributo del agente


# Fun per generazione dei 5 valori per i 5 big five di ogni agents
def big_five_generator():
    deviazione_standard = 0.2
    big_five = {}
    # Generazione iniziale dei valori 
    for trait in ["apertura_mentale", "coscienziosità", "estroversione", "gradevolezza", "nevroticismo"]:
        value = round(random.gauss(0.5, deviazione_standard), 2)
        value = max(min(value, 1), 0.01)  # Limitiamo i valori nell'intervallo da 0.01 a 1
        big_five[trait] = value
   
    return big_five

# Fun usata per stabilire verso ceh tipologia di commento/post soi vuole andare in base a delle soglie che possono essere superate nei valori dei big 5
def big_five_personalizer(personality):
    # ...Fai in modo di...
    # Val max e min
    max,min=min_max_dic_finder(personality)
    
    # PER ORA RESTITUISCO SOLAMENTE IL TRATTO NEGATIVO E IL TRATTO POSITIVO PIU ALTO
    # Seleziono solo il più estremo tra max e min
    ext=extreme_selector(max,min)
    prompt=""

    #Estroversione
    if ext[0]=="estroversione":
        if ext[1] > 0.7:
            prompt += "Rispondere in modo energico e coinvolgente. "
        elif ext[1] < 0.3:
            prompt += "Rispondere in modo tranquillo e riservato. "
    
    # Gradevolezza
    if ext[0]=="gradevolezza":
        if ext[1] > 0.7:
            prompt += "essere gentile e collaborativo. "
        elif ext[1] < 0.3:
            prompt += "essere più diretto e assertivo. "
    
    # Coscienziosità
    if ext[0]=="coscienziosità":
        if ext[1] > 0.7:
            prompt += "fornire dettagli accurati e ben organizzati. "
        elif ext[1] < 0.3:
            prompt += "Rispondere in modo conciso e informale. "
    
    # Nevroticismo
    if ext[0]=="nevroticismo":  
        if ext[1] > 0.7:
            prompt += "Esprimere una leggera preoccupazione o cautela. "
        elif ext[1] < 0.3:
            prompt += "Rispondere con sicurezza e serenità. "
    
    # Apertura Mentale
    if ext[0]=="apertura_mentale":
        if ext[1] > 0.7:
            prompt += "essere creativo e esplorativo nella risposta. "
        elif ext[1] < 0.3:
            prompt += "Rispondere in modo semplice e pratico. "
    
    return max[0],min[0]
    
    #devo decidere se voglio restituire una stringa da aggiungere al prompt o altro
    
# Fun usata per cercare i tratti dei big 5 maggiori o minori
def min_max_dic_finder(personality):
    # Trova la chiave e il valore massimi
    max_key = max(personality, key=personality.get)
    max_value = personality[max_key]
    
    # Trova la chiave e il valore minimi
    min_key = min(personality, key=personality.get)
    min_value = personality[min_key]
    
    return (max_key, max_value), (min_key, min_value)

def extreme_selector(max,min):
    # Calcola quanto il massimo si avvicina a 1 e il minimo a 0
    distanza_max = 1 - max[1]
    distanza_min = min[1]
    
    # Se il valore massimo è più estremo, ritorna il massimo, altrimenti il minimo
    if distanza_max < distanza_min:
        return max
    else:
        return min