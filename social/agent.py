import itertools
import json
import os
import random
from func.random_generator import age_gen, content_interaction_gen_prob, interest_gen, personality_activity
from func.req_openia_llm import gen_post, req_follow
from settings import config



# Classe dedicata alla generazione degli agents e alle funzioni ad essi dedicati
class Agent:
    
    id_counter = 0
    
    # Inizializzare un nuovo agents
    def __init__(self,env):
      # Permette ddi tenera a conatto con il riferimento dell'agent nella simulazione
      self.env = env  
      # Inizialmente lo uso al posto del nome
      Agent.id_counter += 1
      self.id = Agent.id_counter
      self.age=age_gen()
      self.interest=interest_gen()
      # Stapilisco il grado di attivita (float) del'agent e genero le sue personalità (dictionary), i due attributi sono correlati
      self.activity_degree,self.personality=personality_activity()
      # In base al grado, stabilisco i livello di attività dell'agents
      self.agent_activity="High" if self.activity_degree >= 0.8 else ("Medium" if self.activity_degree >= 0.2 else "Low")
      # Campo che mi dovrebbe servire per tenere traccia di ciò che ga l'agent
      self.history=[]
      # Quando decide di aggiungere qualcuno, viene rimosso poi dalla lista dei consigliati
      self.friends=[]
      self.feed=[]
      # Lista post pubblicati
      self.published=[]

    # Versione c 
    def find_friends(self,agents_candidates):   
        # Possi limitare in caso gli amici che voglio fare aggiugnere   
        # if len(self.friends)==config.NUM_FRIEND:return              
        
        ag_ca=self.order_by_degree(agents_candidates)
        for ag_id in ag_ca:
                # Questa funzione fa una richiesta a OpenIa che restituisce True/False se è interessato o meno all'amicizia
                #if(req_follow(self.age,self.interest,inner['grade'],inner['agent'].interest,inner['agent'].age)): #---> possibile implementare .selfhistory in futuro
                    # Escludi l'agente corrente e gli agenti già presenti nella lista degli amici
                    if ag_id != self.id and ag_id not in self.friends and len(self.friends) < config.NUM_FRIEND:
                        self.friends.append(ag_id)
                        print(f'LOG "{self.env.now}" ----> Agent {self.id} ha aggiunto Agent {ag_id} come amico.')
                
       


    # Fun dedicata alla creazione e generazione del post
    # News andrà a contenere una notizia sulla quale voglio fargli pubblicare il post che devo ancora decidere
    def generate_post(self):
      #datatime di generazione
        if content_interaction_gen_prob(self.activity_degree):
            # Cerco la News che fitta di più con l'agent chiamante, se non la trovo l'agent non pubblica nulla
            news=self.choosing_news()
            if news:
                #fare richiesta a API di GPT per generare post a riguardo (vengono fornite caratteristiche utente in mdoo da personalizzare in base a quelle il contenuto)
                #potrei eseguire una ristrutturazione della domanda usando i temi o qui o in unafunzione tra questa e quella in openia
                new_p=gen_post(self.env,self.id, self.interest, self.age, news)
                self.published.append(new_p)
                config.POST_DATABASE.append(new_p)
                print(f'LOG "{self.env.now}" ----> {str(self.id)} ha postato')
        
        print(f'LOG "{self.env.now}" ----> {str(self.id)} non ha postato')
        
    
    # Viene scelto un post casuale del feed e poi si sceglie se commentarlo
    def new_comment(self,agent_list):
        # Al momento non mischio l'ordine perchè teoricamente il feed viene generato basato inizialmente sugli amici che un utente ha , partendo da quello che ha grado più alto di compatibilità, quindi hanno già uno pseudo ordine di interesse peer l'utente
        #random.shuffle(self.feed)
        
        # Scelgo un post dal feed, faccio scorrere tutti i post, inizialmente solo un commento per post
        for id_post in self.feed:       
            # Identifico a quale agent il post corrisponde, da quello risalgo al post per vedere se ho già commentato
            publicant_agent=(next((agent for agent in agent_list if agent.id == int(id_post.split('-')[1].split('.')[0])), None))
            
            # Controllo i post pubblicati dall'agente finchè non trovo quello che voglio commentare
            for post in publicant_agent.published:
                if id_post==post.id :
                    # Una volta trovato verifico se non l'ho già commentato
                      if next((com for com in post.comments if com.agent ==publicant_agent.id), None) is None:
                            # Posso finalemnte commentarlo
                            self.interaction_comment(post)
                    # L'ho già commentato quindi vado a vedere se posso commentare il psot successivo
            
                
        
        
    
    # L'utente decide se e come interagire con un post e di conseguenza commenta
    def interaction_comment(self,post):
        #in base all'activity dell'utente, ogni tot tempo gli verrà posta la scelta se ccreare o meno un post su un determinato contenuto 
        #come ordino 
        
        # Decide se commentare basato su activiti dell'utente
        if content_interaction_gen_prob(self.activity_degree):
            post.create_comment(self)
        print(f'LOG "{self.env.now}" ----> MANCATA interazione: Agent {self.id} non ha interagito con {post.id}')


        
    # Fun chiamata da order_by_degree per restituire il grado di un agents
    def cal_degree_friend(self, ag_age, ag_int):
        grado = 0
        diff_eta = abs(self.age - ag_age)
        if diff_eta <= 3:
            grado += 0.5
        elif diff_eta <= 5:
            grado += 0.2
        elif diff_eta <= 10:
            grado += 0.08
        elif diff_eta <= 10:
            grado += 0.04
        
        # Calcola il grado dell'utente in base agli interessi in comune
        grado+=sum(0.5 for int1 in self.interest for int2 in ag_int if int1 == int2)
        return grado
        

    # Fun chiamata da find_friends per restituire una lista di agent ordinati per grado di coerenza
    def order_by_degree(self,ag_cd):
        agent_gr_dic={}
        # Calcola il grado di ogni utente e salvalo nel dizionario gradi_utenti
        for ag in ag_cd:
            gr = self.cal_degree_friend(ag.age,ag.interest)
            agent_gr_dic[ag.id] = {'grade': gr}
        # Versione corta    
        # agent_gr_dic = {ag_id: {'grade': self.cal_degree_friend(ag.age, ag.interest), 'agent': ag} for ag_id, ag in ag_cd.items()}
        return dict(sorted(agent_gr_dic.items(), key=lambda x: x[1]['grade'], reverse=True))
                   
            
    # Fun che verrà chiamata dopo che sono stati creati un po di post che popola (e aggiorna) periodicamente il feed dell'utente personalizzandolo in base a:

    # mod1 -> 1 post randomico per i primi 10 amici della lista di persone che segue
    def polulate_feed1(self,agent_list):
        # Se per qualche motivo il feed non è stato riempito correttamente, vado a riempirlo in modo randomico, ex uni non ha abbasatnza amici alloraa devo andare a riempirgli il feed in altro modo
            for ag in agent_list:
                if len(self.feed)==config.NUM_FEED:
                    print(f'SYM "{self.env.now}" ----> il feed dell Agent {self.id} è stato aggiornato')
                    return
                if ag.id!=self.id:    
                    #fare in modo che s enon è negli amici ma il fee non è ancora pieno, allora agigungo anche se non è amico
                    if ag.id in self.friends:
                        if ag.published:
                        # Prende un post randomico tra quelli di un amico
                            post=random.choice(ag.published)
                            if post.id is not self.feed:
                                self.feed.append(post.id)
                                print(f'LOG "{self.env.now}" ----> Il post {post.id} è stato aggiunto')                        
            # Prima provo a completare il feed solo con i post degli amici, se non è abbastanza prima provo add aggiugnere altri post degli amici
    
            self.complete_feed_f(agent_list)
            if len(self.feed)<config.NUM_FEED:
                # Se amici non bastano
                self.complete_feed_nf(agent_list)
            # Se anche i post degli altri amici non erano abbastanza vado ad attingere in modo randomico da post degli altri agent
            print(f'SYM "{self.env.now}" ----> il feed dell Agent {self.id} è stato aggiornato')

    
             
    #GLI ALTRI FEED SONO DA REVISIONARE           
    # mod2 -> 1 post più recente i primi 10 amici della lista di persone che segue
    def polulate_feed2(self,agents_dict):
        for ag in itertools.islice(agents_dict.values(), config.NUM_FEED):
            if ag.id!=self.id:
                if ag.published:
                    # Prende l'ultimo post dell'amico
                    self.feed.append(ag.published[-1])

    # mod3 -> basa la raccolta dei primi 10 post del feed basandosi sul tema post, andando in ordine 
    def polulate_feed3(self):
        count=1
        # Uso shuffle così da dare i post da analizzare per la selezioen in ordine casuale e non in ordine di creazione, do più variabilità
        for post in random.shuffle(config.POST_DATABASE):
            if count==10: break
            #solo il post non è dell'agent di cui stiamo ccreando il feed e se c'è un matching tra topic posso andare ad aggiungerlo al feed
            if post.agent_id!=self.id and set(post.topic) & set(self.interest):
                self.feed.append(post)
                count+=1         
    
