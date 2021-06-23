# -*- coding: utf-8 -*-
# trabalha com a parte dos arquivos
from lib.interface import *

def abrirBackup(nome):
    try:
        a = open(nome, 'rt')
    except:
        printColorido('ERRO ao ler o arquivo!', "red+", 1)
    else:
        return a.read()
    finally:
        a.close()


def salvarBackup(arq, servicos):
    try:
        a = open(arq, 'wt+')
    except:
        printColorido('Houve um ERRO na criação do arquivo!', "red+", 1)
    else:
        try:
            a.write(servicos)
            a.close()
        except:
            printColorido('Houve um ERRO na hora de escrever os dados!', "red+", 1)
