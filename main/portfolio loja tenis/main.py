import requests
from bs4 import BeautifulSoup
import pandas as pd

# Definindo a URL e os cabeçalhos
url_adidas = 'https://www.spacetennis.com.br/categoria/adidas/'
url_asics = 'https://www.spacetennis.com.br/categoria/asics/'
url_mizuno = 'https://www.spacetennis.com.br/categoria/mizuno/'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}
produtos_lista = []
precos_lista = []


def obter_dados(url):
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_='product-item-body text-center')
    produtos_lista = []
    precos_lista = []
    next_link = soup.find('a', class_='next')
    if next_link:
        next_href = next_link['href']
        next_href_formatado = next_href[6:]
        numero_paginas_inteiro = int(next_href_formatado[0])
        
        for i in range(1,numero_paginas_inteiro+10):
            url_pag = f'{url}?page={i}'
            print(url_pag)
            site = requests.get(url_pag, headers=headers)
            soup = BeautifulSoup(site.content, 'html.parser')
            produtos = soup.find_all('div', class_='product-item-body text-center')
            for produto in produtos:
                nome_produto = produto.find('a', class_='w-100 float-left link-name').get_text().strip()
                produtos_lista.append(nome_produto)
                
                preco = produto.find('span', class_='product-detail--pix').get_text().strip()
                preco_formatado = preco[:-15]  
                precos_lista.append(preco_formatado)
    else:
        for produto in produtos:
            nome_produto = produto.find('a', class_='w-100 float-left link-name').get_text().strip()              
            produtos_lista.append(nome_produto)
            
            preco = produto.find('span', class_='product-detail--pix').get_text().strip()
            preco_formatado = preco[:-15] 
            precos_lista.append(preco_formatado)
    return produtos_lista, precos_lista

produtos_adidas, precos_adidas = obter_dados(url_adidas)
produtos_asics, precos_asics = obter_dados(url_asics)
produtos_mizuno, precos_mizuno = obter_dados(url_mizuno)


produtos_lista = produtos_adidas + produtos_asics + produtos_mizuno
precos_lista = precos_adidas + precos_asics + precos_mizuno

# Criando DataFrame
dados = {'Produto': produtos_lista, 'Preço': precos_lista}
df = pd.DataFrame(dados)
print(df)
# Exibindo o DataFrame

df.to_excel('produtos.xlsx', index=False)
