from ast import Pass
import string
import requests as rq
from requests.auth import HTTPBasicAuth
import json
from datetime import date, timedelta, datetime
import pandas as pd
import zipfile
import csv


# Jira requests:

url_primary = ""
token = ""
user = ''
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

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",",": "))


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

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    

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

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))


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


# Data transform functions:

def tempogasto():
    
    tempogasto = []
    
    if len(data[k]['worklog']['worklogs']) != 0:
        for n in data[k]['worklog']['worklogs'][0]['timeSpent'].split(' '):
            if 'd' in n:
                tempogasto.append(int(n.replace('d', ''))*(60*24))
            elif 'h' in n:
                tempogasto.append(int(n.replace('h', ''))*60)
            elif 'm' in n:
                tempogasto.append(int(n.replace('m', '')))
                
        return sum(tempogasto)
    
    else:
        return 'Aberto'        
                

def timeSpent():
    if data[k]['timespent'] != None:
        return float(f"{(data[k]['timespent'] / 60):.2f}")
    else:
        return 0

    

def dataresolucao():
    if data[k]['resolutiondate'] != None:
        return data[k]['resolutiondate'].split('T')[0]
    else:
        return 'Aberto'
     

def temporesolucao(customfield):
    try:
        if data[k][customfield]['ongoingCycle'] != None or len(data[k][customfield]['ongoingCycle']) != 0:
            breachTime = data[k][customfield]['ongoingCycle']['breachTime']['iso8601'].replace('T', ' ').split('-0300')[0]
            breachTime = datetime.strptime(breachTime, '%Y-%m-%d %H:%M:%S')
            today = datetime.today()
            amount = (breachTime - today)
            
            if data[k][customfield]['ongoingCycle']['breached'] == False:
                return str(amount)
            elif data[k][customfield]['ongoingCycle']['breached'] == True:
                return 'Violado'
            else:
                return None
            
        else:
            return None
    except:
        if data[k][customfield]['completedCycles'] != None and len(data[k][customfield]['completedCycles']) != 0:
            breachTime = data['fields'][customfield]['completedCycles'][0]['breachTime']['iso8601'].replace('T', ' ').split('-0300')[0]
            breachTime = datetime.strptime(breachTime, '%Y-%m-%d %H:%M:%S')
            today = datetime.today()
            amount = (breachTime - today)
            
            if data[k][customfield]['completedCycles'][0]['breached'] == False:
                return str(amount)
            elif data[k][customfield]['completedCycles'][0]['breached'] == True:
                return 'Violado'
            else:
                return None
        else:
            return None
        

def deltatime(data_in, data_out):
    men = (data_in).replace('T', ' ').split('.')[0]
    men = datetime.strptime(men, '%Y-%m-%d %H:%M:%S')
    
    try:
        mai = (data_out).replace('T', ' ').split('.')[0]
        mai = datetime.strptime(mai, '%Y-%m-%d %H:%M:%S')
    except:
        mai=data_out
        
    
    delta = mai - men 
    delta = delta.total_seconds() / (60*60)
    
    return float(f'{delta:.2}')


def resolutiondate():
    if data[k]['resolutiondate'] != None:
        return deltatime(data[k]['created'],data[k]['resolutiondate'])
    else:
        return deltatime(data[k]['created'],datetime.today())


def frdate():
    if len(data[k]['customfield_10051']['completedCycles']) != 0:
        return deltatime(data[k]['created'],data[k]['customfield_10051']['completedCycles'][0]['stopTime']['jira'])
    else:
        return deltatime(data[k]['created'],datetime.today())


def criticidade():
    if data[k]['customfield_10099'] != None:
        return data[k]['customfield_10099']['value']
    else:
        return 'Não categorizado'

    
def prioridade():
    if data[k]['priority'] != None:
        return data[k]['priority']['name']
    else:
        return 'Não categorizado'
    

