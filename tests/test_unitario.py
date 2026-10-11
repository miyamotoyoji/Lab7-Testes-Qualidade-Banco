import unittest
from banco import Conta, ContaCorrente


class TestesUnitarios(unittest.TestCase):
    def test_U01_deposito_positivo(self):
        conta = Conta(None, 1, '0001')
        self.assertTrue(conta.depositar(100))
        self.assertEqual(conta.saldo, 100)

    def test_U02_deposito_invalido(self):
        for valor in (0, -10):
            with self.subTest(valor=valor):
                conta = Conta(None, 1, '0001')
                self.assertFalse(conta.depositar(valor))
                self.assertEqual(conta.saldo, 0)

    def test_U03_saque_valido(self):
        conta = Conta(None, 1, '0001')
        conta.depositar(100)
        self.assertTrue(conta.sacar(40))
        self.assertEqual(conta.saldo, 60)

    def test_U04_saque_sem_saldo(self):
        conta = Conta(None, 1, '0001')
        self.assertFalse(conta.sacar(1))
        self.assertEqual(conta.saldo, 0)

    def test_U05_limite_por_saque(self):
        conta = ContaCorrente(None, 1, '0001', 50, 3)
        conta.depositar(100)
        self.assertFalse(conta.sacar(51))
        self.assertTrue(conta.sacar(50))
        self.assertEqual(conta.saldo, 50)

    def test_U06_saque_invalido(self):
        for valor in (0, -10):
            with self.subTest(valor=valor):
                conta = Conta(None, 1, '0001')
                self.assertFalse(conta.sacar(valor))
                self.assertEqual(conta.saldo, 0)
