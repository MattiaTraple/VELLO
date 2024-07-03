# Classe dedicata alla gestione dei ccommenti dei post -> forse possibile accorpare ma per ora tiene ordine
class Comment:

    def __init__(self,env,post_id,agent_id,content):
        self.post_id = post_id
        # Non è l'oggetto ma solo l'id dell'agent
        self.agent=agent_id
        self.content=content
        self.datetime=env.now
        