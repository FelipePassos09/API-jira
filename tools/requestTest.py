import requests as rq
import json

organizationId = ''
processId = ''
status = ''
accessKey = ''
url = ''
service = f''

statusCode = str()
falhas = 0

"""while (statusCode != 200):
    request = str(rq.post(url = url+service, data = accessKey))
    #response = json.dumps(json.loads(request), indent =4, sort_keys=True, separators=(",", ": "), ensure_ascii=True)
    
    statusCode = request.status_code
    falhas += 1
    
    print(request)
    break"""

lista = [ '' ]