def sintoma():
    if data[k]['customfield_10167'] != None:
        return data[k]['customfield_10167']['value']
    else:
        return 'Não categorizado'
    

def resolucao():
    if data[k]['customfield_10168'] != None:
        return data[k]['customfield_10168']['value']
    else:
        return 'Não categorizado'
    
    
def versao_do_App():
    if data[k]['customfield_10164'] != None:
        return data[k]['customfield_10164'][0]['value']
    else:
        return 'Não categorizado'


def melhoria():
    if data[k]['customfield_10180'] != None:
        return data[k]['customfield_10180']['value']
    else:
        return 'Não categorizado'

def squad():
    if data[k]['customfield_10178'] != None:
        return data[k]['customfield_10178']['value']
    else:
        return 'Não categorizado'    
    
def recorrente(): 
    if data[k]['customfield_10166'] != None:
        return data[k]['customfield_10166']['value']
    else:
        return 'Não categorizado'
    

def satisfaction(): 
    if data[k]['votes'] != None:
        return data[k]['votes']['votes']
    else:
        return 'Não categorizado'


def sla_breached(customfield):
    try:           
        if len(data[k][customfield]['completedCycles']) != 0:
            if data[k][customfield]['completedCycles'][0]['breached'] == False:
                return 'Aderido'
            if data[k][customfield]['completedCycles'][0]['breached'] == True:
                return 'Violado'           
        if data[k][customfield]['ongoingCycle'] != None:
            if data[k][customfield]['ongoingCycle']['breached'] == False:
                return 'Aderido'
            if data[k][customfield]['ongoingCycle']['breached'] == True:
                return 'Violado'
    except:
        return 'Não Navegado/Melhoria'


def responsavel():
    if data[k]['assignee'] != None:
        return data[k]['assignee']['displayName']
    
    else:
        return 'Não Classificado'


def nome_cliente():
    if data[k]['customfield_10127'] != None:
        return data[k]['customfield_10127']['value']
    else:
        return 'Não Aplicado'


def satisfaction():
    if data[k]['customfield_10030'] != None:
        return data[k]['customfield_10030']['rating']
    else:
        return 'Não Avaliado'


def dsemana():
    dia = datetime.strptime((data[k]['created'].replace('T',' ').split('.')[0]), '%Y-%m-%d %H:%M:%S').weekday()
    
    if dia == 1:
        return 'Domingo'
    if dia == 2:
        return 'Segunda'
    if dia == 3:
        return 'Terça'
    if dia == 4:
        return 'Quarta'
    if dia == 5:
        return 'Quinta'
    if dia == 6:
        return 'Sexta'
    if dia == 7:
        return 'Sábado'

    
def quarter(dataEv):
    dataEv = dataEv.replace('T', ' ').split('.')[0]
    dataEv = datetime.strptime(dataEv, '%Y-%m-%d %H:%M:%S')
    return (int(dataEv.month) -1 )//3 + 1
    

def quinzena(dataEv):
    dataEv = dataEv.replace('T', ' ').split('.')[0]
    dataEv = datetime.strptime(dataEv, '%Y-%m-%d %H:%M:%S')
    
    if dataEv.day <= 15:
        return 1
    elif dataEv.day > 15:
        return 2


def categoria():
    if data[k]['customfield_10010'] != None:
        return data[k]['customfield_10010']['requestType']['name']
    else:
        return 'Não Classificado'

def classificacao():
    if data[k]['customfield_10145'] != None:
        return data[k]['customfield_10145']['value']
    else:
        return 'Não Classificado'
    

#reopen task control:

def reaberto(item):
    listaReabertos = pd.read_csv('./reabertos.csv')
    listaReabertos = pd.DataFrame(listaReabertos)
    
    try:
        if data[k]['customfield_10010']['currentStatus']['status'] == 'Reaberto':
            item = {'Chave': item}
            listaReabertos = listaReabertos.append(item, ignore_index = True)
            listaReabertos.to_csv('./reabertos.csv', index=False)
            return 'Sim'
        else:
            if item in list(listaReabertos['Chave']):
                return 'Sim'
            else:
                return 'Não'
    except:
        return 'Não'



