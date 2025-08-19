"""HTTP interface exposing the game simulation via FastAPI.

Provides:
- POST /jogo/simular : JSON input, returns JSON or HTML based on Accept header
- GET / : form + query-based invocation, returns HTML
"""

from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ..usecases.game import simulate_games

app = FastAPI()


class SimulationRequest(BaseModel):
    n: int = 1
    seed: Optional[int] = None


def _render_batch_html(sim, title: str = "Resultado da Simulação (batch)") -> str:
    wins = sim.get("vitorias", {})
    perc = sim.get("percentuais", {})
    avg_str = sim.get("media_rodadas_str") or str(sim.get("media_rodadas"))
    rows = "".join(
        f"<tr><td>{k}</td><td>{wins.get(k, 0)}</td><td>{perc.get(k, 0):.2f}%</td></tr>"
        for k in wins
    )
    return f"""
    <html>
        <head>
            <meta charset='utf-8'>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background:#f6f8fa; color:#111 }}
                .container {{ max-width:900px; margin:24px auto; background:#fff; padding:18px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.08); }}
                table {{ border-collapse:collapse; width:100%; margin-top:12px }}
                table th, table td {{ border:1px solid #ddd; padding:8px; text-align:left }}
                a.button {{ display:inline-block; margin-top:12px; padding:8px 12px; background:#0366d6; color:#fff; text-decoration:none; border-radius:4px }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{title}</h1>
                <p>Simulações: {sim.get("simulacoes")}</p>
                <p>Seed: {sim.get("seed")}</p>
                <p>Média de rodadas: {avg_str}</p>
                <table>
                    <thead><tr><th>Estratégia</th><th>Vitórias</th><th>Percentual</th></tr></thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
                <a class="button" href="/">Voltar</a>
            </div>
        </body>
    </html>
    """


def _render_single_html(sim, title: str = "Resultado da Simulação") -> str:
    vencedor = sim.get("vencedor")
    jogadores = sim.get("jogadores", [])
    rodadas_str = sim.get("rodadas_str") or str(sim.get("rodadas"))
    return f"""
    <html>
        <head>
            <meta charset='utf-8'>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; background:#f6f8fa; color:#111 }}
                .container {{ max-width:700px; margin:24px auto; background:#fff; padding:18px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.08); }}
                h1 {{ margin-top:0 }}
                .meta p {{ margin:6px 0 }}
                a.button {{ display:inline-block; margin-top:12px; padding:8px 12px; background:#0366d6; color:#fff; text-decoration:none; border-radius:4px }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{title}</h1>
                <div class="meta">
                    <p><strong>Vencedor:</strong> {vencedor}</p>
                    <p><strong>Jogadores:</strong> {", ".join(jogadores)}</p>
                    <p><strong>Rodadas:</strong> {rodadas_str}</p>
                </div>
                <a class="button" href="/">Voltar</a>
            </div>
        </body>
    </html>
    """


@app.post("/jogo/simular")
async def simular(req: SimulationRequest, request: Request):
    """Simula o jogo n vezes com parâmetros passados no corpo da requisição.

    Exemplo de corpo: {"n": 1000, "seed": 123}
    """
    result = simulate_games(n=req.n, seed=req.seed)

    # negociação por header Accept
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        if isinstance(result, dict) and result.get("simulacoes", 0) > 1:
            return HTMLResponse(content=_render_batch_html(result))
        return HTMLResponse(content=_render_single_html(result))

    return result


@app.get("/", response_class=HTMLResponse)
async def index(n: Optional[int] = 0, seed: Optional[int] = None):
    """Simple HTML page: form to submit simulation or render result when query params provided.

    Example: GET /?n=1&seed=42
    """
    if n and n > 0:
        res = simulate_games(n=n, seed=seed)
        if isinstance(res, dict) and res.get("simulacoes", 0) > 1:
            return HTMLResponse(content=_render_batch_html(res))
        return HTMLResponse(content=_render_single_html(res))

    # form
    html = """
    <html>
        <head><meta charset='utf-8'><title>Simular Jogo</title></head>
        <body>
            <h1>Simular Jogo</h1>
            <form method="get" action="/">
                <label>n (número de simulações): <input name="n" value="1"></label><br>
                <label>seed (opcional): <input name="seed" value=""></label><br>
                <button type="submit">Simular</button>
            </form>
            <p>Ou envie POST JSON para <code>/jogo/simular</code></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html)
