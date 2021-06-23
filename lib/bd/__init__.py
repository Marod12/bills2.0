# -*- coding: utf-8 -*-
import sqlite3
import datetime
import json
from lib.cryp import *
from lib.interface import *

#data utc
nowUtc = datetime.datetime.utcnow()

conn = sqlite3.connect('servicos.db')

cursor = conn.cursor()

#Table Services
cursor.execute('''
CREATE TABLE IF NOT EXISTS services (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name NOT NULL,
    data NOT NULL,
    createIn NOT NULL,
    updateIn
)
''')

 
## Insert ##
# Create Services #
def insertService(data):
    dataService = cryp(data['data']).decode('utf-8')
    cursor.execute(f'''
            INSERT INTO services (name, data, createIn)
            VALUES ('{data['name']}', '{dataService}', '{nowUtc}') 
        ''')
    conn.commit()
    #retorno do insert
    printColorido(data["name"], "cyan", 1)
    printColorido('add com SUCESSO!', "green+")


## Select ##
# Select Services #
def selectServicesNames():
    cursor.execute('SELECT name FROM services ORDER BY name ASC')
    return cursor.fetchall()


def selectServicesPesquisa():
    cursor.execute('SELECT id, name FROM services ORDER BY name ASC')
    data = cursor.fetchall()

    dataReturn = []
    for i in data:
        dataReturn.append({'id': i[0], 'name': i[1]})

    return dataReturn


def selectServiceDados(data):
    cursor.execute(f'SELECT id, name, data, createIn, updateIn FROM services WHERE id = {data}')

    dataReturn = cursor.fetchone()
    dados = decryp(dataReturn[2])

    retorno = {}

    retorno["id"] = dataReturn[0]
    retorno["name"] = dataReturn[1]
    retorno["data"] = dados
    retorno["createIn"] = dataReturn[3]
    retorno["updateIn"] = dataReturn[4]

    return retorno


## Update ##
# Update Services #
def updateService(data):
    dataService = cryp(data['data']).decode('utf-8')
    cursor.execute(f'''
            UPDATE services 
            SET name = '{data["name"]}', data = '{dataService}', updateIn = '{data["updateIn"]}'
            WHERE id ='{data["id"]}'
        ''')
    conn.commit()
    #retorno do update
    printColorido('com SUCESSO!', 'green+')

## Delete ##
# Delete Services #
def deleteService(data):
    cursor.execute(f'DELETE FROM services WHERE id = {data[0]}')
    conn.commit()
    #retorno do delete
    printColorido(data[1], "cyan", 1)
    printColorido('deletado com SUCESSO!', "green+")
    

def fecharConexao():
    cursor.close()
