# Classe dedicata alla gestione dei ccommenti dei post -> forse possibile accorpare ma per ora tiene ordine
class Post:
    id_counter = 0
    def __init__(self,content,news,agent_id):
        Post.id_counter+=1
        self.id = f"p-{agent_id}.{Post.id_counter}"
        self.agent_id=int(agent_id)
        self.news=news
        self.content=content
        # Campo dedicato ai 2/3 topic in cui può essere identetificata la news
        self.topic=[topic for topic in news.topics if topic]
        self.datatime=datetime.datetime.now()
        # Sarà una lista di coppie id agente, contenuto del commento
        self.comments=[]