import requests
import json

res = requests.get('http://127.0.0.1:8000/api/postlist/')
j = json.loads(res.content)
for i in j:
    print(i['title'])


