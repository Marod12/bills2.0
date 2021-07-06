# -*- coding: utf-8 -*-
import json
import random
import datetime
from lib.arquivo import *
from lib.interface import *
from lib.bd import *


##  Cadastro  ##
def cadastro():
    servico = {}  # dict()  #{}

    while True:
        name = str(input(cor('white+')+ f"{' '*4}Digite o nome do serviço: " + cor('reset'))).upper()
        login = str(input(cor('white+')+ f"{' '*4}Digite o login do serviço: " + cor('reset')))
        senha = str(input(cor('white+')+ f"{' '*4}Digite a senha do serviço: " + cor('reset')))

        #Gera uma chave aleatória
        key = int(random.randrange(32, 513))

        #Encripta o login e a senha
        loginEncrypt = encrypt(login, key)
        senhaEncrypt = encrypt(senha, key)

        #Adiciona os dados ao dict
        servico["name"] = name
        servico["data"] = {}
        servico["data"]["key"] = key
        servico["data"]["login"] = loginEncrypt
        servico["data"]["senha"] = senhaEncrypt

        #verifica se quer adicionar mais algum dado
        while True:
            print()
            question = questionSN(cor('white+') + "  Deseja cadastrar mais dados? [S/N]: " + cor('reset'), 'S', 'N')
            if question == "N":
                break
            
            print()
            nomeDoDado = str(input(cor('white+') + f"{' '*4}Nome do dado: " + cor('reset')))
            dado = str(input(cor('white+') + f"{' '*4}Dado: " + cor('reset')))

            #Encripta o dado 
            dadoEncrypt = encrypt(dado, key)

            #Adiciona os dado ao dict
            servico["data"][nomeDoDado] = dadoEncrypt  # or servico[nomeDoDado: Dado]

        '''Dicts functions
        print(len(servico))
        #servico.clear
        print(servico.values())
        print(servico.keys())
        print(servico.items())'''

        #Envia o dado para ser inserido ao bd e espera a msg de retorno do bd
        insertService(servico)

        servico.clear()  # limpa o dict(),  apagando um serviço antes de add outro

        #Verifica se quer adicionar outro serviço
        print()
        question = questionSN(cor('white+') + "  Deseja cadastrar outro serviço? [S/N]: " + cor('reset'), 'S', 'N')
        if question == "N":
            break


## Todos os Serviços ##
def allServicos():
    servicos = selectServicesNames()

    printColorido(f'{len(servicos)} serviços cadastrados', "gray", 2)

    #Mostra todos os dados
    for servico in servicos:
        printColorido(servico[0], "gray")
    
    printColorido(linha(38).center(40), "gray", 1)


## Pesquisa ##
def pesquisa():
    servicos = []
    if servicos == []:
        #Armazerna o retorno do bd na variável
        servicos = selectServicesPesquisa()

    pesquisa = str(input(cor('white+') + f"{' '*4}Pesquisa: " + cor('reset'))).upper()

    printColorido(linha(38), 'gray', 1)
    #Verifica se o que foi digitado existe e armazena em uma lista 
    resultadoPesquisa = []
    for servico in servicos:
        if pesquisa in servico['name']:
            resultadoPesquisa.append(servico)       

    if resultadoPesquisa == []: #se a lista não tiver nenhum dado
        printColorido('* Nenhum serviço foi encontrado! *', 'gray', 1)
        printColorido(linha(38), 'gray', 2)
    else:
        if len(resultadoPesquisa) == 1: #se a lista tiver só um servico nela
            #Mostra 1 dado encontrado
            printColorido(f'{len(resultadoPesquisa)} serviço encontrado', 'gray', 1)
            printColorido(resultadoPesquisa[0]["name"], 'gray', 1)
            printColorido(linha(38), 'gray', 2)

            #Verifica se o dado pode ser mostrado
            question = questionSN(cor('white+') + "  Deseja ver os dados desse serviço? [S/N]: " + cor('reset'), 'S', 'N')
            if question == 'S':
                verDados(resultadoPesquisa[0]['id'])

        if len(resultadoPesquisa) > 1: #se a lista tiver mais de 1 servico nela
            cont = 1
            #Mostra varios dados encontrados
            printColorido(f'{len(resultadoPesquisa)} serviços encontrados', 'gray', 2)
            for i in resultadoPesquisa:
                printColorido(f'{cont} - {i["name"]}', 'gray')
                cont += 1
            printColorido(linha(38), 'gray', 2)

            #Verifica se algum dado pode ser mostrado
            question = questionSN(cor('white+') + "  Deseja ver os dados de algum desses serviços? [S/N]: " + cor('reset'), 'S', 'N')
            if question == 'S':
                print()
                #Verifica qual dado será mostrado
                numServico = validandoNum(cor('white+') + "  Digite o número do serviço que deseja ver: " + cor('reset'), len(resultadoPesquisa))
                verDados(resultadoPesquisa[numServico - 1]['id'])

