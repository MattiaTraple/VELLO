# TEST FATTO CON MODALITà RICHIESTA SINGOLA
"""
import requests
import json

url = "http://localhost:11434/api/chat"
payload = {
  "model": "gemma:2b",
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    }
  ]
}

# Invia la richiesta POST con i dati JSON
response = requests.post(url, json=payload)

# Controlla se la richiesta è stata eseguita con successo
if response.status_code == 200:
    try:
        # Dividi la risposta in parti
        parts = response.text.split('\n')
        
        # Filtra le parti vuote e decodifica ogni parte come JSON
        json_parts = [json.loads(part) for part in parts if part]
        
        # Unisci le risposte
        complete_response = ''.join(part['response'] for part in json_parts)
        
        print("Risposta del server:", complete_response)
    except json.JSONDecodeError as e:
        # Se la decodifica fallisce, stampa l'errore e il contenuto grezzo della risposta
        print("Errore di decodifica JSON:", e)
        print("Contenuto grezzo della risposta:", response.text)
else:
    print(f"Errore nella richiesta: {response.status_code}, {response.text}")
""" 
# TEST FATTO CON MODALITà CHAT

import requests
import json

# URL dell'endpoint
url = "http://localhost:11434/api/chat"

# Dati da inviare
data = {
    "model": "llama3",
    "messages": [
        {
            "role": "user",
            "content": "why is the sky blue?"
        }
    ]
}

# Invia la richiesta POST
response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

# Controlla se la richiesta è stata eseguita con successo
if response.status_code == 200:
    try:
        json_parts = raw_response.strip().split("\n")
        
        # Decodifica ogni parte JSON e ricostruisci la risposta completa
        complete_response = ''.join(json.loads(part)['message']['content'] for part in json_parts)

    except json.JSONDecodeError:
        # Se la risposta non è un JSON valido, stampa il contenuto grezzo della risposta
        print("Risposta non è un JSON valido. Contenuto grezzo della risposta:")
        print(response.text)
else:
    print(f"Errore nella richiesta: {response.status_code}, {response.text}")

# TEST FATTO CON MODELLO CHE MANTIENE STORIA, UTILE PER ME 
"""
{
  "model": "llama3",
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    },
    {
      "role": "assistant",
      "content": "due to rayleigh scattering."
    },
    {
      "role": "user",
      "content": "how is that different than mie scattering?"
    }
  ]
}'
"""