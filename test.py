from pymongo import MongoClient
import ssl
import sys

uri = "mongodb+srv://mattiatrapletti:mattiaatlassimpy@cluster0.l98hiqh.mongodb.net/"
try:
    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)
except Exception as e:
    print(f"An error occurred: {e}")
    
db=client.get_database("SimPy")
collection = db["Simulations"]
documents = collection.find()
for document in documents:
        print(document)
    
'''import pymongo
import certifi
import ssl
import sys

ca = certifi.where()

# Connessione a mongo con Atlas
uri = "mongodb+srv://mattiatrapletti:mattiaatlassimpy@cluster0.l98hiqh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
try:
    client = pymongo.MongoClient(uri, tlsCAFile=ca, serverSelectionTimeoutMS=5000)  # Imposta un timeout di 5 secondi
except pymongo.errors.ConfigurationError as e:
    print(f"An Invalid URI host error was received. Is your Atlas host name correct in your connection string? Error: {e}")
    sys.exit(1)

# Prova a selezionare il server per verificare la connessione
try:
    client.admin.command('ping')
    print("Connesso al database MongoDB Atlas!")
except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"Errore di connessione al server MongoDB: {e}")
    sys.exit(1)

# Connetti al database "SimPy"
db = client.get_database("SimPy")
collection = db["Simulations"]

# Trova tutti i documenti nella collezione
documents = collection.find()

# Itera sui documenti e stampali a schermo
for document in documents:
    print(document)
    '''