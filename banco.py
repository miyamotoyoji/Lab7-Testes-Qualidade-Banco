from abc import ABC, abstractmethod
from datetime import date, datetime


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)


class Conta:
    def __init__(self, cliente, numero, agencia):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero, agencia):
        return cls(cliente, numero, agencia)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("Operação falhou: valor inválido.")
            return False
        if valor > self._saldo:
            print("Operação falhou: saldo insuficiente.")
            return False
        self._saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Operação falhou: valor inválido.")
            return False
        self._saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite, limite_saques):
        super().__init__(cliente, numero, agencia)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = sum(
            1 for t in self.historico.transacoes if isinstance(t, Saque)
        )
        if valor > self._limite:
            print("Operação falhou: valor excede o limite por saque.")
            return False
        if numero_saques >= self._limite_saques:
            print("Operação falhou: limite de saques excedido.")
            return False
        return super().sacar(valor)


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento


def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Digite um número válido.")


def ler_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_data(mensagem):
    while True:
        try:
            return datetime.strptime(input(mensagem), "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")


def buscar_cliente(clientes, cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def buscar_conta(clientes):
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente(clientes, cpf)
    if cliente is None:
        print("Cliente não encontrado.")
        return None
    if not cliente.contas:
        print("Cliente não possui contas.")
        return None
    numero = ler_int("Número da conta: ")
    for conta in cliente.contas:
        if conta.numero == numero:
            return cliente, conta
    print("Conta não encontrada.")
    return None


def cadastrar_cliente(clientes):
    cpf = input("CPF: ")
    if buscar_cliente(clientes, cpf):
        print("Já existe cliente com esse CPF.")
        return
    nome = input("Nome: ")
    data_nascimento = ler_data("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço: ")
    clientes.append(PessoaFisica(cpf, nome, data_nascimento, endereco))
    print("Cliente cadastrado.")


def criar_conta(clientes):
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente(clientes, cpf)
    if cliente is None:
        print("Cliente não encontrado.")
        return
    numero = ler_int("Número da conta: ")
    agencia = input("Agência: ")
    limite = ler_float("Limite por saque: ")
    limite_saques = ler_int("Limite de saques: ")
    conta = ContaCorrente(cliente, numero, agencia, limite, limite_saques)
    cliente.adicionar_conta(conta)
    print("Conta criada.")


def depositar(clientes):
    resultado = buscar_conta(clientes)
    if resultado is None:
        return
    cliente, conta = resultado
    valor = ler_float("Valor do depósito: ")
    cliente.realizar_transacao(conta, Deposito(valor))


def sacar(clientes):
    resultado = buscar_conta(clientes)
    if resultado is None:
        return
    cliente, conta = resultado
    valor = ler_float("Valor do saque: ")
    cliente.realizar_transacao(conta, Saque(valor))


def extrato(clientes):
    resultado = buscar_conta(clientes)
    if resultado is None:
        return
    _, conta = resultado
    print(f"Agência: {conta.agencia} | Conta: {conta.numero}")
    if not conta.historico.transacoes:
        print("Nenhuma transação realizada.")
    for t in conta.historico.transacoes:
        print(f"{type(t).__name__}: R$ {t.valor:.2f}")
    print(f"Saldo: R$ {conta.saldo:.2f}")


def main():
    clientes = []
    while True:
        print("\n1 - Cadastrar cliente")
        print("2 - Criar conta corrente")
        print("3 - Depositar")
        print("4 - Sacar")
        print("5 - Extrato")
        print("0 - Sair")
        opcao = input("Opção: ")
        if opcao == "1":
            cadastrar_cliente(clientes)
        elif opcao == "2":
            criar_conta(clientes)
        elif opcao == "3":
            depositar(clientes)
        elif opcao == "4":
            sacar(clientes)
        elif opcao == "5":
            extrato(clientes)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()