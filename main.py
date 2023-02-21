import tkinter
from tkinter import *
from tkinter import ttk
import requests
import os
import pygame
from todos_metodos import obter_lista_id_nomes_cards, obter_lista_nome_cards, \
    obter_lista_id_nomes_cards_juntos, download_imagem, carta_result

pasta_do_projeto = os.path.dirname(__file__)
pasta_de_imagens = pasta_do_projeto + "\\images"
pasta_de_links = pasta_do_projeto + "\\links"


# Função executada ao fechar a janela, que apaga as imagens usadas e fecha a janela
def fechando_janela():
    pasta_do_projeto = os.path.dirname(__file__)
    pasta_de_imagens = pasta_do_projeto + "\\images"

    for file_name in os.listdir(pasta_de_imagens):
        os.remove(os.path.join(pasta_de_imagens, file_name))

    janela.destroy()


# Roda a função que gera a lista com o nome de todas as cartas e outra função que obtém o nome e id de todas elas
lista_nome_cards = obter_lista_nome_cards()
lista_id_nome_cards = obter_lista_id_nomes_cards()
lista_id_nome_cards_juntos = obter_lista_id_nomes_cards_juntos()

# Variável que quantifica as cartas na API
quantas_cartas_na_colecao = len(lista_nome_cards)

# início configurações do TKinter
janela = Tk()
janela.protocol("WM_DELETE_WINDOW", fechando_janela)
janela.resizable(False, False)
janela.title("*** Pokedéx Yugioh ***")
janela.config(background="blue")
janela.iconbitmap("./images_programa/enigma.ico")

img_fundo = PhotoImage(file="images_programa\\fundo_pronto.png")
label_fundo = Label(janela, image=img_fundo)
label_fundo.pack()

# Cálculo para a definição do centro da tela, para o aparecimento ideal da janela do programa
largura = 1080
altura = 720

largura_screen = janela.winfo_screenwidth()
altura_screen = janela.winfo_screenheight()

posx = ((largura_screen / 2) - (largura / 2))
posy = ((altura_screen / 2) - (altura / 2))

janela.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))


# Iniciando a música junto com o programa
pygame.mixer.init()
musica = pygame.mixer.Channel(7)
som = pygame.mixer.Sound("./sounds/yugioh_fb_music.mp3")

musica.play(som, loops=10)
musica.set_volume(0.5)



# Define o evento para a pesquisa da carta no combobox
def search(event):
    value = event.widget.get()

    if value == '':
        cb_cartas['values'] = lista_nome_cards
    else:
        data = []
        for item in lista_nome_cards:
            if value.lower() in item.lower():
                data.append(item)
        cb_cartas['values'] = data


