import tweepy
from secret import *
import random
import time
import schedule


def honeypot(a=0, b=9, m=0, n=len(keys)):
    for c in range(m, n):
        auth = tweepy.OAuthHandler(keys[c]['API_Key'], keys[c]['API_Key_Secret']) #acessar a API através das chaves de cada conta honeypot
        auth.set_access_token(keys[c]['Access_Token'], keys[c]['Access_Token_Secret'])
        api = tweepy.API(auth, wait_on_rate_limit=True)

        x = random.randint(a, b) #sortear número aleatório entre 0 e 9
        print(keys[c]['User'], x)

        if 0 <= x < 4: #publica texto aleatório armazenado em uma lista
            text = open('arquivo.txt', 'r', errors="ignore") #abre o arquivo txt
            tweet = text.readlines()
            if tweet == []: #se a lista estiver vazia
                print('vazio') #retorna "vazio"
                print(api.update_status('lista de tweets vazia')) #post no Twitter de aviso que a lista está vazia
            else:
                print(api.update_status(tweet[0])) #publicar a primeira linha de texto do arquivo.txt
                del tweet[0] #excluir a primeira linha do arquivo.txt
                text = open('arquivo.txt', 'w', errors="ignore") #abrir arquivo.txt em modo de edição
                text.writelines(tweet) #salva arquivo.txt sem a primeira linha
                text.close()

        elif 4 <= x < 6:
            BRAZIL_WOE_ID = 23424768 #código do Brasil
            trends = api.get_place_trends(BRAZIL_WOE_ID) #buscar os assuntos do momento no Brasil

            topicos = list()
            for assunto in trends[0]["trends"]:
                topicos.append(assunto["name"])  #para colocar termos do assunto do momento em uma lista

            text = open('arquivo.txt', 'r', errors="ignore")  #abrir o arquivo.txt (modo leitura apenas)
            tweet = text.readlines()  #cada linha do arquivo.txt vira um elemento na lista tweet
            if tweet == []: #se o arquivo.txt estiver vazio
                #print(random.choice(topicos[:3]) + 'trend vazia')  #EXCLUIR ESSA LINHA
                print(api.update_status('lista de tweets vazia'))  #post no Twitter de aviso que a lista está vazia
            else:
                print(api.update_status(random.choice(topicos[:3]) + ' ' + tweet[0]))   #escolher 1 dos 3 primeiros tópicos presentes na lista topicos mais a primeira linha do arquivo.txt
                del tweet[0] #excluir a primeira linha do tweet.txt
                text = open('arquivo.txt', 'w', errors="ignore")  #abrir arquivo.txt em modo de edição
                text.writelines(tweet) #salva arquivo.txt sem a primeira linha
                text.close()

        elif 6 <= x < 8:
            BRAZIL_WOE_ID = 23424768
            trends = api.get_place_trends(BRAZIL_WOE_ID) #buscar os assuntos do momento no Brasil

            topicos = list()
            for assunto in trends[0]["trends"]:
                topicos.append(assunto["url"]) #pega o url de cada assunto do momento 

            print(api.update_status('Confira as tendências: ' + random.choice(topicos))) #publica o link

        elif 8 <= x < 10:
            contas = list()
            for user in keys:
                contas.append(user['User']) #cria uma lista com as contas honeypots
            contas.pop(c) #exclui da lista a conta que vai retweetar
            usuario = random.choice(contas) #escolhe uma das 3 contas na lista de forma aleatória
            tweets = api.user_timeline(screen_name=usuario, count=10) #busca os 10 últimos tweets da conta escolhida na linha 65
            ids = list() 
            for tweet in tweets:
                ids.append(tweet.id) #pegando id dos 10 tweets (cada tweet tem um id)
            retweet = random.choice(ids) #escolher aleatoriamente um tweet da lista ids
            try:
                print(api.retweet(retweet)) #retweetar
                print(api.create_favorite(retweet)) #para dar like na publicação

            except tweepy.errors.Forbidden:
                honeypot(8, 9, c, c + 1) #se tentar retweetar algo que já foi retweetado, dá erro. Tenta retweetar um novo tweet

        time.sleep(random.randint(0, 30)) #para dar intervalo de tempo entre um ciclo e outro


schedule.every(10).seconds.do(honeypot) #agendar para rodar a função honeypot a cada 10 segundos 
while True:
    schedule.run_pending()
    time.sleep(random.randint(2760, 4140)) #para ter 20 a 25 publicações diárias

