


# Classe dedicata al funzionamento dei post in generale
class Post:
    id_counter = 0
    def __init__(self,content,news):
        Post.id_counter+=1
        self.id = Post.id_counter
        self.news=news
        self.content=content
        # Sarà una lista di coppie id agente, contenuto del commento
        self.comments=[]
    