## Ver dados de um serviços ##
def verDados(data):
    dados = selectServiceDados(data)

    printColorido(linha(38).center(40), "gray", 1)
    printColorido(dados["name"], "gray", 2)
    
    #Mostra cada um dos dados
    for k, i  in dados['data'].items():
        if k != 'key':
            printColorido(f'{k} -- {decrypt(i, dados["data"]["key"])}', "gray")

    #Mostra quando foi criado
    ## Transforma a str em datetime
    createIn = datetime.datetime.strptime(dados["createIn"], '%Y-%m-%d %H:%M:%S.%f')
    
    ## Transforma no formato dd/mm/yyyy
    criadoEm = datetime.datetime.date(createIn).strftime("%d/%m/%Y")
    printColorido(f'Criado em {criadoEm}', "gray", 1)      

    #Mostra quando foi atualizado e quanto tempo faz
    if dados["updateIn"] != None:
        ## Transforma a str em datetime
        updateIn = datetime.datetime.strptime(dados["updateIn"], '%Y-%m-%d %H:%M:%S.%f')
        
        ## Transforma no formato dd/mm/yyyy
        atualizadoEm = datetime.datetime.date(updateIn).strftime("%d/%m/%Y")
        printColorido(f'Atualizado em {atualizadoEm}', "gray", 1)
        
        #Diferença entre duas datas, formato datetime
        dif = datetime.datetime.utcnow() - updateIn

        #Calculos da diferença entre as datas
        semanas = int(dif.days // 7) #calculo das semanas
        dias = int(dif.days) #retorno da difernça em dias
        horas = int(((int(dif.seconds) // 60) // 60) % 60) #calculo das horas
        minutos = int((int(dif.seconds) // 60) % 60) #calculo dos minutos
        segundos = int(int(dif.seconds) % 60) #calculo dos segundos

        """
            Tive que fazer os calculos, porque so essas funcões 
            de retorno estavam funcionando.

            Funções que não funcionaram
                dif.years
                dif.months
                dif.weeks
                dif.hours    
                dif.minutes
        """

        printColorido('há', "gray")
        #Condição para mostrar quanto tempo faz que foi atualizado
        if semanas > 0:
            printColorido(f'{semanas} semanas e {dias % 7} dias', "gray")
        elif dias > 0:
            printColorido(f'{dias} dias e {horas} horas', "gray")
        elif horas > 0:
            printColorido(f'{horas} horas e {minutos} minutos', "gray")
        elif minutos > 0:
            printColorido(f'{minutos} minutos e {segundos} segundos', "gray")
        elif segundos > 0:
            printColorido(f'{segundos} segundos', "gray")

    printColorido(linha(38).center(40), "gray", 2)

    #Verifica se quer fazer algo com o serviço, mostra o menu do serviço
    question = questionSN(cor('white+') + "  Deseja fazer algo? [S/N]: " + cor('reset'), 'S', 'N')
    if question == 'S':
        menuServico(dados) 


## Menu do serviço ##            
def menuServico(data):
    while True:
        resposta = menu(f'MENU - {data["name"]}', ['Alterar', 'Deletar','Voltar <-'], 38, 42, None, 4)
        if resposta == 1:
            # Atualiza algum dado do serviço!
            menuUpdate(data)
            break
        elif resposta == 2:
            # Deleta o serviço!
            cabecalhoColorido(f'Deletar - {data["name"]}', 2,'red+', 36, 40)
            deleteServico([data['id'], data['name']])
            break
        elif resposta == 3:
            break
        else:
            printColorido('ERRO! Digite uma opção válida!', "red+", 2)


## Menu update do serviço ##
def menuUpdate(data):
    dadoAlterado = {}
    dadosAlterar = []
    
    #Coloca os dado em um novo dict
    dadoAlterado["id"] = data['id']
    dadoAlterado["name"] = data['name']
    dadoAlterado["data"] = {}
    dadoAlterado["updateIn"] = datetime.datetime.utcnow()

    #Gera um número aleatório e add a key
    newKey = int(random.randrange(32, 513))
    dadoAlterado["data"]["key"] = newKey

    #Para cada item em data é alterado o dado com uma nova criptografia
    for k, i  in data['data'].items():
        if k != 'key':
            dadoAlterado["data"][k] = encrypt(decrypt(i, data["data"]["key"]), newKey)

    #Munu para os dado que seram alterados
    while True:
        #para cada dado em data add em dadosAlterar ** os dados que podem ser alterados **
        dadosAlterar.append('name')
        for k in dadoAlterado['data'].keys():
            if k != 'key':
                dadosAlterar.append(k)

        #adiciona as opções principais do menu altera
        if len(dadosAlterar) > 3:
            dadosAlterar.append('remover um dado')
        dadosAlterar.append('add um novo dado')
        dadosAlterar.append('SALVAR alterações')
        dadosAlterar.append('Voltar <-')

        resposta = menu(f'Alterar - {dadoAlterado["name"]}', dadosAlterar, 36, 40, 'yellow', 5)

        #Erro de valor não aceito
        if resposta == 0 or resposta > len(dadosAlterar):
            printColorido('ERRO! Digite uma opção válida!', "red+", 1)
        else:
            ultimo = int(dadosAlterar.index(dadosAlterar[-1])) + 1
            penultimo = int(dadosAlterar.index(dadosAlterar[-2])) + 1
            antepenultimo = int(dadosAlterar.index(dadosAlterar[-3])) + 1
            anteantepenultimo = int(dadosAlterar.index(dadosAlterar[-4])) + 1

            #Volta para o menu principal
            if resposta == len(dadosAlterar): # or ultimo
                question = questionSN(cor('white+') + "  Deseja salvar as alterações feitas? [S/N]: " + cor('reset'), 'S', 'N')
                if question == 'S':
                    updateServico([data, dadoAlterado])
                    break
                else:
                    break

            #Salva as alterações
            if resposta == penultimo:
                updateServico([data, dadoAlterado])
                break

            #Add um novo dado ao serviço
            if resposta == antepenultimo:
                cabecalhoColorido('Add um novo dado', 2, None, 34)
                nomeDoNovoDado = str(input(cor('white+') + f"{' '*4}Nome do dado: " + cor('reset')))
                novoDado = str(input(cor('white+') + f"{' '*4}Dado: " + cor('reset')))

                dadoAlterado["data"][nomeDoNovoDado] = encrypt(novoDado, newKey)

                printColorido(f'{nomeDoNovoDado} -- {novoDado}', "cyan", 1)
                printColorido('adicionado com SUCESSO!', "green+")

            #Remove um dado do serviço
            if len(dadosAlterar) > 6:
                if resposta == anteantepenultimo:
                    dadoExcluir = dadosAlterar[3:-4] #pega os valores da lista que podem ser excluidos
                    
                    dadoExcluir.append('Voltar <-')

                    while True:
                        respostaExcluir = menu('Remover dado', dadoExcluir, 34, 40, 'red', 6)

                        if respostaExcluir == 0 or respostaExcluir > len(dadoExcluir):
                            printColorido('ERRO! Digite uma opção válida!', "red+", 1)
                        else:
                            if respostaExcluir == len(dadoExcluir):
                                break
                            else:
                                #deleta o dado escolhido do dict 
                                dadoAlterado["data"].pop(dadoExcluir[respostaExcluir - 1]) 

                                printColorido(dadoExcluir[respostaExcluir - 1], "cyan", 1)
                                printColorido('removido com SUCESSO!', "green+")
                                break           

            #Altera um dado existente no serviço
            dadoAlterar = []
            if len(dadosAlterar) > 6:
                dadoAlterar = dadosAlterar[0:-4] #pega os valores da lista que corresponde aos dos dados - nome
            else:
                dadoAlterar = dadosAlterar[0:-3] # or [:3]pega os 3 primeiros valores da lista - nome
            
            if resposta <= len(dadoAlterar): 
                ## Altera o nome
                if resposta == 1:
                    cabecalhoColorido('Alterar - nome', 1, 'yellow+', 34, 40)
                    printColorido(f'{dadosAlterar[0]} atual é {dadoAlterado["name"]}', 'white+', 2)
                    novoValor = str(input(cor('white+') + f"{' '*4}Digite o novo Nome para o serviço: "  + cor('reset'))).upper()
                    dadoAlterado["name"] = novoValor
                    printColorido(f'{dadosAlterar[0]} alterado para {novoValor}', "cyan", 1)
                    printColorido('com SUCESSO!', "green+")
                ## Altera os outros dados
                else:
                    cabecalhoColorido(f'Alterar - {dadosAlterar[resposta - 1]}', 1, 'yellow+', 34, 40)
                    dadoAtual = decrypt(dadoAlterado["data"][dadosAlterar[resposta - 1]], newKey)
                    printColorido(f'{dadosAlterar[resposta - 1]} atual é {dadoAtual}', 'white+', 2)
                    novoValor = str(input(cor('white+') + f"{' '*4}Digite oa nov(oa) {dadosAlterar[resposta - 1]} do serviço: "  + cor('reset')))
                    dadoAlterado["data"][dadosAlterar[resposta - 1]] = encrypt(novoValor, newKey)
                    printColorido(f'{dadoAtual} alterado para {novoValor}', "cyan", 1)
                    printColorido('com SUCESSO!', "green+")                
  
        dadosAlterar.clear() #limpa a lista

        
## Update do serviço ##
def updateServico(data):
    printColorido('Alterado de', 'white+', 1)
    #dados Originais
    printColorido(linha(34), 'gray', 1)
    printColorido(data[0]['name'], 'gray', 2)
    for k, i  in data[0]['data'].items():
        if k != 'key':
            printColorido(f'{k} -- {decrypt(i, data[0]["data"]["key"])}', 'gray')

    printColorido(linha(34), 'gray', 2)

    #retorno do update no bd
    updateService(data[1])
    printColorido('Para', 'white+')

    #dados Alterados
    printColorido(linha(34), 'gray', 1)
    printColorido(data[1]['name'], 'gray', 2)
    for k, i  in data[1]['data'].items():
        if k != 'key':
            printColorido(f'{k} -- {decrypt(i, data[1]["data"]["key"])}', 'gray')

    printColorido(linha(34), 'gray', 1)
    

## Deleta o serviço ##
def deleteServico(data):
    printColorido('** O serviço será ', 'red+')
    printColorido('deletado', 'red+')
    printColorido('permanentemente! **', 'red+')
    printColorido(linha(36), 'red+', 1)
    question = questionSN(cor('white+') + f'{" "* 5}Tem Certeza? [S/N]: ' + cor('reset'), 'S', 'N')
    if question == 'S':
        #Retorna a resposta do bd
        deleteService(data)


## BackUP ##
# Insere um backup
def inserirBackup():
    arqInport = str(input(cor('white+')+ f"{' '*4}Digite o nome do arquivo: " + cor('reset')))
    arqInport = './' + arqInport + '.txt'

    insertBackup(arqInport)


# Faz um backup
def fazerBackup():
    arqExport = str(input(cor('white+')+ f"{' '*4}Digite o nome do arquivo: " + cor('reset')))
    arqExport = './' + arqExport + '.txt'

    fazBackup(arqExport)
