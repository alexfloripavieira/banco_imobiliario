Apresentação técnica — Simulador de Jogo (Banco Imobiliário simplificado)
=====================================================================

Objetivo
--------
Apresentar a implementação do simulador de jogo, a arquitetura (Clean
Architecture), principais classes e tipagens, fluxos e decisões de design —
material preparado para ser exposto a uma banca técnica para vaga de dev
sênior.

Sumário
-------
- Visão geral
- Arquitetura e separação de camadas
- Modelos / classes e responsabilidades
- Tipagens e contrato das funções
- Fluxo do caso de uso (simulação)
- Estratégias dos jogadores
- Testes, lint e qualidade
- Execução e considerações finais

Visão geral
-----------
O projeto implementa um simulador de um jogo de propriedades com regras
simplificadas inspiradas em Banco Imobiliário. O objetivo é comparar quatro
estratégias de compra de propriedades via simulação repetida e expor um
endpoint HTTP para disparar simulações.

Contrato da API
---------------
GET /jogo/simular?n=<int>&seed=<int?>
- n (int, default=1) — número de simulações a executar
- seed (int, opcional) — semente RNG para reprodutibilidade

Retorno (n==1):
{
  "vencedor": "<estrategia>",
  "jogadores": ["<ordem por saldo>"],
  "rodadas": <int>
}

Retorno (n>1): estatísticas agregadas — número de simulações, vitórias por
estratégia, percentuais e média de rodadas.

Arquitetura (Clean Architecture)
--------------------------------
Estrutura principal (módulos):

- src/domain — entidades puras do domínio
  - `Player`, `Property`
- src/adapters — adaptadores e implementações concretas
  - `strategies.py` — políticas de compra
- src/usecases — regras de orquestração / motor
  - `game.py` — `Game`, `simulate_games` / `simulate_game`
- src/interfaces — adaptadores de interface (FastAPI)
  - `api.py` — endpoint `/jogo/simular`
- main.py — entrypoint para executar com Uvicorn

Responsabilidades por camada
- Domain: modelos e comportamento mínimo (ex.: `Player.move`, `pay`,
  `buy`, `release_properties`).
- Adapters: implementação das estratégias de decisão (impulsivo,
  exigente, cauteloso, aleatório).
- Usecases: orquestra turnos, rolagem de dados, pagamentos, compra,
  encerramento por falência ou timeout, agregação de estatísticas.
- Interfaces: expõe caso de uso via HTTP sem lógica de domínio.

Modelos e classes
------------------
src/domain/models.py

- class Property:
  - position: int
  - price: int
  - rent: int
  - owner: Optional[Player]

- class Player:
  - name: str
  - strategy: str
  - balance: int = 300
  - position: int = 0
  - properties: List[Property]
  - active: bool

  Métodos:
  - move(steps: int, board_size: int) -> bool
  - pay(amount: int) -> None
  - receive(amount: int) -> None
  - buy(prop: Property) -> None
  - release_properties() -> None

Tipagens e contrato de funções
------------------------------
- Estratégias: Callable[[Player, Property], bool]
- Game.simulate() -> Tuple[str, List[str], int]
  (retorna vencedor, ranking e número de rodadas)
- simulate_games(n: int, seed: Optional[int]) -> Dict[str, Any]

Fluxo do caso de uso (alto nível)
---------------------------------
1. Inicializar tabuleiro (20 propriedades) e jogadores em ordem
   aleatória.
2. Repetir rodadas até 1000 ou 1 jogador restante:
   - Para cada jogador ativo:
     - rolar dado (1..6), mover, receber +100 se completar a volta
     - inspecionar propriedade: se sem dono, avaliar política e comprar
       se decidir; se com dono, pagar aluguel
     - se saldo < 0 => jogador eliminado e libera propriedades
3. Ao final, montar ranking por saldo; se timeout escolher maior saldo.

Estratégias implementadas
-------------------------
- impulsivo: compra sempre
- exigente: compra se aluguel > 50
- cauteloso: compra se reserva >= 80 após compra
- aleatorio: compra com probabilidade 50%

Qualidade e testes
------------------
- Testes unitários com pytest (cobrem estratégias e integração básica)
- Configurações iniciais para flake8 e mypy no repositório
- Makefile com alvos `test`, `lint`, `typecheck`, `run` para replicar
  validações localmente

Execução e reprodutibilidade
----------------------------
- Endpoint aceita `seed` para reprodutibilidade; as simulações usam uma
  RNG base para gerar sementes por jogo e criar RNGs por-jogo.

Decisões de arquitetura e trade-offs
-----------------------------------
- Simplicidade: valores do tabuleiro gerados programaticamente para
  evitar dados estáticos e focar na infra/arquitetura.
- Reprodutibilidade: `seed` exposto, cada jogo usa semente derivada para
  manter independência entre execuções.
- Testes: cobertura básica; expandir para cenários de falência e compra
  em cantos extremos é recomendável.

Slides / sugestões de apresentação
---------------------------------
1. Comece com o problema e contrato da API
2. Mostre diagrama de camadas (Domain / Adapters / Usecases /
   Interfaces)
3. Mostre 1-2 snippets-chave: `Player.buy`, `Game.simulate` (alta ordem)
4. Demonstre execução com `curl` ou via `python` (ex.: `simulate_games`)
5. Fale sobre testes e próximos passos

Exemplos de uso (curl)

Simulação única (exemplo usando POST JSON):

```bash
curl -s -X POST http://localhost:8080/jogo/simular \
  -H "Content-Type: application/json" \
  -d '{"n":1}'
```

Simulação em lote (1000 vezes, seed=123):

```bash
curl -s -X POST http://localhost:8080/jogo/simular \
  -H "Content-Type: application/json" \
  -d '{"n":1000, "seed":123}'
```

Para apresentação / demonstração ao público (guia para leigos)
---------------------------------------------------------------

Se você quiser demonstrar a aplicação para uma pessoa leiga, siga estes
passos simples e rápidos:

1) Preparar o ambiente (uma vez):

```bash
sudo apt update
sudo apt install -y pkg-config libcairo2-dev libgirepository1.0-dev python3-dev build-essential
make install
```

2) Iniciar a API:

```bash
make run
```

3) Demonstrar simulação individual:

 - Abra `http://127.0.0.1:8080/` no navegador, defina `n=1` e (opcional) `seed`.
 - Clique em Simular. Resultado em JSON aparecerá formatado na página.

4) Demonstrar simulação em lote:

 - No navegador, defina `n=1000` e `seed=123`, clique em Simular (ou envie POST com `Accept: text/html`).
 - A página exibirá uma tabela com as vitórias por estratégia e percentuais.

5) Alternativa rápida via terminal:

```bash
# resumo no terminal (CLI)
make simulate N=10 SEED=42

# JSON agregado
curl -s -X POST http://127.0.0.1:8080/jogo/simular -H "Content-Type: application/json" -d '{"n":1000, "seed":123}' | jq

# HTML legível (salve e abra)
curl -s -X POST http://127.0.0.1:8080/jogo/simular -H "Content-Type: application/json" -H "Accept: text/html" -d '{"n":1000, "seed":123}' -o result.html
xdg-open result.html
```

