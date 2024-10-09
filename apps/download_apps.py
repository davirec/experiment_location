from os import pipe2

import csv
import os
import requests


def baixar_arquivo(arquivo_csv, diretorio_destino):
    # Abre o arquivo CSV para leitura
    print(diretorio_destino)
    with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
        leitor = csv.reader(csvfile, delimiter=';')
        # Itera sobre as linhas e imprime a quarta coluna
        for linha in leitor:
            if len(linha) >= 4:  # Verifica se a linha tem pelo menos 4 colunas
                # print(linha[3])
                nome = linha[2].split("/")[-1]
                app_path = os.path.join(diretorio_destino, nome)
                request_url(linha[2], app_path)


def baixar_arquivos_csv(nome_arquivo):
    # Verifica se a pasta de destino existe, caso contrário, cria


    if os.path.isfile(nome_arquivo):
        # Nome do diretório será o nome do arquivo (sem extensão)
        nome_diretorio = os.path.splitext(nome_arquivo)[0]

        # Cria o diretório
        if not os.path.exists(nome_diretorio):
            os.makedirs(nome_diretorio)
        # print('sss'+nome_arquivo+" "+diretorio_destino)
        baixar_arquivo(nome_arquivo, nome_diretorio)


def request_url(url, endereco):
    resposta = requests.get(url)
    if resposta.status_code == requests.codes.OK:
        with open(endereco, 'wb') as novo_arquivo:
                novo_arquivo.write(resposta.content)
        print("Download finalizado {}".format(endereco))
    else:
        resposta.raise_for_status()


if __name__ == "__main__":
    # Defina o caminho para a pasta de origem e destino
    pasta_origem_csv = '/home/davi/projetos_git/experiment_location/apps/apks.csv'

    baixar_arquivos_csv(pasta_origem_csv)
