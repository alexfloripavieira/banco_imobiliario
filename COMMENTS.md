Como rodar o simulador

Requisitos:
- Python 3.8+
- Instalar dependências: pip install -r requirements.txt

Executar localmente:

1. Instale dependências

```bash
pip install -r requirements.txt
```

2. Rode a aplicação

```bash
python main.py
```

3. Acesse o endpoint

GET http://localhost:8080/jogo/simular

Resposta de exemplo:

{
    "vencedor": "cauteloso",
    "jogadores": ["cauteloso", "aleatorio", "exigente", "impulsivo"]
}

Exemplos com curl

Simulação única (padrão) — enviar no body (JSON):

```bash
curl -s -X POST http://localhost:8080/jogo/simular \
  -H "Content-Type: application/json" \
  -d '{"n":1}'
```

Simulação em lote (1000 execuções) com seed reprodutível — enviar no body (JSON):

```bash
curl -s -X POST http://localhost:8080/jogo/simular \
  -H "Content-Type: application/json" \
  -d '{"n":1000, "seed":123}'
```

Simulações em lote e seed

- É possível executar múltiplas simulações e obter estatísticas usando query params `n` e `seed`.
- Exemplo: `GET /jogo/simular?n=1000&seed=123` retornará número de simulações, contagem de vitórias por estratégia, percentuais e média de rodadas.

Resposta de exemplo (n>1):
{
  "simulacoes": 1000,
  "seed": 123,
  "vitorias": {"impulsivo": 200, "exigente": 250, "cauteloso": 350, "aleatorio": 200},
  "percentuais": {"impulsivo": 20.0, "exigente": 25.0, "cauteloso": 35.0, "aleatorio": 20.0},
  "media_rodadas": 312.4
}

Comandos úteis com Makefile

Para facilitar, há um `Makefile` com alvos úteis:

- `make install` — instala dependências listadas em `requirements.txt`.
- `make test` — executa a suíte de testes (pytest).
- `make lint` — executa `flake8` (pode falhar se não instalado).
- `make typecheck` — executa `mypy` (pode falhar se não instalado).
- `make run` — executa `python3 main.py`.
- `make uvicorn` — executa o servidor uvicorn.

Exemplo rápido:

```bash
make install
make test
make run
```
