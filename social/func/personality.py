import random

# Dict che viene poi salvato nel rispettivo attributo del agente
big_five = {}

# Fun per generazione dei 5 valori per i 5 big five di ogni agents
def big_five_generator():
    deviazione_standard = 0.2
    
    # Generazione iniziale dei valori 
    for trait in ["apertura mentale", "coscienziosità", "estroversione", "gradevolezza", "nevroticismo"]:
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


