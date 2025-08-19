Como rodar o simulador

Requisitos:
- Python 3.8+
- Instalar dependências: pip install -r requirements.txt

Executar localmente:

# Como rodar o simulador

Este arquivo mostra os passos mínimos para executar o projeto no seu computador, sem termos técnicos difíceis.

Resumo rápido
- Use o Makefile para preparar o ambiente e rodar.
- A API fica em: http://127.0.0.1:8080/
- Tudo funciona sem sudo (sem privilégios de administrador).

Passo a passo

1) Preparar o projeto (uma vez)
Abra um terminal na pasta do projeto e rode:

```bash
make install
```

Isso cria um ambiente local e instala as dependências só para este projeto.

2) Iniciar a aplicação (server)
No terminal, rode:

```bash
make run
```

Deixe esse terminal aberto enquanto testa pelo navegador ou curl.

3) Testar uma simulação simples (uma execução)

- Pelo navegador: abra http://127.0.0.1:8080/ e coloque `n=1` (seed é opcional). Clique em Simular.
- Pelo terminal (curl, mostra JSON formatado):

```bash
curl -s -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -d '{"n":1,"seed":42}' http://127.0.0.1:8080/jogo/simular | python -m json.tool
```

4) Testar simulação em lote (várias execuções)

- Pelo terminal (JSON agregado):

```bash
curl -s -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -d '{"n":10,"seed":42}' http://127.0.0.1:8080/jogo/simular | python -m json.tool
```

- Para ver uma versão legível em HTML no navegador (salva e abre automaticamente):

```bash
curl -s -X POST -H 'Content-Type: application/json' -H 'Accept: text/html' \
  -d '{"n":10,"seed":42}' http://127.0.0.1:8080/jogo/simular -o /tmp/sim_result.html && xdg-open /tmp/sim_result.html >/dev/null 2>&1 &
```

5) Rodar via linha de comando (script local)

Também existe um atalho para rodar localmente sem HTTP:

```bash
make simulate N=1 SEED=42
# ou para lote
make simulate N=1000 SEED=123
```

6) Rodar os testes

```bash
make test
```
