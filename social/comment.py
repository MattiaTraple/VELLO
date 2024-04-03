# Classe dedicata alla gestione dei ccommenti dei post -> forse possibile accorpare ma per ora tiene ordine
import datetime


class Comment:

    def __init__(self,env,post,content):
        self.post_id = post.id
        self.agent=post.agent
        self.content=content
        self.datetime=env.now
        