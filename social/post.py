import datetime
from comment import Comment  

# Classe dedicata al funzionamento dei post in generale

class Post:
    def __init__(self,env,content,news,agent_id,post_count):
        self.env=env
        self.id = f"p-{agent_id}.{post_count}"
        self.agent_id=int(agent_id)
        self.news=news
        self.content=content
        # Field for the post's
        self.topic=[topic for topic in news["topics"] if topic]
        self.datatime=env.now
        # List of coupple in form "id_agent:comment"
        self.comments=[]
    
    # Fun used to the comment generation
    def create_comment(self,agent):
        from func.req_ollama_llm import gen_com
        com=gen_com(self.news,self.content,agent)
        # Salvo id di chi pubblica il commento, il commento stesso, e il tempo in cui lo ha fatto
        if com:
            # Creazione oggetto com
            self.comments.append(Comment(self.env,self.id,agent.id,com))
            print(f'LOG "{self.env.now}" ----> COMMENT: Done-int beetween agent {agent.id}, post {self.id}, post owner {self.agent_id}')