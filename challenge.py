# Bibliotecas que nós instalamos manualmente
from bs4 import BeautifulSoup
# Bibliotecas nativas do Python
import json
import requests
# URL do site
url = 'https://infosimples.com/vagas/desafio/commercia/product.html'
# Objeto contendo a resposta final
resposta_final = {}
# Faz o request
response = requests.get(url)
# Parse do responses
parsed_html = BeautifulSoup(response.content, 'html.parser')
# Vamos pegar o título do produto, na tag H2, com ID "product_title"
resposta_final['title'] = parsed_html.select_one('h2#product_title').get_text()
# Vamos pegar a marca do produto, na tag H2, com class "brand"
resposta_final['brand'] = parsed_html.select_one("div[class='brand']").get_text()
# Vamos pegar as categorias do produto, na tag nav, com class "current-category"
categories = parsed_html.select_one("nav[class='current-category']").get_text(separator=' ').replace("\n","")
# Depois dividir ela em um array com o separador " > " e retirar espaços vazios de cada string
categories = [item.strip() for item in categories.split(" > ")]
resposta_final['categories'] = categories

# Vamos pegar a descrição do produto, na tag h4, e procurar em todos os vizinhos com a tag p
descriptions= parsed_html.select_one("h4").find_next_siblings('p')
description = ""
# Depois juntamos os dois textos que estão separados no html
for text in descriptions:
    description += text.get_text().strip()
resposta_final['description'] = description

# Vamos pegar as caracteristicas de cada variação do produto, que estão na tag div com a class card
skus = parsed_html.find_all('div', class_='card')
object = []
# Iteramos para cada variação
for sku in skus:    
    # Pegamos o nome
    name = sku.select_one('div[class="prod-nome"]').get_text()
    # Pegamos o preço atual se houver. Caso contrário, None é adicionado
    current_price = sku.select_one('div[class="prod-pnow"]')
    if current_price != None:
        current_price = current_price.get_text()
    # Pegamos o preço antigo se houver. Caso contrário, None é adicionado
    previous_price = sku.select_one('div[class="prod-pold"]')
    if previous_price != None:
        previous_price = previous_price.get_text()
    # Verificamos a disponibilidade do produto: se possue preço atual, o produto está disponível. Caso contrário, ele está indisponível
    available = True
    if current_price == None:
        available = False
    # O objeto inteiro é criado com cada característica da variação
    object.append({'name': name, 'current_price': current_price, 'previous_price': previous_price, 'available': available})
resposta_final['skus'] = object

# Vamos pegar as propriedades do produto, que estão com a tag tr
properties = parsed_html.find_all('tr')
object = []
# Iteramos para cada propriedade
for property in properties:
    # Pegamos o título da propriedade
    label = property.select_one('b')
    if label != None:
        label = label.get_text()
    # Pegamos o valor da propriedade
    value = property.find_all('td')
    if value != []:
        value = value[1].get_text()
    # O objeto inteiro é criado com cada título e valor
    if label != None and value != []:
        object.append({'label': label, 'value': value})
resposta_final['properties'] = object

# Vamos pegar as avaliações do produto, que estão na tag div com a class card
reviews = parsed_html.find_all('div', class_='analisebox')
object = []
# Iteramos para cada avaliação
for review in reviews:
    # Pegamos o nome
    name = review.select_one('span[class="analiseusername"]').get_text()
    # Pegamos a data
    date = review.select_one('span[class="analisedate"]').get_text()
    # Pegamos quantas estrelas, de 1 a 5, foram dadas para avaliação
    score = review.select_one('span[class="analisestars"]').get_text()
    # Pegamos o texto deixado pelo avaliador
    text = review.select_one('p').get_text()
    # O objeto inteiro é criado com cada característica da avaliação
    object.append({'name': name, 'date': date, 'score': score, 'text': text})
resposta_final['reviews'] = object

# Vamos pegar a média das avaliações do produto, na tag h3, na tag h4
resposta_final['reviews_average_score'] = parsed_html.select_one('h3').find_next().get_text().replace("Average score: ","")
# Vamos pegar a url da página do produto que já é fornecida no início do código
resposta_final['url'] = url

# Salva o arquivo JSON com a resposta final
with open('produto.json', 'w') as arquivo_json:
# Adicionei alguns parâmetros a mais para que o arquivo json fique mais legível
    json.dump(resposta_final, arquivo_json, indent=4, ensure_ascii=False)
