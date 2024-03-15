import random
def genera_age(range_eta_probabilita):
    # Calcola la somma delle probabilità
    totale_probabilita = sum(probabilita for _, probabilita in range_eta_probabilita)
    
    # Genera un numero casuale tra 0 e la somma delle probabilità
    numero_casuale = random.uniform(0, totale_probabilita)
    
    # Seleziona il range di età basato sul numero casuale
    accumulatore_probabilita = 0
    for eta, probabilita in range_eta_probabilita:
        accumulatore_probabilita += probabilita
        
        if numero_casuale < accumulatore_probabilita:
            # Genera un'età casuale all'interno del range selezionato
            eta_generata = random.randint(eta.start, eta.stop - 1)
            return eta_generata

def age():
    # Range utenti twitter
    range_age = [(range(13, 17), 0.066), (range(17, 24), 0.171), (range(25, 34), 0.385), (range(35, 49), 0.207), (range(50, 102), 0.171)]
    eta_generata = genera_age(range_age)