"""Executa testes reais e salva evidencias UTF-8 por etapa."""
from datetime import datetime, timezone
from pathlib import Path
import contextlib
import io
import json
import platform
import sys
import unittest

ROOT = Path(__file__).resolve().parent
etapa = sys.argv[1] if len(sys.argv) > 1 else 'depois'
if etapa not in ('antes', 'depois'):
    raise SystemExit('Use: python executar_testes.py antes|depois')
grupos = ['unitario', 'integracao', 'funcional']
if etapa == 'depois':
    grupos.append('poupanca')
resumo = []
for grupo in grupos:
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), pattern=f'test_{grupo}.py', top_level_dir=str(ROOT))
    registro = io.StringIO()
    registro.write(f'Etapa: {etapa}\nGrupo: {grupo}\nUTC: {datetime.now(timezone.utc).isoformat()}\nPython: {platform.python_version()}\n\n')
    with contextlib.redirect_stdout(registro):
        resultado = unittest.TextTestRunner(stream=registro, verbosity=2).run(suite)
    destino = ROOT / 'resultados' / f'{etapa}_{grupo}.txt'
    destino.write_text(registro.getvalue(), encoding='utf-8')
    resumo.append(dict(grupo=grupo, executados=resultado.testsRun, falhas=len(resultado.failures), erros=len(resultado.errors), ignorados=len(resultado.skipped)))
    print(f'{grupo}: {resultado.testsRun} testes; sucesso={resultado.wasSuccessful()}')
(ROOT / 'resultados' / f'{etapa}_resumo.json').write_text(json.dumps(resumo, indent=2), encoding='utf-8')
sys.exit(1 if any(r['falhas'] or r['erros'] or r['ignorados'] for r in resumo) else 0)
