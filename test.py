O = input("Oracion: ")

a = O.count('a') + O.count('A')+ 0
e = O.count('e') + O.count('E')+ 0
i = O.count('i') + O.count('I')+ 0
o = O.count('o') + O.count('O')+ 0
u = O.count('u') + O.count('U')+ 0

print(f'a: {a}\ne: {e}\ni: {i}\no: {o}\nu: {u}\n' )


frase = input('Ingresa una palabra o frase: ')

for c in frase:
    if c in ['a', 'e', 'i', 'o', 'u']:
        print(c, end='')