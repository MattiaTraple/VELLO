import json
jso=[
    {
        "title": "Dalla Nasa la prima canzone hip-hop nello spazio profondo",
        "topics": [
            "Musica classica",
            "Hip hop"
        ]
    },
    {
        "title": "Novit\u00e0 Mediaset, speciali Amici-Verissimo e c\u00e8 Leotta&nbsp;",
        "topics": []
    },
    {
        "title": "Volo no-stress, 10 tips per viaggiare in aereo",
        "topics": [
            "Viaggi low-cost",
            "Turismo culturale"
        ]
    },
    {
        "title": "Tredici citt\u00e0 con il bollino rosso, venerd\u00ec saranno 17",
        "topics": []
    },
    {
        "title": "Le mostre del weekend, da Guido Reni e Magritte a Merz",
        "topics": [
            "Arte digitale",
            "Pittura ad olio"
        ]
    },
    {
        "title": "Von der Leyen: Non lascer\u00f2 che gli estremismi distruggano lU\u00e8",
        "topics": []
    },
    {
        "title": "Forte scossa di terremoto nella zona dei Campi Flegrei ",
        "topics": [
            "Ambiente e cambiamenti climatici",
            "Conservazione della biodiversit\u00e0"
        ]
    },
    {
        "title": "Joe Biden ha il Covid ma assicura, mi sento ben\u00e8",
        "topics": []
    },
    {
        "title": "Francia: in fiamme un edificio residenziale a Nizza, 7 morti",
        "topics": [
            "Politica internazionale",
            "Economia"
        ]
    },
    {
        "title": "Giochi di ruolo (RPG)",
        "topics": [
            "Fantascienza",
            "Drammi"
        ]
    },
    {
        "title": "Surf",
        "topics": [
            "Sport estremi",
            "Turismo culturale"
        ]
    },
    {
        "title": "Pallavolo",
        "topics": []
    },
    {
        "title": "Maratone e corsa",
        "topics": [
            "Gestione dello stress",
            "Crescita personale"
        ]
    },
    {
        "title": "Giochi indie",
        "topics": [
            "Tecnologia dellinformazione",
            "Criptovalute"
        ]
    },
    {
        "title": "Addestramento dei cani",
        "topics": [
            "Animale domestico",
            "Conservazione della biodiversit\u00e0"
        ]
    }
]

with open('/data/homes_data/mattiatrapletti/SimPy/social/data/topic.json', 'r', encoding='utf-8') as file:
        topic_data_tot = json.load(file)
    # Considero solo le sottocategorie
topic_data = [item for sublist in topic_data_tot.values() for item in sublist]

def detect_miss_classification(response,topic_list):
    res=[]
    for item in response:
        if item['title'] not in topic_list:
            if len(item['topics'])!=0:
                res.append(item)
    return res

print(detect_miss_classification(jso,topic_data))