# Função principal que faz a requisição da carta pelo ID, verifica o retorno, organiza e desempacota os informações
def request_card_escolhido(carta):
    # Nome da carta e linguagem desejada
    carta_pesquisada = str(carta)
    linguagem_da_carta = "pt"

    # Cria o link com as instruções  e faz o request com o link solicitado
    # https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Mago%20Negro&language=pt
    link_pronto = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={carta_pesquisada}"
    carta_escolhida = requests.get(link_pronto)

    # Verifica se obteve retorno ok (200), ou não obteve retorno ok (400)
    ok_ou_nao = carta_result(carta_escolhida)
    print(ok_ou_nao)

    # Converte o resultado do tipo result para o tipo json (dicionário)
    carta_escolhida_json = carta_escolhida.json()

    global card_id1
    card_id1 = carta_escolhida_json['data'][0]["id"]

    global card_name1
    card_name1 = carta_escolhida_json['data'][0]["name"]

    try:
        global card_type1
        card_type1 = carta_escolhida_json['data'][0]["type"]
    except KeyError as erroType:
        card_type1 = "--"

    try:
        global card_frametype1
        card_frametype1 = carta_escolhida_json['data'][0]["frameType"]
    except KeyError as erroFrameType:
        card_frametype1 = "--"

    try:
        global card_desc1
        card_desc1 = carta_escolhida_json['data'][0]["desc"]
    except KeyError as erroDesc:
        card_desc1 = "--"

    try:
        global card_atk1
        card_atk1 = carta_escolhida_json['data'][0]["atk"]
    except KeyError as erroAtk:
        card_atk1 = "--"

    try:
        global card_def1
        card_def1 = carta_escolhida_json['data'][0]["def"]
    except KeyError as erroDef:
        card_def1 = "--"

    try:
        global card_level1
        card_level1 = carta_escolhida_json['data'][0]["level"]
    except KeyError as erroLevel:
        card_level1 = "--"

    try:
        global card_race1
        card_race1 = carta_escolhida_json['data'][0]["race"]
    except KeyError as erroRace:
        card_race1 = "--"

    try:
        global card_attribute1
        card_attribute1 = carta_escolhida_json['data'][0]["attribute"]
    except KeyError as erroAttribute:
        card_attribute1 = "--"

    try:
        global card_archetype1
        card_archetype1 = carta_escolhida_json['data'][0]["archetype"]
    except KeyError as erroAttribute:
        card_archetype1 = "--"

    try:
        global card_scale1
        card_scale1 = carta_escolhida_json['data'][0]["scale"]
    except KeyError as erroAttribute:
        card_scale1 = "--"

    try:
        global card_link1
        card_link1 = carta_escolhida_json['data'][0]["linkval"]
    except KeyError as erroAttribute:
        card_link1 = "--"

    if "linkmarkers" in carta_escolhida_json['data'][0]:
        try:

            global card_linkmarker1

            card_linkmarker1 = carta_escolhida_json['data'][0]["linkmarkers"]

            print(card_linkmarker1)

            if "Top" in card_linkmarker1:
                global imagem_cima
                imagem_cima = PhotoImage(file=f"{pasta_de_links}\\link_on_cima.png")
                lb_link_off_sup.config(image=imagem_cima)
            else:
                imagem_cima = PhotoImage(file=f"{pasta_de_links}\\link_off_cima.png")
                lb_link_off_sup.config(image=imagem_cima)

            if "Top-Right" in card_linkmarker1:
                global imagem_cima_dir
                imagem_cima_dir = PhotoImage(file=f"{pasta_de_links}\\link_on_cima_direito.png")
                lb_link_off_sup_dir.config(image=imagem_cima_dir)
            else:
                imagem_cima_dir = PhotoImage(file=f"{pasta_de_links}\\link_off_cima_direito.png")
                lb_link_off_sup_dir.config(image=imagem_cima_dir)

            if "Top-Left" in card_linkmarker1:
                global imagem_cima_esq
                imagem_cima_esq = PhotoImage(file=f"{pasta_de_links}\\link_on_cima_esquerdo.png")
                lb_link_off_sup_esq.config(image=imagem_cima_esq)
            else:
                imagem_cima_esq = PhotoImage(file=f"{pasta_de_links}\\link_off_cima_esquerdo.png")
                lb_link_off_sup_esq.config(image=imagem_cima_esq)

            if "Left" in card_linkmarker1:
                global imagem_esquerda
                imagem_esquerda = PhotoImage(file=f"{pasta_de_links}\\link_on_esquerda.png")
                lb_link_off_esq.config(image=imagem_esquerda)
            else:
                imagem_esquerda = PhotoImage(file=f"{pasta_de_links}\\link_off_esquerda.png")
                lb_link_off_esq.config(image=imagem_esquerda)

            if "Bottom-Left" in card_linkmarker1:
                global imagem_baixo_esq
                imagem_baixo_esq = PhotoImage(file=f"{pasta_de_links}\\link_on_baixo_esquerdo.png")
                lb_link_off_inf_esq.config(image=imagem_baixo_esq)
            else:
                imagem_baixo_esq = PhotoImage(file=f"{pasta_de_links}\\link_off_baixo_esquerdo.png")
                lb_link_off_inf_esq.config(image=imagem_baixo_esq)

            if "Bottom" in card_linkmarker1:
                global imagem_baixo
                imagem_baixo = PhotoImage(file=f"{pasta_de_links}\\link_on_baixo.png")
                lb_link_off_inf.config(image=imagem_baixo)
            else:
                imagem_baixo = PhotoImage(file=f"{pasta_de_links}\\link_off_baixo.png")
                lb_link_off_inf.config(image=imagem_baixo)

            if "Bottom-Right" in card_linkmarker1:
                global imagem_baixo_dir
                imagem_baixo_dir = PhotoImage(file=f"{pasta_de_links}\\link_on_baixo_direito.png")
                lb_link_off_inf_dir.config(image=imagem_baixo_dir)
            else:
                imagem_baixo_dir = PhotoImage(file=f"{pasta_de_links}\\link_off_baixo_direito.png")
                lb_link_off_inf_dir.config(image=imagem_baixo_dir)

            if "Right" in card_linkmarker1:
                global imagem_direita
                imagem_direita = PhotoImage(file=f"{pasta_de_links}\\link_on_direito.png")
                lb_link_off_dir.config(image=imagem_direita)
            else:
                imagem_direita = PhotoImage(file=f"{pasta_de_links}\\link_off_direita.png")
                lb_link_off_dir.config(image=imagem_direita)

        except KeyError as erroAttribute:
            card_linkmarker1 = "--"

        download_imagem(card_id1)
    else:
        # global imagem_cima
        imagem_cima = PhotoImage(file=f"{pasta_de_links}\\link_off_cima.png")
        lb_link_off_sup.config(image=imagem_cima)

        # global imagem_cima_dir
        imagem_cima_dir = PhotoImage(file=f"{pasta_de_links}\\link_off_cima_direito.png")
        lb_link_off_sup_dir.config(image=imagem_cima_dir)

        # global imagem_cima_esq
        imagem_cima_esq = PhotoImage(file=f"{pasta_de_links}\\link_off_cima_esquerdo.png")
        lb_link_off_sup_esq.config(image=imagem_cima_esq)

        # global imagem_esquerda
        imagem_esquerda = PhotoImage(file=f"{pasta_de_links}\\link_off_esquerda.png")
        lb_link_off_esq.config(image=imagem_esquerda)

        # global imagem_baixo_esq
        imagem_baixo_esq = PhotoImage(file=f"{pasta_de_links}\\link_off_baixo_esquerdo.png")
        lb_link_off_inf_esq.config(image=imagem_baixo_esq)

        # global imagem_baixo
        imagem_baixo = PhotoImage(file=f"{pasta_de_links}\\link_off_baixo.png")
        lb_link_off_inf.config(image=imagem_baixo)

        # global imagem_baixo_dir
        imagem_baixo_dir = PhotoImage(file=f"{pasta_de_links}\\link_off_baixo_direito.png")
        lb_link_off_inf_dir.config(image=imagem_baixo_dir)

        # global imagem_direita
        imagem_direita = PhotoImage(file=f"{pasta_de_links}\\link_off_direita.png")
        lb_link_off_dir.config(image=imagem_direita)

        download_imagem(card_id1)


