import unittest
from banco import Cliente, ContaCorrente, Deposito, Saque


class TestesIntegracao(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente('Endereco ficticio')
        self.conta = ContaCorrente(self.cliente, 1, '0001', 500, 2)
        self.cliente.adicionar_conta(self.conta)

    def test_I01_cliente_transacao_conta_historico(self):
        self.cliente.realizar_transacao(self.conta, Deposito(200))
        self.cliente.realizar_transacao(self.conta, Saque(50))
        self.assertIs(self.cliente.contas[0], self.conta)
        self.assertEqual(self.conta.saldo, 150)
        self.assertEqual([type(t) for t in self.conta.historico.transacoes], [Deposito, Saque])
        self.assertEqual([t.valor for t in self.conta.historico.transacoes], [200, 50])

    def test_I02_recusa_nao_entra_no_historico(self):
        self.cliente.realizar_transacao(self.conta, Deposito(-10))
        self.cliente.realizar_transacao(self.conta, Saque(10))
        self.assertEqual(self.conta.saldo, 0)
        self.assertEqual(self.conta.historico.transacoes, [])

    def test_I03_limite_quantidade_usa_historico(self):
        self.cliente.realizar_transacao(self.conta, Deposito(100))
        for _ in range(3):
            self.cliente.realizar_transacao(self.conta, Saque(10))
        self.assertEqual(self.conta.saldo, 80)
        self.assertEqual(len(self.conta.historico.transacoes), 3)
