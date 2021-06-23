# -*- coding: utf-8 -*-
# parte inicial do programa
from lib.servico import *

while True:
    #Faz a lista do menu
    menuMain = ['Todos os Serviços', 'Pesquisa', 'Cadastro de Serviço']
    if selectServicesNames() == []:
        menuMain.append('Inserir backup')
    else:
        menuMain.append('Fazer backup')
    menuMain.append('Sair do Sistema')

    #Menu
    resposta = menu('MENU PRINCIPAL', menuMain)
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
        # Insere um backup
        cabecalhoColorido(menuMain[-2], 2, 'gray', 38, 40)
        if selectServicesNames() == []:
            inserirBackup()
        # Faz um backup
        else:
            fazerBackup()
    elif resposta == 5:
        cabecalhoColorido('Saindo do Sistema...  Até logo', 2, 'gray', 38, 40)
        break
    else:
        printColorido('ERRO! Digite uma opção válida!', "red+", 1)
        