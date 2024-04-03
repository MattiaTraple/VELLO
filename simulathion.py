import simpy


class Agent:
    def __init__(self, env, agent_id):
        self.env = env
        self.agent_id = agent_id
        self.friends = set()  # Lista degli amici
        self.published_content = []  # Contenuti pubblicati

    # Aggiunge un amico alla lista degli amici
    def add_friend(self, friend_id):
        self.friends.add(friend_id)

    # Pubblica un contenuto
    def publish_content(self, content):
        self.published_content.append(content)
        print(f"Agent {self.agent_id} ha pubblicato: {content}")

    # Commenta un contenuto di un amico
    def comment_content(self, friend_id, content):
        print(f"Agent {self.agent_id} ha commentato il contenuto di Agent {friend_id}: {content}")

