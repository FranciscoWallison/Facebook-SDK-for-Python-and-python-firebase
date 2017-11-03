import facebook
import requests
import json

# connect banco
from firebase import firebase
firebase = firebase.FirebaseApplication('https://you_domin.firebaseio.com/')

# config facebookAPI
access_token ="you_token"
graph = facebook.GraphAPI(access_token)

# Variaveis
pergunta = 'Hospital' # pesquisa por paginas com esse nome
lgMapa = '-3.731862, -38.526669' # localização 


pages = graph.search(type='place',
	q=pergunta,
	center=lgMapa,
    fields="message,name,comments,created_time,location")

while(True):
     try:
        for page in pages['data']:
                print(page)
        # Tente fazer requisição se a proxima pagina existir
        pages=requests.get(pages['paging']['next']).json()
        
     except KeyError:
        # Quando não existir mais paginas (['paging']['next']), quebre o loop
        # fim de loop
        break

filteReturn = pages['data']

# Armazenando as informações
# Em arquivo
directFile = 'pesquisas/'+pergunta+'.json'
directDB = '/'+pergunta

with open( directFile, 'w') as fp:
    json.dump(filteReturn, fp)
# Firebase
firebase.post(directDB, filteReturn)

print ( 'ok...')

