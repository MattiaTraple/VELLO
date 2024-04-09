import pymongo
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client.get_database("local")
collection = db.get_collection("Agents")


documento_di_prova = {
    "campo_di_prova": "valore_di_prova"
}

# Inserimento del documento nella collezione
inserimento = collection.insert_one(documento_di_prova)


if inserimento.inserted_id:
    print("Il documento con il campo di prova è stato inserito con successo.")
else:
    print("Si è verificato un errore durante l'inserimento del documento.")