# Função do botão ok, que pesquisa o ID da carta selecionada, chama a função de request, e retorna os status do card
def botao_ok_combobox():
    carta_nome = cb_cartas.get()
    global carta_id
    for i in lista_id_nome_cards_juntos:
        for j, l in i.items():
            if l == carta_nome:
                carta_id = j
                request_card_escolhido(carta_id)
                mostrar_imagem()

                lb_resultado_nome.config(text=card_name1, font="Arial 13")
                lb_resultado_nome.place(x=500, y=65)
                lb_resultado_id.config(text=card_id1, font="Arial 13")
                lb_resultado_id.place(x=500, y=93)
                lb_resultado_tipo.config(text=card_type1, font="Arial 13")
                lb_resultado_tipo.place(x=500, y=121)
                lb_resultado_frametype.config(text=card_frametype1.title(), font="Arial 13")
                lb_resultado_frametype.place(x=500, y=149)
                lb_resultado_ataque.config(text=card_atk1, font="Arial 13")
                lb_resultado_ataque.place(x=500, y=177)
                lb_resultado_defesa.config(text=card_def1, font="Arial 13")
                lb_resultado_defesa.place(x=500, y=205)
                lb_resultado_level.config(text=card_level1, font="Arial 13")
                lb_resultado_level.place(x=500, y=233)
                lb_resultado_raca.config(text=card_race1, font="Arial 13")
                lb_resultado_raca.place(x=500, y=261)
                lb_resultado_atributo.config(text=card_attribute1, font="Arial 13")
                lb_resultado_atributo.place(x=500, y=289)
                lb_resultado_descricao.config(text=card_desc1, font="Arial 11")
                lb_resultado_descricao.place(x=500, y=358)
                lb_resultado_arquetipo.config(text=card_archetype1, font="Arial 13")
                lb_resultado_arquetipo.place(x=905, y=93)
                lb_resultado_escala.config(text=card_scale1, font="Arial 13")
                lb_resultado_escala.place(x=905, y=121)
                lb_resultado_valor_link.config(text=card_link1, font="Arial 13")
                lb_resultado_valor_link.place(x=905, y=149)
                # lb_resultado_valor_linkmarkers.config(text=card_linkmarker1, font="Arial 13")
                # lb_resultado_valor_linkmarkers.place(x=905, y=177)


