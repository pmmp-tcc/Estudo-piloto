import tweepy
from secret import *
import random
import time
import schedule


def honeypot(a=0, b=9, m=0, n=len(keys)):
    for c in range(m, n):
        auth = tweepy.OAuthHandler(keys[c]['API_Key'], keys[c]['API_Key_Secret'])
        auth.set_access_token(keys[c]['Access_Token'], keys[c]['Access_Token_Secret'])
        api = tweepy.API(auth, wait_on_rate_limit=True)

        x = random.randint(a, b) #sortear número aleatório entre 0 e 9
        print(keys[c]['User'], x)

        if 0 <= x < 4: #publica tweet, que é só texto
            text = open('arquivo.txt', 'r', errors="ignore") #abre o arquivo txt
            tweet = text.readlines()
            if tweet == []: #se a lista estiver vazia
                print('vazio') #dá uma lista vazia
                print(api.update_status('lista de tweets vazia')) #reabastecer a lista
            else:
                print(api.update_status(tweet[0]))
                del tweet[0]
                text = open('arquivo.txt', 'w', errors="ignore")
                text.writelines(tweet)
                text.close()

        elif 4 <= x < 6:
            BRAZIL_WOE_ID = 23424768 #código do Brasil
            trends = api.get_place_trends(BRAZIL_WOE_ID) #publica trend topics

            topicos = list()
            for assunto in trends[0]["trends"]:
                topicos.append(assunto["name"])

            text = open('arquivo.txt', 'r', errors="ignore")
            tweet = text.readlines()
            if tweet == []:
                print(random.choice(topicos[:3]) + 'trend vazia')
                print(api.update_status(random.choice(topicos[:3]) + ' ' + 'lista de tweets vazia'))
            else:
                print(api.update_status(random.choice(topicos[:3]) + ' ' + tweet[0]))
                del tweet[0]
                text = open('arquivo.txt', 'w', errors="ignore")
                text.writelines(tweet)
                text.close()

        elif 6 <= x < 8:
            BRAZIL_WOE_ID = 23424768
            trends = api.get_place_trends(BRAZIL_WOE_ID)

            topicos = list()
            for assunto in trends[0]["trends"]:
                topicos.append(assunto["url"]) #publicar links

            print(api.update_status('Confira as tendências: ' + random.choice(topicos)))

        elif 8 <= x < 10:
            contas = list()
            for user in keys:
                contas.append(user['User'])
            contas.pop(c)
            usuario = random.choice(contas)
            tweets = api.user_timeline(screen_name=usuario, count=10) 
            ids = list()
            for tweet in tweets:
                ids.append(tweet.id)
            retweet = random.choice(ids)
            try:
                print(api.retweet(retweet)) #retweetava
                print(api.create_favorite(retweet))

            except tweepy.errors.Forbidden:
                honeypot(8, 9, c, c + 1)

        time.sleep(random.randint(0, 30)) #para dar intervalo de tempo entre um ciclo e outro


schedule.every(10).seconds.do(honeypot) #agendar para rodar a função honeypot a cada 10 segundos 
while True:
    schedule.run_pending()
    time.sleep(random.randint(2760, 4140))

