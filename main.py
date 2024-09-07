from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timezone
import json
import os
import schedule
import time

url = 'https://coinmarketcap.com/currencies/dogecoin/'

def run_scraper():
    print('running')
    data = []

    # Carregar preços existentes
    if os.path.exists('dogecoin_prices.json'):
        with open('dogecoin_prices.json') as f:
            data = json.load(f)

    # Fazer a requisição com cabeçalho de user-agent
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code != 200:
        print("Erro ao acessar a página:", response.status_code)
        return

    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    # Procurar o elemento que contém o preço
    regex = re.compile('.*priceValue.*')
    price_tag = soup.find('div', {'class':"sc-65e7f566-0 DDohe flexStart alignBaseline"})

    # Verificar se o preço foi encontrado
    if price_tag is None:
        print("Preço não encontrado na página.")
        return

    current_price = price_tag.text.strip()
    print(current_price)

    # Obter o horário atual em UTC
    dt = datetime.now(timezone.utc)
    utc_timestamp = dt.timestamp()

    # Preparar o objeto JSON
    export_object = {
        'time': utc_timestamp,
        'price': current_price
    }
    print(export_object)

    data.append(export_object)

    # Salvar os dados no arquivo JSON
    with open('dogecoin_prices.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

schedule.every(60).seconds.do(run_scraper)  # Aumente o intervalo para 60 segundos

# Executar o agendador
while True:
    schedule.run_pending()
    time.sleep(1)
