# Questo file è dedicato ai settings della simulazione
import os
from openai import OpenAI

# Numero di agenti che verranno ccreati
NUM_AGENTS=40
# Durata della simulazione
SIM_TIME=300
# Limite iniziale di amici fissati
NUM_FRIEND=10
# Notizia di prova fornita
NEWS="Elon Musk ha rubato un cucchiaino in un ristorante"

# Chiave API usata per le richieste
CLIENT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))
