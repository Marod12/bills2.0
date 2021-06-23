def leiaInt(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            printColorido('ERRO: por favor, digite um número inteiro válido.', "red+", 2)
            continue
        except (KeyboardInterrupt):
            printColorido('Usuário preferiu não digitar esse número.', "red+", 2)
            return 0
        else:
            return n


def validandoNum(msg, valor):
    while True:
        m = leiaInt(msg)
        if m <= valor and m > 0:
            return m
            break
        else:
            printColorido('ERRO! Digite uma opção válida!', "red+", 2)


def questionSN(msg, metodo, metodo2):
    while True:
        m = str(input(msg)).upper().strip()
        if m == metodo:
            return m
            break
        elif m == metodo2:
            return m
            break
        else:
            printColorido('ERRO! Digite uma opção válida!', "red+", 2)


def linha(tam):  #tam = 42
    return '-' * tam


def menu(nomeMenu, lista, tam=42, aoCentro=42, suaCor=None, esp=2):
    cabecalhoColorido(nomeMenu, 1, suaCor, tam, aoCentro)
    c = 1
    for item in lista:
        if suaCor == None:
            print(cor('white+') + f'{" " * esp}{c}' + cor('reset') + ' - ' + item)
        else:
            print(cor(suaCor) + f'{" " * esp}{c}' + ' - ' + item + cor('reset'))
        c += 1

    if suaCor == None:
        print(f'{" " * (esp - 2)}' + linha(tam))
    else:    
        printColorido(linha(tam), suaCor)
    opc = leiaInt(cor('white+')+ f' Sua Opção: ' + cor('reset'))
    return opc
    

def cor(data):
    if data == 'reset':
        return "\033[0m"
    if data == 'reset+':
        return "\033[0"
    if data == 'red':
        return "\033[0;31m"
    if data == 'red+':
        return "\033[1;31m"
    if data == 'gray':
        return "\033[1;30m"
    if data == 'cyan':
        return "\033[1;36m"
    if data == 'green':
        return "\033[32m"
    if data == 'green+':
        return "\033[1;32m"
    if data == 'yellow':
        return "\033[0;33m"
    if data == 'yellow+':
        return "\033[1;33m"
    if data == 'white+':
        return "\033[1;37m"


def printColorido(msg, suaCor, esp=None, tam=40):
    if esp == 1:
        print(cor(suaCor), '\n', '{:^{}}'.format(msg, tam), cor("reset"))
    elif esp == 2:
        print(cor(suaCor), '\n', '{:^{}}'.format(msg, tam), '\n', cor("reset"))
    else:
        print(cor(suaCor), '{:^{}}'.format(msg, tam), cor("reset"))


def cabecalhoColorido(msg, esp=2, suaCor=None, tam=42, aoCentro=42):
    if esp == 1:
        if suaCor == None:
            print()
            print(linha(tam).center(aoCentro))
            print('{:^{}}'.format(msg, 42))
            print(linha(tam).center(aoCentro))
        else:
            print(cor(suaCor), '\n', linha(tam).center(aoCentro), cor("reset"))
            print(cor(suaCor), '{:^{}}'.format(msg, 40), cor("reset"))
            print(cor(suaCor), linha(tam).center(aoCentro), cor("reset"))
    if esp == 2:
        if suaCor == None:
            print()
            print(linha(tam).center(aoCentro))
            print('{:^{}}'.format(msg, 42))
            print(linha(tam).center(aoCentro), '\n')
        else:
            print(cor(suaCor), '\n', linha(tam).center(aoCentro), cor("reset"))
            print(cor(suaCor), '{:^{}}'.format(msg, 40), cor("reset"))
            print(cor(suaCor), linha(tam).center(aoCentro), '\n', cor("reset"))
        