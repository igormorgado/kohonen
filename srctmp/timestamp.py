from datetime import datetime
import pytz



# entra com o nome do operador
O = input("Escreva a primeira letra do seu nome: ")
A = input("Entre com o nome do arquivo: ")


# data atual
local = datetime.now()


str = [local.strftime("%Y%m%d%H%M%S_"),O, "_", A]
str = str.replace(" ", "")

print(local.strftime("%Y%m%d%H%M%S_"),O,"_",A )
