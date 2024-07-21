import random

def personality_activity(eta, personality):
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
        if range_eta[0] <= eta <= range_eta[1]:
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

# Esempio di utilizzo
eta = 30
personality = 0.7
grado_attivita = personality_activity(eta, personality)
print(f"Il grado di attività per un utente di {eta} anni con estroversione {personality} è {grado_attivita:.2f}")
