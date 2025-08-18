"""HTTP interface exposing the game simulation via FastAPI."""

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from ..usecases.game import simulate_games

app = FastAPI()


class SimulationRequest(BaseModel):
    n: int = 1
    seed: Optional[int] = None


@app.post('/jogo/simular')
async def simular(req: SimulationRequest):
    """Simula o jogo n vezes com parâmetros passados no corpo da requisição.

    Exemplo de corpo: {"n": 1000, "seed": 123}
    """
    return simulate_games(n=req.n, seed=req.seed)
