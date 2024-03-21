import json

# La lista da salvare
lista = [1, 2, 3, 4, 5]

# Nome del file JSON
nome_file = "lista.json"

# Salvataggio della lista nel file JSON
with open(nome_file, 'w') as f:
    json.dump(lista, f)

print("Lista salvata correttamente nel file:", nome_file)


