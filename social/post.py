import datetime
from comment import Comment  

# Classe dedicata al funzionamento dei post in generale

class Post:
    id_counter = 0
    def __init__(self,env,content,news,agent_id):
        Post.id_counter+=1
        self.env=env
        self.id = f"p-{agent_id}.{Post.id_counter}"
        self.agent_id=int(agent_id)
        self.news=news
        self.content=content
        # Campo dedicato ai 2/3 topic in cui può essere identetificata la news
        self.topic=[topic for topic in news["topics"] if topic]
        self.datatime=env.now
        # Sarà una lista di coppie id agente, contenuto del commento
        self.comments=[]
    
    # Fun usata per la creazione dei commenti
    #agent è un oggetto
    def create_comment(self,agent):
        from func.req_ollama_llm import gen_com
        com=gen_com(self.news,self.content,agent)
        # Salvo id di chi pubblica il commento, il commento stesso, e il tempo in cui lo ha fatto
        if com:
            # Creazione oggetto com
            self.comments.append(Comment(self.env,self.id,agent.id,com))
            print(f'LOG "{self.env.now}" ----> COMMENT: Done-int beetween agent {agent.id}, post {self.id}, post owner {self.agent_id}')