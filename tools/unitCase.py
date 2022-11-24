from encodings.utf_8 import encode
import string
import requests as rq
from requests.auth import HTTPBasicAuth
import json
from datetime import date, timedelta, datetime
import pandas as pd

url_primary = ""
token = ""
user = ''
auth = HTTPBasicAuth(user,token)

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



tkt = 4428
while True:
    try:
        json_object = json.dumps(json.loads(item(f'SU-{tkt}')), ensure_ascii=False)# -*- coding=utf-8 -*-
        
        with open(f'./src/fileModels/test-SU-{tkt}.json', 'w') as outfile:
            outfile.write(json_object)
        break
    except:
        json_object = json.dumps(json.loads(item(f'SU-{tkt}')), ensure_ascii=True)
        with open(f'./src/fileModels/test-SU-{tkt}.json', 'w') as outfile:
            outfile.write(json_object)
        break

print(json.loads(json_object))

print('Done')