# Fun ausiliaria per il completamento feed riprendendo post di agent nella lista friend
    def complete_feed_f(self,agent_list): 
            for ag in agent_list:
                if len(self.feed)==config.NUM_FEED: return
                if ag.id!=self.id:
                    #fare in modo che se non è negli amici ma il feed non è ancora pieno, allora agigungo anche se non è amico
                    if ag.id is self.friends:
                        if ag.published:
                        # Prende un post randomico tra quelli di un amico
                            post=random.choice(ag.published)
                            if post.id is not self.feed:
                                self.feed.append(post.id)
                                print(f'LOG "{self.env.now}" ----> *Completamento feed ausiliare_1* Il post {post.id} è stato aggiunto')                        

             
# Fun ausiliaria per il completamento feed in caso i post degli agent nella lista friends non basti
    def complete_feed_nf(self,agent_list):
            # Mischio l'ordine così da rendere più casuale l'agent che viene estratto
            random.shuffle(agent_list)
            for ag in agent_list:
                if len(self.feed)==config.NUM_FEED: return
                if ag.id!=self.id:
                    #fare in modo che se non è negli amici ma il feed non è ancora pieno, allora agigungo anche se non è amico
                    if ag.id is not self.friends:
                        if ag.published:
                        # Prende un post randomico tra quelli di un amico
                            post=random.choice(ag.published)
                            if post.id is not self.feed:
                                self.feed.append(post.id)
                                print(f'LOG "{self.env.now}" ----> *Completamento feed ausiliare_2* Il post {post.id} è stato aggiunto')                        


    # Fun ausiliaria per scegliere la notizia cche fitta di più in base ai temi di interesse dell'utente    
    def choosing_news(self):
        # Mischio la lista in modo da far partire da un punto random ogni agent tutte le volte (ccoprire il maggiorn numero di notizie, evitare ripetizione)
        random.shuffle(config.NEWS)
        for news_item in config.NEWS:
            for topic in news_item["topics"]:
                # Se è negli interessi dell'agent 
                
                # AL MOMENTO è COMMENTATO PERCHè DEVO ASPETTARE DI AVERE LA CATEGORIZZAZIONE DELLA NEWS, ALRIMENTI NON RIESCO A FARE IL PARING CON GLI INTERESSI DELL'UTENTE
                #if topic in self.interest:
                    return {"name":news_item["name"],"topics":topic}
                    