from dataclasses import is_dataclass
from datetime import *
from datetime import timedelta, datetime, date, tzinfo
import pandas as pd
import pytz
import os
import json
import csv

# def deltatime(data_in, data_out):
#     men = (data_in).replace('T', ' ').split('.')[0]
#     men = datetime.strptime(men, '%Y-%m-%d %H:%M:%S')
    
#     try:
#         mai = (data_out).replace('T', ' ').split('.')[0]
#         mai = datetime.strptime(mai, '%Y-%m-%d %H:%M:%S')
#     except:
#         mai=data_out
        
    
#     delta = mai - men 
    
#     return delta

# print(deltatime('2022-03-18 00:00:00',datetime.today()))

# data = pd.read_json('./output.json')
# dataSend = {}

# for key, val in data.groupby('Chave'):
#     dataSend[str(key)] = data.to_dict('records')

# print(dataSend)
    
# with open('./test-SU-2765.json') as data:
#     data = json.load(data)
        
# def quarter(dataEv):
#     dataEv = dataEv.replace('T', ' ').split('.')[0]
#     dataEv = datetime.strptime(dataEv, '%Y-%m-%d %H:%M:%S')
#     return (int(dataEv.month) -1 )//3 + 1

# dataForm = datetime.strptime((data['fields']['created'].replace('T', ' ').split('.')[0]), '%Y-%m-%d %H:%M:%S')

# print(quarter(data['fields']['created']))

#print(str(date.today() - timedelta(days=1)))

# def reaberto(item):
#     listaReabertos = pd.read_csv('./reabertos.csv')
#     listaReabertos = pd.DataFrame(listaReabertos)
   
#     if data['fields']['customfield_10010']['currentStatus']['status'] == 'Reaberto':
#         item = {'Chave': item}
#         listaReabertos = listaReabertos.append(item, ignore_index = True)
#         listaReabertos.to_csv('./reabertos.csv', index=False)
#         return 'Sim'
#     else:
#         if item in list(listaReabertos['Chave']):
#             return 'Sim'
#         else:
#             return 'Não'

# listaReabertos = pd.read_csv('./reabertos.csv')
# listaReabertos = pd.DataFrame(listaReabertos)
        
# print(reaberto('SU-2765'))

# errors = []

# for i in range(1,200,1):
#     errors.append(f'SU-{i}')

# with open('./logTest.txt','w') as log:
#     log.write(f'Chaves não carregadas {errors}\n\n{str(datetime.now())}')
    
# log.close()

with open('C:\API Jira\src\\fileModels\\test-SU-2500.json') as data:
    data = json.load(data)

print(data['fields']['customfield_10050'])
k = 'fields'

def timeSpent():
    if data[k]['timespent'] != None:
        return float(f"{(data[k]['timespent'] /60):.2f}")
    else:
        return 0

    
# Validar retorno do timestamp se condiz com chamado
print(timeSpent())