#set dataframe:
dataset = {
        'IdJira': [],
        'Status': [],
        'Relator': [],
        'Data Criação': [],
        'Resumo': []
    }

df_data = pd.DataFrame(dataset)


#set searching:
query = (f'project = SU and updated >= {str(date.today() - timedelta(days=1))}')

## 
# createdDate >= {datetime.today() - timedelta(days=1)}
##

data = json.loads(jqls(query))
lista_casos = []

for k, v in data.items():
    if k == 'issues':
        for i in v:
            lista_casos.append(i['key'])

issue = lista_casos

print(issue)

#consulta por range:

issue = []

for i in range(1271, 4000, 1):
    issue.append(f'SU-{i}')

print(issue)
errors = []

#set dataframe compiling:
for i in issue:
    data = json.loads(item(i))

    for k,v in data.items():
        if k == 'fields':
            try:
                newrow = {
                    'Chave':str(i),
                    'IdJira':data['id']+'-'+data[k]['updated'],
                    'Status': data[k]['customfield_10010']['currentStatus']['status'],
                    'Relator': data[k]['creator']['displayName'],
                    'Resumo': data[k]['summary'], #.replace('\u00e7','ç')
                    'Categoria': categoria(),
                    'Tipo de Item': data[k]['issuetype']['name'],
                    'Classificação': classificacao(), #criar checagem de valor nulo.
                    'Sintoma': sintoma(),
                    'Resolução': resolucao(),
                    'Versão do App': versao_do_App(),
                    'Recorrente': recorrente(),
                    'Criticidade': criticidade(),
                    'Prioridade': prioridade(),
                    'SLA Cumprido(1ª Resposta)': sla_breached('customfield_10051'),
                    'SLA Cumprido(Resolução)': sla_breached('customfield_10050'),
                    'Reaberto': reaberto(i),
                    'Satisfação': satisfaction(),
                    'Data Criação': data[k]['created'].split('T')[0],
                    'Data Resolução': dataresolucao(),
                    'Data Alteração': data[k]['statuscategorychangedate'].split('T')[0],
                    'Tempo Gasto': timeSpent(), # ajustar para calcular a partir do timeSpent, em segundos.
                    'Tempo de Resolução': resolutiondate(),
                    'Tempo 1ª Resposta': frdate(),
                    'Tempo Restante': temporesolucao('customfield_10050'),
                    'Nome cliente': nome_cliente(),
                    'Responsável': responsavel(),
                    'Dia/Semana': str((datetime.strptime((data[k]['created'].replace('T',' ').split('.')[0]), '%Y-%m-%d %H:%M:%S')).strftime('%A')),
                    'Dia/Mês': str((datetime.strptime((data[k]['created'].replace('T',' ').split('.')[0]), '%Y-%m-%d %H:%M:%S')).strftime('%d')),
                    'Quinzena': quinzena(data[k]['created']),
                    'Mês': str((datetime.strptime((data[k]['created'].replace('T',' ').split('.')[0]), '%Y-%m-%d %H:%M:%S')).strftime('%B')),
                    'Ano': str((datetime.strptime((data[k]['created'].replace('T',' ').split('.')[0]), '%Y-%m-%d %H:%M:%S')).strftime('%Y')),
                    'Squad': squad(),
                    'Melhoria': melhoria(),
                    'Quarter': quarter(data[k]['created'])
                }
                df_data = df_data.append(newrow, ignore_index=True)
            except:
                try:
                    newrow = {
                    'Chave':str(i),
                    'IdJira':data['id']+'-'+data[k]['updated'],
                    'Status': 'Pendente',
                    'Relator': data[k]['creator']['displayName'],
                    'Resumo': data[k]['summary'].replace('\u00e7','ç'),
                    'Categoria': categoria(),
                    'Tipo de Item': data[k]['issuetype']['name'],
                    'Classificação': classificacao(),
                    'Sintoma': 'Não Categorizado',
                    'Resolução': 'Não Categorizado',
                    'Versão do App': 'Não Categorizado',
                    'Recorrente': recorrente(),
                    'Criticidade': criticidade(),
                    'Prioridade': prioridade(),
                    'SLA Cumprido(1ª Resposta)': sla_breached('customfield_10051'),
                    'SLA Cumprido(Resolução)': sla_breached('customfield_10050'),
                    'Reaberto': reaberto(i),
                    'Satisfação': satisfaction(),
                    'Data Criação': data[k]['created'].split('T')[0],
                    'Data Resolução': dataresolucao(),
                    'Data Alteração': data[k]['statuscategorychangedate'].split('T')[0],
                    'Tempo Gasto': timeSpent(),
                    'Tempo de Resolução': resolutiondate(),
                    'Tempo 1ª Resposta': frdate(),
                    'Tempo Restante': temporesolucao('customfield_10050'),
                    'Nome cliente': nome_cliente(),
                    'Responsável': responsavel(),
                    'Dia/Semana': datetime.strptime((data[k]['created'].replace('T',' ').split('.')[0]), '%Y-%m-%d %H:%M:%S').weekday(),
                    'Dia/Mês': str((datetime.strptime((data[k]['created'].replace('T',' ').split('.')[0]), '%Y-%m-%d %H:%M:%S')).strftime('%d')),
                    'Quinzena': quinzena(data[k]['created']),
                    'Mês': str((datetime.strptime((data[k]['created'].replace('T',' ').split('.')[0]), '%Y-%m-%d %H:%M:%S')).strftime('%B')),
                    'Ano': str((datetime.strptime((data[k]['created'].replace('T',' ').split('.')[0]), '%Y-%m-%d %H:%M:%S')).strftime('%Y')),
                    'Squad': squad(),
                    'Melhoria': melhoria(),
                    'Quarter': quarter(data[k]['created'])
                }
                    df_data = df_data.append(newrow, ignore_index=True)
                except:
                    errors.append(i)
                    Pass
                
            print(i)
        
        
