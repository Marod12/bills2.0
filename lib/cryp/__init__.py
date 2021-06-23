# -*- coding: utf-8 -*-
import json, base64

#Crypt
def cryp(data):
    # Converte Python dict para JSON
    msg = json.dumps(data)
    return base64.b64encode(msg.encode('utf-8'))


#Decrypt
def decryp(data):
    retorno = base64.b64decode(data)
    # Converte string para Python dict
    msg = json.loads(retorno)
    return msg


###  Crypt  ###
Alfabeto = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'

def crypt(msg, dir, key):
    cond = key
    m = ''
    for c in msg:
        if c in Alfabeto:
            c_index = Alfabeto.index(c)
            m += Alfabeto[(c_index + (dir * cond)) % len(Alfabeto)]
        else:
            m += c
    return m

def encrypt(msg, key):
    return crypt(msg, len(msg), key)

def decrypt(msg, key):
    return crypt(msg, -len(msg), key)