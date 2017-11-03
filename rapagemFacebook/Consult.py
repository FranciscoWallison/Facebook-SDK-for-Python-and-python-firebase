import facebook
import requests
import json
from collections import namedtuple

# connect banco
from firebase import firebase
firebase = firebase.FirebaseApplication('https://you_domin.firebaseio.com/')

# config facebookAPI
access_token ="you_token"
graph = facebook.GraphAPI(access_token)


pergunta = 'Hospital' # pesquisa por paginas com esse nome
directFile = 'pesquisas/'+pergunta+'.json'


arquivo = open(directFile, 'r')
unica_string = arquivo.read()
arquivo.close()

# transformando em OBJETO
x = json.loads(unica_string, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

id_consult = []
# atribuindo valres
for place  in x.Hospital.data:
    id_consult.append( str(place.id)  )

result_all_feeds = [] 

for event in id_consult:
    feeds = graph.get_connections(event,
    connection_name="feed",
    fields="message,name,comments,created_time")
    result_all_feeds.append( feeds['data'] )


directFile_result = 'pesquisas/result_all_feeds'+pergunta+'.json'
directDB = pergunta+'result_all'


with open( directFile_result, 'w') as fp:
    json.dump(result_all_feeds, fp)

# Firebase
firebase.post(directDB, result_all_feeds)

print ( 'ok...')