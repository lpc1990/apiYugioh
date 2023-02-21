import requests
from PIL import ImageTk, Image
import os


# Método que pega todas as cartas, separa por ID e nome, cria uma lista só com os nomes e a retorna
def obter_lista_id_nomes_cards():
    todas_as_cartas = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
    todas_as_cartas_json = todas_as_cartas.json()

    lista_cartas_completa = []
    lista_todas_as_cartas_nomes_ids = []

    for i, j in todas_as_cartas_json.items():
        for cada_carta in j:
            lista_cartas_completa.append({'id': cada_carta['id'], 'nome': cada_carta['name']})

    for i in lista_cartas_completa:
        for j, l in i.items():
            lista_todas_as_cartas_nomes_ids.append(i['nome'])

    return lista_todas_as_cartas_nomes_ids


def obter_lista_nome_cards():
    todas_as_cartas = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
    todas_as_cartas_json = todas_as_cartas.json()

    lista_cartas_completa = []
    lista_todas_as_cartas_nomes = []

    for i, j in todas_as_cartas_json.items():
        for cada_carta in j:
            lista_cartas_completa.append({'nome': cada_carta['name']})

    for i in lista_cartas_completa:
        lista_todas_as_cartas_nomes.append(i['nome'])

    return lista_todas_as_cartas_nomes


def obter_lista_id_nomes_cards_juntos():
    todas_as_cartas = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
    todas_as_cartas_json = todas_as_cartas.json()

    lista_cartas_completa = []
    lista_todas_as_cartas_nomes_ids_juntos = []

    for i, j in todas_as_cartas_json.items():
        for cada_carta in j:
            lista_cartas_completa.append({cada_carta['id']: cada_carta['name']})

    # for i in lista_cartas_completa:
    #     for j, l in i.items():
    #         print(j, l)
    #         lista_todas_as_cartas_nomes_ids_juntos.append(i['nome'])

    return lista_cartas_completa


# Obtém o resultado da verificação do request
def carta_result(carta_escolhida):
    numero_resposta_requisicao = carta_escolhida.status_code
    if numero_resposta_requisicao == 200:
        return "Carta recebida!"
    else:
        return "Carta não recebida!"


# Faz o donwload da imagem da carta escolhida para a pasta images, convertendo ela para PNG
def download_imagem(id):
    pasta_do_projeto = os.path.dirname(__file__)
    pasta_de_imagens = pasta_do_projeto + "\\images"
    print(pasta_de_imagens)
    url = f"https://images.ygoprodeck.com/images/cards/{id}.jpg"

    response = requests.get(url)

    with open(f"{id}.jpg", "wb") as file:
        file.write(response.content)

    img = f"{id}.jpg"
    abrir_imagem = Image.open(img)
    abrir_imagem.save(f"{pasta_de_imagens}\\{id}.png", "png")

    os.remove(img)

    redimentionar_imagem = Image.open(f"{pasta_de_imagens}\\{id}.png")
    redimentionar_imagem = redimentionar_imagem.resize((340, 496))
    redimentionar_imagem.save(f"{pasta_de_imagens}\\{id}.png")