# Função que gera a imagem no label
def mostrar_imagem():
    global img_carta
    caminho_carta = f"{pasta_de_imagens}\\{carta_id}.png"
    img_carta = tkinter.PhotoImage(file=caminho_carta)
    lb_imagem = Label(janela, image=img_carta)
    lb_imagem.place(x=20, y=20)


# Label do texto pesquise pela sua carta
lb_sua_carta = Label(janela, text="Pesquise pela sua carta", background="#d1d2d4")
lb_sua_carta.place(x=805, y=2)

# Combobox
cb_cartas = ttk.Combobox(janela, width=40, values=lista_nome_cards, exportselection=False)
cb_cartas.place(x=745, y=20)
cb_cartas.bind('<KeyRelease>', search)


# função de callback para o bind do botão
def botao_ok_combobox_callback(event):
    botao_ok_combobox()


# Botão ok do combobox
botao_confirmar = Button(janela, text="OK", width=7, height=1, command=botao_ok_combobox)
botao_confirmar.bind("<Return>", botao_ok_combobox_callback)
botao_confirmar.place(x=1015, y=16)

# Label da quantidade de cartas!
lb_sua_carta = Label(janela, font="Arial 14 bold", text=f"Já temos   {quantas_cartas_na_colecao}   cards no catálogo!",
                     foreground="#002e51", background="#d1d2d4")
lb_sua_carta.place(x=380, y=16)

# Labels do nome
# lb_nome = Label(janela, text="Nome:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_nome.place(x=405, y=62)

lb_resultado_nome = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_nome.place(x=500, y=62)

# Labels do ID
# lb_id = Label(janela, text="ID:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_id.place(x=405, y=90)

lb_resultado_id = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_id.place(x=500, y=90)

# Labels do tipo
# lb_tipo = Label(janela, text="Tipo:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_tipo.place(x=405, y=118)

lb_resultado_tipo = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_tipo.place(x=500, y=118)

# Labels do frametype
# lb_frametype = Label(janela, text="Ftype:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_frametype.place(x=405, y=146)

lb_resultado_frametype = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_frametype.place(x=500, y=146)

# Labels do ataque
# lb_ataque = Label(janela, text="Ataque:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_ataque.place(x=405, y=174)

lb_resultado_ataque = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_ataque.place(x=500, y=174)

# Labels da defesa
# lb_defesa = Label(janela, text="Defesa:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_defesa.place(x=405, y=202)

lb_resultado_defesa = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_defesa.place(x=500, y=202)

# Labels do level
# lb_level = Label(janela, text="Level:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_level.place(x=405, y=230)

lb_resultado_level = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_level.place(x=500, y=230)

# Labels da raça
# lb_raca = Label(janela, text="Raça:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_raca.place(x=405, y=258)

lb_resultado_raca = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_raca.place(x=500, y=258)

# Labels do Atributo
# lb_atributo = Label(janela, text="Atributo:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_atributo.place(x=405, y=286)

lb_resultado_atributo = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_atributo.place(x=500, y=286)

# Labels do arquetipo
# lb_arquetipo = Label(janela, text="Arquetipo:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_arquetipo.place(x=810, y=90)

lb_resultado_arquetipo = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_arquetipo.place(x=905, y=90)

# Labels do escala de pêndulo
# lb_escala = Label(janela, text="Escala:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_escala.place(x=810, y=118)

