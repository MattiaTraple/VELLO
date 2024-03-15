from openai import OpenAI
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

#func dedicata alla generazioen dei post
def openia_gen_post(topic,agent,news):
    
    #scrivo bene le richeiste per openia
    sys_cont="Sei un utente di un social media che dopo aver letto della notizia "++
    user_cont
    
    request(sys_cont,user_cont)

  

    
#richiesta generica che verrà inviata a OpenIA
def request(sys_cont,user_cont):
    # Example OpenAI Python library request
    MODEL = "gpt-3.5-turbo"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            #The system message can be used to prime the assistant with different personalities or behaviors.
            #attenzione, in gpt-3.5-turbo-0301 on viene prestata tanta attenzione a system, meglio specificare tutto in user 
            {"role": "system", "content": sys_cont},
            {"role": "user", "content": user_cont},
            ],
        temperature=0,
    )
    print(response.choices[0].message.content)