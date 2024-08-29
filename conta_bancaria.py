import os
import time
from datetime import datetime

def limpa_aguarda():
    time.sleep(3)
    os.system('cls')


def limpa_tela():
    os.system('cls')


def data_hora():
    data_hora_atual = datetime.now()

    data_hora_formatada = data_hora_atual.strftime('%d/%m/%Y %H:%M')
    
    return data_hora_formatada


def ocorrencia():
    return data_hora()


menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
LIMITE_DIARIO = 1500
valor_sacado_hoje = 0

while True:

    escolha = input(menu)

    if escolha > '0' and escolha < '5':

        if escolha == '1':
            
            limpa_tela()

            valor_deposito = float(input('Informe o valor a ser depositado!\n'))

            limpa_tela()
            
            if valor_deposito > 0:
                
                saldo += valor_deposito

                extrato += f'Operação de depósito. Valor: R$ {valor_deposito:.2f}\n'
                
            print(f'Depósito realizado como seucesso!\nValor R${valor_deposito:.2f} {ocorrencia()}')

            limpa_aguarda()


        elif escolha =='2':

            limpa_tela()

            valor_saque = float(input('Informe o valor a ser sacado:\n'))

            limpa_tela()

            valida_saldo = valor_saque > saldo
                 
            valida_limite = valor_saque > limite

            valida_saques = numero_saques >= LIMITE_SAQUES

            valida_limite_dia = valor_sacado_hoje + valor_saque > LIMITE_DIARIO

            if valida_saldo:
                limpa_tela()

                print('Falha na operação!\nSALDO INSUFUCIENTE PARA PARA SACAR ESTA IMPORTÂNCIA')

                limpa_aguarda()

            elif valida_limite:

                limpa_tela()

                print('Operação não permitida!\nVALOR DO SAQUE É EXCEDENTE AO LIMITE DIÁRIO!')

                limpa_aguarda()

            elif valida_saques:

                limpa_tela()

                print('Falha na operação.\nNÚMERO DE SAQUES DIÁRIOS EXCEDIDO.')

                limpa_aguarda()

            elif valida_limite_dia:

                limpa_tela()

                print('Operação falhou!\nOvalorjá sacado hoje excede o limite diário de R$ 1.500,00')

                limpa_aguarda()


            elif valor_saque > 0:
                saldo -= valor_saque


                extrato += f'Operação de saque. Valor: R$ {valor_saque:.2f}\n'

                print(f'Saque realizado como seucesso!\nValor R${valor_saque:.2f} {ocorrencia()}')

                limpa_aguarda()


            else:

                limpa_tela()

                print('Falha na operação! O valor informado é iválido.')

                limpa_aguarda()

        elif escolha =='3':

            limpa_tela()

            print("\n================ EXTRATO ================")
            print("Sem movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")

            sair = input('Deseja encerrar? (S/N)\n')

            limpa_tela()

            if not sair in ('s','S'):
                break



        elif escolha =='4':
            print('Obrigado por utilizar os nossos serviços!')
            limpa_aguarda()
            break

    else:
       limpa_tela()

       print('Por favor, digite apenas o número que corresponde a operação desejada!')

    limpa_aguarda() 