lb_resultado_escala = Label(janela, text="     ---", font="Arial 15", background="#d1d2d4")
lb_resultado_escala.place(x=905, y=118)

# Labels do valor link
# lb_valor_link = Label(janela, text="Link:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_valor_link.place(x=810, y=146)

lb_resultado_valor_link = Label(janela, text="     ---    ", font="Arial 15", background="#d1d2d4")
lb_resultado_valor_link.place(x=905, y=146)

# Labels do valor linkmarkers
# lb_valor_linkmarkers = Label(janela, text="Link M:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_valor_linkmarkers.place(x=810, y=180)

lb_resultado_valor_linkmarkers = Label(janela, text="       ", font="Arial 15", background="#d1d2d4")
lb_resultado_valor_linkmarkers.place(x=905, y=194)

# Labels da descrição
# lb_descricao = Label(janela, text="Desc:", font="Arial 15", foreground="#E0DFCA", background="#d1d2d4")
# lb_descricao.place(x=405, y=314)

lb_resultado_descricao = Label(janela, text="     ---    ", font="Arial 15", wraplength=500, justify=LEFT,
                               background="#d1d2d4")
lb_resultado_descricao.place(x=705, y=460)

# imagem link off canto superior direito
link_link_off_sup_dir = f"{pasta_de_links}\\link_off_cima_direito.png"
link_off_sup_dir = tkinter.PhotoImage(file=link_link_off_sup_dir)
lb_link_off_sup_dir = Label(janela, image=link_off_sup_dir, background="#d1d2d4")
lb_link_off_sup_dir.place(x=1000, y=174)

# imagem link off superior
link_link_off_sup = f"{pasta_de_links}\\link_off_cima.png"
link_off_sup = tkinter.PhotoImage(file=link_link_off_sup)
lb_link_off_sup = Label(janela, image=link_off_sup, background="#d1d2d4")
lb_link_off_sup.place(x=950, y=170)

# imagem link off canto superior esquerdo
link_link_off_sup_esq = f"{pasta_de_links}\\link_off_cima_esquerdo.png"
link_off_sup_esq = tkinter.PhotoImage(file=link_link_off_sup_esq)
lb_link_off_sup_esq = Label(janela, image=link_off_sup_esq, background="#d1d2d4")
lb_link_off_sup_esq.place(x=900, y=174)

# imagem link off direito
link_link_off_dir = f"{pasta_de_links}\\link_off_direita.png"
link_off_dir = tkinter.PhotoImage(file=link_link_off_dir)
lb_link_off_dir = Label(janela, image=link_off_dir, background="#d1d2d4")
lb_link_off_dir.place(x=1010, y=224)

# imagem link off esquerdo
link_link_off_esq = f"{pasta_de_links}\\link_off_esquerda.png"
link_off_esq = tkinter.PhotoImage(file=link_link_off_esq)
lb_link_off_esq = Label(janela, image=link_off_esq, background="#d1d2d4")
lb_link_off_esq.place(x=896, y=220)

# imagem link off canto inferior direito
link_link_off_inf_dir = f"{pasta_de_links}\\link_off_baixo_direito.png"
link_off_inf_dir = tkinter.PhotoImage(file=link_link_off_inf_dir)
lb_link_off_inf_dir = Label(janela, image=link_off_inf_dir, background="#d1d2d4")
lb_link_off_inf_dir.place(x=1000, y=274)

# imagem link off inferior
link_link_off_inf = f"{pasta_de_links}\\link_off_baixo.png"
link_off_inf = tkinter.PhotoImage(file=link_link_off_inf)
lb_link_off_inf = Label(janela, image=link_off_inf, background="#d1d2d4")
lb_link_off_inf.place(x=950, y=277)
#
# imagem link off canto inferior esquerdo
link_link_off_inf_esq = f"{pasta_de_links}\\link_off_baixo_esquerdo.png"
link_off_inf_esq = tkinter.PhotoImage(file=link_link_off_inf_esq)
lb_link_off_inf_esq = Label(janela, image=link_off_inf_esq, background="#d1d2d4")
lb_link_off_inf_esq.place(x=900, y=274)

janela.mainloop()
