# def Nome():
#     nome = input(" Digite o seu nome? ")
#     print("Seja bem vindo(a)", nome )
# Nome()

# def Salario():
#     salario = float(input("Digite o seu salário por mes: "))
#     print("Seu salário é de: ", salario )
# Salario()

# def Soma():
#     valor1 = int(input("Digite o primeiro valor: "))
#     valor2 = int(input("Digite o segundo valor: "))
#     soma = valor1 + valor2
#     print(soma)
# Soma()

def Menu():
    print("Opções do Menu:")
    print("Para acessar escolha 1:")
    print("Para sair escolha 0:")
    escolha = int(input("Escolha: "))
    if escolha == 1:
            Acesso()
    elif escolha == 0:
            print("Saiu")
    else:
            print("Opção inválida")
def Acesso():
    print("Bem Vindo!")
Menu()
Acesso()