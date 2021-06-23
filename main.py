# -*- coding: utf-8 -*-
# parte inicial do programa
from lib.servico import *

while True:
    resposta = menu('MENU PRINCIPAL', ['Todos os Serviços', 'Pesquisa','Cadastro de Serviço', 'Sair do Sistema'])
    if resposta == 1:
        # Lista todos os serviços!
        cabecalhoColorido('Todos os Serviços', 1, 'gray', 38, 40)
        allServicos()
    elif resposta == 2:
        # Pesquisar por um serviço!
        cabecalhoColorido('Pesquisa', 1, 'gray', 38, 40)
        pesquisa()
    elif resposta == 3:
        # Cadastrar um serviço novo!
        cabecalhoColorido('Cadastro de Serviço', 2, 'gray', 38, 40)
        cadastro()
    elif resposta == 4:
        cabecalhoColorido('Saindo do Sistema...  Até logo', 2, 'gray', 38, 40)
        break
    else:
        printColorido('ERRO! Digite uma opção válida!', "red+", 1)