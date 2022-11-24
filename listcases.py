import string
import requests as rq
from requests.auth import HTTPBasicAuth
import json
from datetime import date, timedelta, datetime
import pandas as pd
import pytz
import calendar



url_primary = "https://upfluxpm.atlassian.net/rest/api/3/"
token = "1HIoLIKNtvxh7huivj3S59CB"
user = 'felipep@upflux.net'
auth = HTTPBasicAuth(user,token)

def Ids():
    list_ids = []
    for i in range(1, 50, 1):
        list_ids.append(i)
    
    return list_ids


def issues():
    url_extension = 'jql/match'
    
    url = url_primary + url_extension
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"    
    }

    payload = json.dumps({
        "issueIds": Ids(),
        "jqls":[
            "project = SU"
            
        ]
    })

    response = rq.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
        )

    return print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",",": ")))


def list_events():
    url_extension = 'events'
        
    url = url_primary + url_extension

    headers = {
    "Accept": "application/json"
    }

    response = rq.request(
    "GET",
    url,
    headers=headers,
    auth=auth
    )

    result = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    
    for i in result:
        print(i)
    

def transitions(item=string):
    url_extension = f'issue/{item}/transitions'
    url = url_primary + url_extension
    
    headers = {
    "Accept": "application/json"
    }

    response = rq.request(
    "GET",
    url,
    headers=headers,
    auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


def item(item=string):
    url_extension = f'issue/{item}'
    url = url_primary + url_extension

    headers = {
   "Accept": "application/json"
    }

    response = rq.request(
    "GET",
    url,
    headers=headers,
    auth=auth
    )

    while True:
        try:
            return json.dumps(json.loads(response.text), indent=4, sort_keys=True, separators=(",", ": "))
            break
        except:
            return json.dumps(json.loads(response.text), indent=4, sort_keys=True, separators=(",", ": "))
            break



def jqls(func=string):
    url_extension = f'search'
    url = url_primary + url_extension
    
    headers = {
                "Accept": "application/json"
        }

    query = {
            'jql': func
        }

    response = rq.request(
            "GET",
            url,
            headers=headers,
            params=query,
            auth=auth
    )

    return json.dumps(json.loads(response.text), indent=4, sort_keys=True, separators=(",", ": "), ensure_ascii=False)

#set dataframe:
dataset = {
    'Id': [],
    'Status': [],
    'Relator': [],
    'Data Criação': [],
    'Resumo': []
}

df_data = pd.DataFrame(dataset)

# extraindo casos para navegação lista de casos:
tkt = (f'project = SU and updated > 2022-05-10')
filename = 1

"""try:
    json_object = json.dumps(json.loads(jqls(tkt)), ensure_ascii=False)
    with open(f'./test-JQL-{filename}.json', 'w') as outfile:
        outfile.write(json_object)
except:
    json_object = json.dumps(json.loads(jqls(tkt)), ensure_ascii=True)
    with open(f'./test-JQL-{filename}.json', 'w') as outfile:
        outfile.write(json_object)"""



data = json.loads(jqls(tkt))
lista_casos = []

for k, v in data.items():
    if k == 'issues':
        for i in v:
            lista_casos.append(i['key'])

print(lista_casos)