#output:
filename_json = f'./output.json'
filename_csv = f'./output.csv'

df_data.to_json(filename_json, force_ascii=False)
df_data.to_csv(filename_csv, index = False, sep=';', encoding='utf-8')
df_data = pd.DataFrame(df_data)


#dfDataAgrupado = df_data.groupby('Chave', sort = False).to_dict('r')
dfDataAgrupado = df_data
data = {}

for key, val in dfDataAgrupado.groupby('Chave'):
    data["eventLog"] = dfDataAgrupado.to_dict('records')

with open(filename_json, 'w', encoding='utf-8') as outfile:
    json.dump(data, fp= outfile, ensure_ascii=False)
    
outfile.close()

# Packaging log to .zip:
dfDataAgrupado.to_json('./exit.json', force_ascii=False, orient = 'records')
zip = zipfile.ZipFile('zoutput.zip', 'w', zipfile.ZIP_DEFLATED)
zip.write(filename_json)
zip.close()

#Requisition compile:
"""
groupId = ''
clientId = ''
url_Base = ''
service = f''
accessKey = ''


payload = {}

files = [('eventLog',('file', open('./zoutput.zip', 'rb'), 
         'application/octet-stream'))
         ]

headers = {
    'groupId': groupId,
    'Accept': 'application/json',
    'Authorization': accessKey
}

requisicao = rq.request('POST', url = url_Base+service, headers = headers, files = files)"""


with open('./log.txt','w') as log:
    log.write(f'{errors}\n\n{str(datetime.now())}')
    
log.close()

