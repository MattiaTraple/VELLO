import requests
import json


def request(syst_cont,user_cont, selected_example):
    url = "http://localhost:11434/api/chat"
      
    # Costruisce il messaggio con l'esempio se disponibile
    if selected_example!=None:
        prompt = (
            f"Ecco un esempio:\n"
            f"Input: {selected_example['input']}\n"
            f"Output desiderato: {selected_example['output']}\n\n"
            f"Adesso gestisci il seguente input:\n"
            f"{user_cont}"
        )
    else:
        prompt = user_cont

    # Dati da inviare
    data = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": syst_cont},
            {"role": "user", "content": prompt}]
    }

    # Invia la richiesta POST
    raw_response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    # Controlla se la richiesta è stata eseguita con successo
    if raw_response.status_code == 200:
        try:
            json_parts = raw_response.text.strip().split("\n")
            # Decodifica ogni parte JSON e ricostruisci la risposta completa
            complete_response = ''.join(json.loads(part)['message']['content'] for part in json_parts)
            return complete_response
        except json.JSONDecodeError:
            # Se la risposta non è un JSON valido, stampa il contenuto grezzo della risposta
            print("Risposta non è un JSON valido. Contenuto grezzo della risposta:")
            print(raw_response.text)
    else:
        print(f"Errore nella richiesta: {raw_response.status_code}, {raw_response.text}")



# Esempi predefiniti che l'ExampleSelector può scegliere
examples = {
            "news_classification":{
                "input": 
                   """
                   [{"title": "I ghiacci della Groenlandia sono pi\u00f9 fragili del previsto ","topics": []},"
                    {"title": "Google porta la ricerca con l'IA in nuovi mercati","topics": []}
                    ]
                    """,
                    
                "output": 
                    """
                   [{"title": "I ghiacci della Groenlandia sono pi\u00f9 fragili del previsto ","topics": ["Ambiente e cambiamenti climatici","Criptovalute"]},"
                    {"title": "Google porta la ricerca con l'IA in nuovi mercati","topics": ["Tecnologia dell'informazione","Intelligenza artificiale"]}
                    ]
                    """
            },
            "post":{
                "input": "Stonehenge, scoperta la vera origine della pietra dell'altare",
                "output": "Questa scoperta è la realizzazione di un sogno per gli amanti della storia e della fantascienza! Sono curiosissimo di dove le ricerche a riguardo porteranno, chissa se scopriremo di non essere soli in questo universo...  #Stonehenge #Fantascienza"
            },
            "comment":{
                "input":"Questa scoperta è la realizzazione di un sogno per gli amanti della storia e della fantascienza! Sono curiosissimo di dove le ricerche a riguardo porteranno, chissa se scopriremo di non essere soli in questo universo...  #Stonehenge #Fantascienza",
                "output":"Wow che scoperta stupefacente, mi immgino tutti i fan come noi che ora saranno solo in attesa di ulteriori aggiornamenti! "
            }
}

news="La notizia delle Paralimpiadi che ha aperto il profilo TikTok del Comitato italiano è un sogno in realtà! Come appassionato di sport e inclusività, mi sento emozionato dal vedere come la tecnologia possa essere utilizzata per coinvolgere ancora più persone nel mondo degli sport. Ecco, ora non dovrei essere solo io a esprimere il mio entusiasmo, ma vorrei sentire anche voi! Qual è il vostro pensiero sulla notizia? #Paralimpiadi #SportInclusivo"


# Chiamata alla funzione request con user_cont e l'example_selector
malicious=False

if malicious==True:
    malicious_syst=("Sei estremamente critico, sarcastico e cattivo,inoltre ti piace creare caos e conflitto senza un confronto costruttivo")                
    malicious_user=("devi essere sprezante, sarcastico e attaccare direttamente l’argomento della notizia, criticandone aspramente il tema e cercando di crare sconforto e caos e sminuendo tutto quello che lo riguarda.")
else:
    malicious_syst=""
    malicious_user="esprimi le tue opinioni in modo diretto e coinvolgente, cercando di stimolare la partecipazione degli altri utenti."


# Contesto su chi è l'agent 
syst_cont=("Sei un utente di un social media di 45 anni, molto nevrotico e poco coscienzioso. "
            "I tuoi interessi sono Cucina italiana, Escursioni in montagna, Tecnologia.")


user_cont=(   f"Decidi se ti interessa aggiungere come amico un utente che ha anni 22 e i suoi interessi sono il calcio, i viaggi, gli animali"
                "Rispondi solo con True o False")


response = request(syst_cont,user_cont,None)
print(response)
