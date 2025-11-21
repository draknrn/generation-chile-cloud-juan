# Programa que realiza operaciones aritméticas básicas entre dos números ingresados por el usuario
print("Calculadora básica")
n1 = input("Ingrese el primer valor: ")

operadores = ["+", "-", "*", "/"]
operador = input("Ingrese operador [""+"", ""-"", ""*"", ""/""]: ")
while operador not in operadores:
    print("Operador no válido. Por favor, use [""+"", ""-"", ""*"" o ""/""]")
    operador = input("Ingrese operador [""+"", ""-"", ""*"", ""/""]: ")

n2 = input("Ingrese el segundo valor: ")
def convertir_numero(valor): # Convierte la entrada del usuario a int o float según corresponda
    if "." in valor or "," in valor:
        valor = valor.replace(",", ".")
        return float(valor)
    else:
        return int(valor)

n1 = convertir_numero(n1)
n2 = convertir_numero(n2)

if operador == "+": # Realiza la operación según el operador ingresado
    print(f"{n1}+{n2} = {n1 + n2}")
elif operador == "-":
    print(f"{n1}-{n2} = {n1 - n2}")
elif operador == "*":
    print(f"{n1} * {2} = {n1 * n2}")
elif operador == "/":
    if n2 != 0:
        print(f"{n1}/{n2} = {n1 / n2}")
    else:
        print("Error: División por cero no permitida.")