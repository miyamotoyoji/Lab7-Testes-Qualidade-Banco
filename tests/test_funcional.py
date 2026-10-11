import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CADASTRO = ['1', '00000000000', 'Cliente Teste', '01/01/2000', 'Endereco ficticio']
CONTA = ['2', '00000000000', '1', '0001', '500', '3']


def executar(entradas):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    resultado = subprocess.run([sys.executable, str(ROOT / 'banco.py')],
                               input='\n'.join(entradas) + '\n', capture_output=True,
                               text=True, encoding='utf-8', env=env, timeout=10)
    if resultado.returncode != 0:
        raise AssertionError(resultado.stderr)
    return resultado.stdout


class TestesFuncionais(unittest.TestCase):
    def test_F01_fluxo_completo_pelo_terminal(self):
        saida = executar(CADASTRO + CONTA + ['3', '00000000000', '1', '200',
                         '4', '00000000000', '1', '50', '5', '00000000000', '1', '0'])
        for texto in ('Cliente cadastrado.', 'Conta criada.', 'Deposito: R$ 200.00',
                      'Saque: R$ 50.00', 'Saldo: R$ 150.00'):
            self.assertIn(texto, saida)

    def test_F02_cliente_inexistente(self):
        saida = executar(['3', 'inexistente', '0'])
        self.assertIn('Cliente não encontrado.', saida)

    def test_F03_entrada_invalida_e_recuperacao(self):
        saida = executar(CADASTRO + CONTA + ['3', '00000000000', '1', 'abc', '10,50',
                         '5', '00000000000', '1', '0'])
        self.assertIn('Digite um número válido.', saida)
        self.assertIn('Saldo: R$ 10.50', saida)

    def test_F04_cpf_duplicado(self):
        saida = executar(CADASTRO + ['1', '00000000000', '0'])
        self.assertIn('Já existe cliente com esse CPF.', saida)
