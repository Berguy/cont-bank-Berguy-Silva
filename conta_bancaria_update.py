import os
import time
import textwrap
from datetime import datetime


usuarios = []
contas = []
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
LIMITE_DIARIO = 1500
valor_sacado_hoje = 0
quantidade_transacao = 0
TRANSACAO_DIA = 10
data_da_ultima_transaco = None
AGENCIA = "0001"

# Utilitários:

def limpa_aguarda():
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')


def limpa_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def data_hora():
    return datetime.now().strftime('%d/%m/%Y %H:%M')


def reset_limite():
    global numero_saques, valor_sacado_hoje, quantidade_transacao, data_da_ultima_transaco
    hoje = datetime.now().date()
    if data_da_ultima_transaco != hoje:
        numero_saques = 0
        valor_sacado_hoje = 0
        quantidade_transacao = 0
        data_da_ultima_transaco = hoje

# Operações:

def sacar(*, valor_saque, saldo, extrato, numero_saques, limite, valor_sacado_hoje):
    if valor_saque > saldo:
        return saldo, extrato, "Falha na operação! SALDO INSUFICIENTE."
    elif valor_saque > limite:
        return saldo, extrato, "Operação não permitida! VALOR DO SAQUE É EXCEDENTE AO LIMITE DIÁRIO!"
    elif numero_saques >= LIMITE_SAQUES:
        return saldo, extrato, "Falha na operação. NÚMERO DE SAQUES DIÁRIOS EXCEDIDO."
    elif valor_sacado_hoje + valor_saque > LIMITE_DIARIO:
        return saldo, extrato, "Operação falhou! O valor já sacado hoje excede o limite diário de R$ 1.500,00."
    elif valor_saque <= 0:
        return saldo, extrato, "Falha na operação! O valor informado é inválido."
    
    saldo -= valor_saque
    extrato += f'Operação de saque. Valor: R$ {valor_saque:.2f} {data_hora()}\n'
    return saldo, extrato, f"Saque realizado com sucesso! Valor R$ {valor_saque:.2f} {data_hora()}"

def depositar(valor_deposito, saldo, extrato):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f'Operação de depósito. Valor: R$ {valor_deposito:.2f} {data_hora()}\n'
        return saldo, extrato, f"Depósito realizado com sucesso! Valor R$ {valor_deposito:.2f} {data_hora()}"
    
    else:
        return saldo, extrato, "Falha na operação! O valor informado é inválido."

def exibir_extrato(saldo, *, extrato):
    extrato_msg = "\n================ EXTRATO ================\n"
    extrato_msg += "Sem movimentações." if not extrato else extrato
    extrato_msg += f"\nSaldo: R$ {saldo:.2f} {data_hora()}\n"
    extrato_msg += "==========================================\n"
    return extrato_msg

# Novas funções solicitadas:

def criar_usuario(nome, data_nascimento, cpf, endereco):
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    for usuario in usuarios:
        if usuario["cpf"] == cpf_limpo:
            return "Usuário já cadastrado!"
    
    novo_usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf_limpo, "endereco": endereco}
    usuarios.append(novo_usuario)
    return "Usuário criado com sucesso!"

def criar_conta(cpf):
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    for usuario in usuarios:
        if usuario["cpf"] == cpf_limpo:
            numero_conta = len(contas) + 1
            nova_conta = {"agencia": AGENCIA, "numero_conta": numero_conta, "usuario": usuario}
            contas.append(nova_conta)
            return f"Conta criada com sucesso! Agência: {AGENCIA}, Número da conta: {numero_conta}"
    return "Usuário não encontrado! Não foi possível criar a conta."

def listar_contas():
    if not contas:
        return "Nenhuma conta cadastrada."
    
    contas_msg = "\n================ CONTAS ================\n"
    for conta in contas:
        contas_msg += (f"Agência: {conta['agencia']} - Conta: {conta['numero_conta']} - "
                       f"Titular: {conta['usuario']['nome']}\n")
    contas_msg += "==========================================\n"
    return contas_msg

#  Função primária:

def main():
    global saldo, extrato, numero_saques, valor_sacado_hoje, quantidade_transacao
    
    while True:
        reset_limite()

        if quantidade_transacao >= TRANSACAO_DIA:
            print('Você atingiu o limite de transações do dia.\nTente novamente amanhã')
            limpa_aguarda()
            break

        menu = """\n
|------ BANCO PROGRESSO ------|        
|\t[1] Depositar         |
|\t[2] Sacar             |
|\t[3] Extrato           |
|\t[4] Criar Usuário     |
|\t[5] Criar Conta       |
|\t[6] Listar Contas     |
|\t[7] Sair              |
|-----------------------------|

Digite um número para iniciar o serviço.
=> """
        escolha = input(menu)

        if escolha == '1':

            limpa_tela()

            valor_deposito = float(input('Informe o valor a ser depositado!\n'))

            limpa_tela()

            saldo, extrato, mensagem = depositar(valor_deposito, saldo, extrato)

            print(mensagem)

            limpa_aguarda()

            quantidade_transacao += 1

        elif escolha == '2':

            limpa_tela()

            valor_saque = float(input('Informe o valor a ser sacado:\n'))

            limpa_tela()

            saldo, extrato, mensagem = sacar(

                valor_saque=valor_saque,
                saldo=saldo,
                extrato=extrato,
                numero_saques=numero_saques,
                limite=limite,
                valor_sacado_hoje=valor_sacado_hoje
            )
            print(mensagem)

            limpa_aguarda()

            if "Saque realizado com sucesso" in mensagem:
                numero_saques += 1
                valor_sacado_hoje += valor_saque
                quantidade_transacao += 1

        elif escolha == '3':

            limpa_tela()

            print(exibir_extrato(saldo, extrato=extrato))

            sair = input('Deseja encerrar? (S/N)\n')

            if sair.lower() == 's':

                limpa_tela()

                break
            else:

                limpa_tela()

        elif escolha == '4':

            limpa_tela()

            nome = input("Informe o nome do usuário:\n")

            limpa_tela()

            data_nascimento = input("Informe a data de nascimento (dd/mm/yyyy):\n")

            limpa_tela()

            cpf = input("Informe o CPF (somente números):\n")

            limpa_tela()

            endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF):\n")

            limpa_tela()

            mensagem = criar_usuario(nome, data_nascimento, cpf, endereco)

            print(mensagem)
            
            limpa_aguarda()

        elif escolha == '5':

            limpa_tela()

            cpf = input("Informe o CPF do usuário (somente números):\n")

            limpa_tela()

            mensagem = criar_conta(cpf)

            print(mensagem)

            limpa_aguarda()

        elif escolha == '6':

            limpa_tela()

            print(listar_contas())

            limpa_aguarda()

        elif escolha == '7':

            limpa_tela()

            print('Obrigado por utilizar os nossos serviços!')

            limpa_aguarda()

            break

        else:

            limpa_tela()

            print('Por favor, digite apenas o número que corresponde à operação desejada!')

            limpa_aguarda()

# Executar:

if __name__ == "__main__":
    main()
