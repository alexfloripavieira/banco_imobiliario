# prompt_engineering — Instruções rápidas

Resumo rápido: este repositório contém uma pequena API HTTP (FastAPI) que expõe o uso do jogo.

Requisitos
- Ubuntu/Debian (instruções abaixo). Python 3.12.

Passos de setup (recomendado)

1) Instale dependências do sistema (necessárias para compilar extensões nativas como pycairo/reportlab):

```bash
sudo apt update
sudo apt install -y pkg-config libcairo2-dev libgirepository1.0-dev python3-dev build-essential
```

2) Use o `Makefile` para criar um ambiente virtual, instalar dependências Python e rodar a aplicação:

```bash
# cria .venv, instala pacotes e inicia a aplicação
make run

# ou para só instalar deps
make install

# iniciar uvicorn diretamente (usa .venv automaticamente)
make uvicorn
```

Observações
- O `Makefile` cria um ambiente virtual em `.venv` e usa o pip/pythond desse venv — assim a execução fica isolada do Python do sistema.
- Se a instalação falhar por falta de bibliotecas do sistema, execute `make system-deps` para ver a instrução de instalação dos pacotes do SO.

Alternativa (se você não puder instalar pacotes do sistema)
- Se `reportlab` não for necessário para seu fluxo, considere removê-lo de `requirements.txt` para evitar compilar dependências nativas.

Como desenvolver
- Testes: `make test` (roda pytest dentro do `.venv`).
- Lint: `make lint`.
- Typecheck: `make typecheck`.

Execução local
- A API roda por padrão em `http://0.0.0.0:8080` quando iniciada com `make run`.

Se quiser, posso adicionar instruções mais detalhadas ou um script `dev.sh` para automatizar mais passos.
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
# prompt_engineering — Guia para iniciantes

Este repositório contém uma pequena API (FastAPI) e um pequeno CLI para
simular um jogo de compra de propriedades com 4 estratégias diferentes.
Este guia mostra, de forma simples, como executar simulações individuais e
em lote, tanto via terminal quanto via navegador/HTTP.

Pré-requisitos
- Sistema: Debian/Ubuntu (instruções de instalação de pacotes do sistema
  incluídas). Funciona em outras distribuições com os pacotes equivalentes.
- Python 3.12 (ou >=3.8).

Instalação (passo a passo)

1) (Opcional) Dependências do sistema

O projeto originalmente listava `reportlab`, que precisa de bibliotecas do
sistema para compilar. Para permitir execução sem sudo em máquinas que não
podem instalar pacotes do sistema, removemos `reportlab` de
`requirements.txt`. Assim você pode rodar tudo sem privilégios de root.

2) Use o Makefile para criar ambiente virtual e instalar dependências Python:

```bash
make install
```

3) Inicie a API:

```bash
make run
```

Como executar simulações

Simulação única (via HTTP)
- Abra o navegador em `http://127.0.0.1:8080/`, preencha `n=1` e clique em
  Simular. O resultado aparecerá formatado na página.
- Ou com curl:

```bash
curl -s -X POST http://127.0.0.1:8080/jogo/simular \
  -H "Content-Type: application/json" \
  -d '{"n":1, "seed":42}' | jq
```

Simulação única (via CLI)

```bash
make simulate N=1 SEED=42
# ou
.venv/bin/python scripts/run_simulation.py -n 1 --seed 42
```

Simulação em lote (via HTTP) — agregado JSON ou HTML legível

```bash
# JSON (agregado)
curl -s -X POST http://127.0.0.1:8080/jogo/simular \
  -H "Content-Type: application/json" \
  -d '{"n":1000, "seed":123}' | jq

# HTML (mais legível) - salve e abra no navegador
curl -s -X POST http://127.0.0.1:8080/jogo/simular \
  -H "Content-Type: application/json" \
  -H "Accept: text/html" \
  -d '{"n":1000, "seed":123}' -o resultado.html
xdg-open resultado.html
```

Simulação em lote (via CLI) — resumo humano + JSON

```bash
make simulate N=1000 SEED=123
```

O que você verá
- Simulação única: JSON com `vencedor`, `jogadores` (ordem por saldo) e
  `rodadas`.
- Simulação em lote: JSON agregado com `simulacoes`, `vitorias`, `percentuais`
  e `media_rodadas`. Se pedir HTML, verá uma tabela amigável.

Comandos úteis
- `make install` — cria `.venv` e instala requisitos.
- `make run` — inicia a API.
- `make uvicorn` — inicia uvicorn (usa `.venv`).
- `make simulate N=<n> SEED=<seed>` — executa simulação via CLI.
- `make test` — executa testes (pytest).

