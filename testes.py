import requests

headers = {
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzcyNTY2NTgxfQ.dkyJppjCTSioJCF6vb6pofkv97jf1QsjQEagWbZfPI0"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", 
             headers=headers)
print(requisicao)
print(requisicao.json())