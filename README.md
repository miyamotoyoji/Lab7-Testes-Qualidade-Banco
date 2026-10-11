# Laboratório - Testes e Qualidade de Software

Atividades 6.1-6.5 do PDF, correspondentes a 7.1-7.5 no Moodle.

## Executar
Requer Python 3; não há dependências externas.
```
python banco.py
python -m unittest discover -s tests -v
python executar_testes.py depois
```
No PyCharm, abra esta pasta como projeto e selecione um interpretador Python 3 existente. Execute banco.py ou os testes.

## Origem e evolução
Base copiada de [Execicio_5.4](https://github.com/miyamotoyoji/Execicio_5.4), commit cbeaad1a0db241f9407f4148c674867992af023c. O arquivo Ex5.4.py foi renomeado para banco.py para permitir importação nos testes.
- 0ff15d3: sistema original e 13 testes executados antes da alteração.
- eb61a78: poupança e 8 novos testes, com os 13 anteriores novamente aprovados.
- Documentação e evidências complementares em docs/ e resultados/.

## Poupança
Menu 6 transfere saldo disponível da conta corrente para a reserva de poupança. Menu 7 resgata para a mesma conta. O extrato mostra ambas as posições e as transações. Não consome limite de saque e não permite valores não positivos, não finitos ou acima do saldo de origem.
Decisão de escopo: reserva e resgate, sem rendimento automático, pois o enunciado não define taxa nem período. Estado em memória; valores float herdados do exercício; não representa sistema bancário de produção. Limite de saques acumulado no histórico, conforme a base, sem reinício diário. As validações de depósito/saque originais foram preservadas, inclusive suas limitações; os testes não demonstram ausência de todos os defeitos.

## Resultado real
Antes: 6 unitários + 3 de integração + 4 funcionais = 13 aprovados.
Depois: os mesmos 13 + 8 de poupança = 21 aprovados. Zero falhas, erros ou ignorados.
Logs registram data UTC e versão de Python. Testes funcionais abrem subprocessos reais com entradas de terminal e verificam saída e encerramento normal.

## Entregas
- docs/7.1_Roteiro.md
- docs/7.2_Unitario.md, tests/test_unitario.py e respectivos logs.
- docs/7.3_Integracao.md, tests/test_integracao.py e respectivos logs.
- docs/7.4_Funcional.md, tests/test_funcional.py e respectivos logs.
- docs/7.5_Regressao.md, implementação e suíte completa.
