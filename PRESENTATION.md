Apresentação técnica — Simulador de Jogo (Banco Imobiliário simplificado)
=====================================================================

É um simulador inspirado em Banco Imobiliário. O código roda localmente e
compara quatro estratégias de compra de propriedades usando simulações.
Você pode pedir uma simulação única (n=1) ou muitas simulações (n>1) e ver
um resumo com vitórias, percentuais e média de rodadas.

  ```bash
  make install   # prepara o ambiente (só uma vez)
  make run       # inicia a API em http://127.0.0.1:8080/
  ```

  ```bash
  curl -s -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
    -d '{"n":1,"seed":42}' http://127.0.0.1:8080/jogo/simular | python3 -m json.tool
  ```

  ```bash
  curl -s -X POST -H 'Content-Type: application/json' -H 'Accept: text/html' \
    -d '{"n":1000,"seed":123}' http://127.0.0.1:8080/jogo/simular -o /tmp/sim.html && xdg-open /tmp/sim.html
  ```

Estrutura do código
---------------------------------
- `src/domain`: modelos centrais (Player, Property).
- `src/adapters`: regras de decisão (estratégias).
- `src/usecases`: motor da simulação (`Game`, `simulate_games`).
- `src/interfaces`: API (FastAPI) e HTML de visualização.

```bash
curl -s -X POST http://127.0.0.1:8080/jogo/simular \
  -H 'Content-Type: application/json' -d '{"n":1, "seed":42}' | python3 -m json.tool
```

Simulação em lote (HTML legível):

```bash
curl -s -X POST http://127.0.0.1:8080/jogo/simular \
  -H 'Content-Type: application/json' -H 'Accept: text/html' \
  -d '{"n":1000, "seed":123}' -o /tmp/sim.html && xdg-open /tmp/sim.html
```


