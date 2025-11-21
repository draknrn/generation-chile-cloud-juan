
print("Ingrese números a sumar: ")
n1 = input("Número 1: ")
n2 = input("Número 2: ")

def convertir_numero(valor):
    if "." in valor or "," in valor:
        valor = valor.replace(",", ".")
        return float(valor)
    else:
        return int(valor)

n1 = convertir_numero(n1)
n2 = convertir_numero(n2)

print("La suma es:", n1 + n2)