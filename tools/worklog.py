from encodings.utf_8 import encode
import requests as rq
from requests.auth import HTTPBasicAuth
import json
from datetime import date, timedelta, datetime
import pandas as pd


# base variables:

url_primary = ""
token = ""
user = ''
auth = HTTPBasicAuth(user,token)

output_jsonFilename = './worklogOutput.json'

# Jira functions:

def getWorklog(issueIdOrKey = str):
    """Returns an JSON that contains all the worklogs of an issue.

    Args:
        issueIdOrKey (string, optional): string with the key or id of an Jira issue . Defaults to str.

    Returns:
        json: json with contains the worklog.
    """
    
    method = f'issue/{issueIdOrKey}/worklog'
    

    headers = {
    "Accept": "application/json"
    }

    response = rq.request(
    "GET",
    url_primary+method,
    headers=headers,
    auth=auth
    )

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)


def getJql(func = str):
    """Returns an JSON object with the worklog data by jql function.

    Args:
        func (string, mandatory): an string with JQL query. Defaults to str.

    Returns:
        JSON: an json object with the worklog data.
    """
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

def getComment(obj):
    """Get the comment of the worklog by the json path.

    Args:
        obj (json_path): an path json of the issue loop.

    Returns:
        string: return the comment as a string or None.
    """
    
    # if obj['comment'] == None:
    #     return None
    # else:
    #     return obj['comment']['content'][0]['content'][0]['text']
    
    for key, value in obj.items():
        if key == 'comment':
            return obj['comment']['content'][0]['content'][0]['text']
        else:
            return None


# list issues:

query = (f'project = SU and updated >= {str(date.today() - timedelta(days=1))}')

data = json.loads(getJql(query))
lista_casos = []

for k, v in data.items():
    if k == 'issues':
        for i in v:
            lista_casos.append(i['key'])


data = []

for i in lista_casos:
    worklog = json.loads(getWorklog(i))
    for note in worklog['worklogs']:
        print(i)
        data.append({
            'issue': i,
            'date': note['created'],
            'comment': getComment(note),
            'author': note['author']['displayName'],
            'timeSpent': (note['timeSpentSeconds'] /60)/60
        })
        
        


output = {
    "Data": data
}

print(output)

with open(output_jsonFilename, 'w', encoding='UTF-8') as outfile:
    json.dump(json.loads(output), fp=outfile, ensure_ascii=False)