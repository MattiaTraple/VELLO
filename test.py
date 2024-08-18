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


syst_cont=("Sei un assistente linguistico esperto nella categorizzazione delle notizie che verranno usate dagli utenti di un social per pubblicare dei post a riguardo."
            "Riceverai delle notizie con informazioni in formato JSON e Il tuo compito è classificare ogni notizia aggiungendo come campo di 'topic', una lista di almeno due argomenti inerenti alla notizia."
            "Gli argomenti disponibili si trovano nella seguente lista: {'ambiente','clima','animali','sostenibilità','salute','cibo','bambini poveri','ciclismo','vacanze'}.")


user_cont = (f"Queste sono le notizie che dovrai calssificare completandone il campo topic con la lista dei temi che vengono trattati nella notizia:{news}"
            "Rispondi solamente con quello che sarebbe il contenuto del Json copmpleto")

response = request(syst_cont,user_cont,examples["news_classification"])
print(response)
