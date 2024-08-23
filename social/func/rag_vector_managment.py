from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


model = SentenceTransformer('all-MiniLM-L6-v2')
# Setto dim embedding
dimension = 384
index = faiss.IndexFlatL2(dimension)
# Dic mapping ID
metadati_agenti = {}
# Dic memo dati embedding
data = {}
   
   
    
# Fun lanciata quando un utente commenta o pubblica un post
def add_agent_action(agente_id, testo):
    # Crea embedding per il testo
    embedding = model.encode([testo])
    # Aggiungi l'embedding all'indice FAISS
    index.add(embedding.astype('float32'))
    # Ottieni l'indice dell'embedding appena aggiunto
    indice = index.ntotal - 1
    # Memorizza l'indice dell'embedding nel dizionario dei metadati
    if agente_id not in metadati_agenti:
        metadati_agenti[agente_id] = []
    metadati_agenti[agente_id].append(indice)
    # Memorizza i dati associati all'embedding
    data[indice] = (agente_id, testo)


# Fun usata per recuperaere le azioni precednti di un certo agent
def get_agent_action(agente_id, top_k=4):
    if agente_id not in metadati_agenti:
        return []
    indici = metadati_agenti[agente_id]
    indici_pertinenti = indici[-top_k:]
    contenuti = [data[i][1] for i in indici_pertinenti]
    
    return contenuti