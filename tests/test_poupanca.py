import unittest
from banco import Cliente, ContaCorrente, Deposito, Saque, InvestimentoPoupanca, ResgatePoupanca
from tests.test_funcional import executar, CADASTRO, CONTA


class TestesPoupanca(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente('Endereco ficticio')
        self.conta = ContaCorrente(self.cliente, 1, '0001', 500, 1)
        self.cliente.adicionar_conta(self.conta)
        self.cliente.realizar_transacao(self.conta, Deposito(1000))

    def test_P01_investir_preserva_total(self):
        self.cliente.realizar_transacao(self.conta, InvestimentoPoupanca(600))
        self.assertEqual((self.conta.saldo, self.conta.saldo_poupanca), (400, 600))
        self.assertEqual(self.conta.saldo + self.conta.saldo_poupanca, 1000)
        self.assertIsInstance(self.conta.historico.transacoes[-1], InvestimentoPoupanca)

    def test_P02_valores_invalidos_nao_alteram_estado(self):
        for tipo in (InvestimentoPoupanca, ResgatePoupanca):
            for valor in (0, -1, float('nan'), float('inf'), -float('inf')):
                with self.subTest(tipo=tipo.__name__, valor=valor):
                    self.cliente.realizar_transacao(self.conta, tipo(valor))
                    self.assertEqual((self.conta.saldo, self.conta.saldo_poupanca), (1000, 0))
                    self.assertEqual(len(self.conta.historico.transacoes), 1)

    def test_P03_investimento_sem_saldo(self):
        self.cliente.realizar_transacao(self.conta, InvestimentoPoupanca(1001))
        self.assertEqual((self.conta.saldo, self.conta.saldo_poupanca), (1000, 0))
        self.assertEqual(len(self.conta.historico.transacoes), 1)

    def test_P04_resgate_parcial_e_total(self):
        self.cliente.realizar_transacao(self.conta, InvestimentoPoupanca(1000))
        self.cliente.realizar_transacao(self.conta, ResgatePoupanca(250))
        self.assertEqual((self.conta.saldo, self.conta.saldo_poupanca), (250, 750))
        self.cliente.realizar_transacao(self.conta, ResgatePoupanca(750))
        self.assertEqual((self.conta.saldo, self.conta.saldo_poupanca), (1000, 0))
        self.assertEqual(len(self.conta.historico.transacoes), 4)

    def test_P05_resgate_sem_saldo(self):
        self.cliente.realizar_transacao(self.conta, ResgatePoupanca(1))
        self.assertEqual((self.conta.saldo, self.conta.saldo_poupanca), (1000, 0))
        self.assertEqual(len(self.conta.historico.transacoes), 1)

    def test_P06_poupanca_nao_consume_limite_saque(self):
        self.cliente.realizar_transacao(self.conta, InvestimentoPoupanca(600))
        self.cliente.realizar_transacao(self.conta, ResgatePoupanca(600))
        self.cliente.realizar_transacao(self.conta, Saque(100))
        self.cliente.realizar_transacao(self.conta, Saque(100))
        self.assertEqual(self.conta.saldo, 900)
        self.assertEqual(sum(isinstance(t, Saque) for t in self.conta.historico.transacoes), 1)

    def test_P07_fluxo_funcional_poupanca(self):
        saida = executar(CADASTRO + CONTA + ['3', '00000000000', '1', '1000',
                         '6', '00000000000', '1', '600', '7', '00000000000', '1', '100',
                         '5', '00000000000', '1', '0'])
        for texto in ('InvestimentoPoupanca: R$ 600.00', 'ResgatePoupanca: R$ 100.00',
                      'Saldo: R$ 500.00', 'Poupança: R$ 500.00'):
            self.assertIn(texto, saida)

    def test_P08_isolamento_entre_contas(self):
        outra = ContaCorrente(self.cliente, 2, '0001', 500, 1)
        self.cliente.adicionar_conta(outra)
        self.cliente.realizar_transacao(self.conta, InvestimentoPoupanca(100))
        self.assertEqual((outra.saldo, outra.saldo_poupanca), (0, 0))
        self.assertEqual(outra.historico.transacoes, [])
