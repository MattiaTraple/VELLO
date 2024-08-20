import requests
import json


news=[ 
    {
        "title": "I ghiacci della Groenlandia sono pi\u00f9 fragili del previsto ",
        "topics": []
        },
    {
        "title": "Toxic di Saule Bliuvaite Pardo d'oro a Locarno",
        "topics": []
        },
    {
        "title": "Lazio: Baroni 'pronti per l'esordio, Dia dar\u00e0 una grande mano'",
        "topics": []
        }]


def request(syst_cont,user_cont, selected_example):
    url = "http://localhost:11434/api/chat"
      
    # Costruisce il messaggio con l'esempio se disponibile
    if selected_example:
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
            complete_response = complete_response[0:-1]
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


# Chiamata alla funzione request con user_cont e l'example_selector
malicious=True

if malicious==True:
    malicious_syst=("Sei un utente estremamente arrogante e maleducato. Hai l'abitudine di ridicolizzare ciò di cui parlano gli articoli,facendo commenti sprezzanti e critici." 
                    "Ti piace sminuire e screditare le notizie con sarcasmo, attacchi personali e disprezzo.")
    malicious_user=("usi un tono derisorio per criticare aspramente la notizia e far sembrare inutile o ridicolo ciò che viene discusso. "
                    "Attacca senza pietà l'argomento e chi potrebbe essere d'accordo con esso, facendo sembrare le loro opinioni stupide e prive di valore.")
else:
    malicious_syst=""
    malicious_user="esprimi le tue opinioni in modo diretto e coinvolgente, cercando di stimolare la partecipazione degli altri utenti."

syst_cont=( f"Sei un utente di un social media, hai un età di 33, tendi ad essere abbastanza estroverso, con una bassa apertura_mentale."
            f"I tuoi interessi sono Calcio, Surf, Programmi di dimagrimento, Investimenti azionari, Progetti di bricolage, Criptovalute, Alta moda ma nel generare non devi menzionare direttamente questi argomenti. "
             f"{malicious_syst}")
    
     # Contesto cosa deve fare l'agent
user_cont=( f"Hai appena letto della notizia 'Juve, Mbangula: il gol? Pensavo fosse solo un sogno' di cui i topic centrali sono Calcio , sport."
            f"Scrivi un post a riguardo in italiano che pubblicheresti sul social in cui {malicious_user}"
            "Oltre al testo del post non scrivere nient'altro nella risposta")


response = request(syst_cont,user_cont,examples["post"])
print(response)
