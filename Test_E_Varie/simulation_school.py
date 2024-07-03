import simpy


class School:
    def __init__(self, env):
        # Inizializza l'oggetto della scuola con l'ambiente di simulazione passato come parametro.
        self.env = env
        # Crea un evento che rappresenta la fine della lezione.
        self.class_ends = env.event()
        # Crea processi per gli studenti (pupil) e il campanello (bell).
        
        
        self.publish_post_procs = [env.process(self.publish_post(agent)) for agent in agent_list]
        
        
        
        self.bell_proc = env.process(self.bell())

    def publish_post(agent):
        # Il campanello suona due volte.
        while True:
            # Aspetta 45 unità di tempo prima di suonare il campanello.
            yield self.env.timeout(45)
            # Notifica agli studenti che la lezione è finita-> possono continuare a produrre  
            self.class_ends.succeed()
            print("successo")
            # Reimposta l'evento della fine della lezione per il prossimo suono del campanello.
            self.class_ends = self.env.event()
            # Stampa una riga vuota per separare le lezioni.
            print()

    def publish_post(agent):
        
        while True:
            post_publication
            # mette in pausa il processo dello studente fino a quando non viene attivato l'evento self.class_ends. Quando l'evento self.class_ends viene attivato (tramite self.class_ends.succeed() nel metodo bell), il processo dello studente si sblocca e continua l'esecuzione.
            yield self.class_ends

# Crea un ambiente di simulazione.
env = simpy.Environment()
# Crea un'istanza della scuola nell'ambiente di simulazione.
school = School(env)
# Avvia l'ambiente di simulazione.
env.run()