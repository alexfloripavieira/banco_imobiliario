"""Game engine / use case: simulate single or multiple games and aggregate statistics."""

import random
from random import Random
from typing import Any, Dict, List, Optional, Tuple

from ..adapters.strategies import STRATEGIES
from ..domain.models import Player, Property


from ..domain.constants import (
    BASE_PROPERTY_PRICE, BASE_RENT, BOARD_SIZE, LAP_BONUS, MAX_ROUNDS,
    PRICE_MULTIPLIER, RENT_MULTIPLIER
)

class Game:
    def __init__(self, rng: Optional[Random] = None):
        self.board: List[Property] = []
        self.players: List[Player] = []
        self.maxRounds = MAX_ROUNDS
        self.rng = rng or random.Random()

    def setup(self):
        self.board = [Property(pos, BASE_PROPERTY_PRICE + pos * PRICE_MULTIPLIER, BASE_RENT + pos * RENT_MULTIPLIER) for pos in range(BOARD_SIZE)]

    def createPlayers(self):
        order = ["impulsivo", "exigente", "cauteloso", "aleatorio"]
        self.rng.shuffle(order)
        self.players = [Player(name=s, strategy=s) for s in order]

    def getActivePlayers(self) -> List[Player]:
        return [p for p in self.players if p.active]

    def simulate(self) -> Tuple[str, List[str], int]:
        self.initializeGame()
        return self.runSimulation()

    def initializeGame(self) -> None:
        self.setup()
        self.createPlayers()

    def runSimulation(self) -> Tuple[str, List[str], int]:
        roundCount = 0
        
        while roundCount < self.maxRounds and len(self.getActivePlayers()) > 1:
            roundCount += 1
            for player in self.players:
                if not player.active:
                    continue

                steps = self.rng.randint(1, 6)
                completed = player.move(steps, BOARD_SIZE)
                if completed:
                    player.receive(LAP_BONUS)

                prop = self.board[player.position]
                if prop.owner is None:
                    strategy = STRATEGIES[player.strategy]
                    if player.balance >= prop.price and strategy(player, prop):
                        player.buy(prop)
                elif prop.owner is not player:
                    player.pay(prop.rent)
                    prop.owner.receive(prop.rent)
                    if not player.active:
                        player.releaseProperties()

                if len(self.getActivePlayers()) == 1:
                    break

        return self.determineWinner(roundCount)

    def determineWinner(self, roundCount: int) -> Tuple[str, List[str], int]:
        active = self.getActivePlayers()
        if len(active) == 1:
            winner = active[0]
        else:
            sortedPlayers = sorted(self.players, key=lambda p: p.balance, reverse=True)
            winner = sortedPlayers[0]

        ranking = sorted(self.players, key=lambda p: p.balance, reverse=True)
        return winner.strategy, [p.strategy for p in ranking], roundCount


def simulateGames(n: int = 1, seed: Optional[int] = None) -> Dict[str, Any]:
    """Run n simulations and return aggregated statistics.

    If n == 1 returns a single-run style result similar to original API.
    If n > 1 returns aggregated stats: win counts, percentages and average rounds.
    """
    seeds = []
    base_rng = random.Random(seed)
    results = []
    for _ in range(n):
        s = base_rng.randint(0, 2**32 - 1)
        seeds.append(s)
        g = Game(rng=random.Random(s))
        winner, ranking, rounds = g.simulate()
        results.append({"winner": winner, "ranking": ranking, "rounds": rounds})

    if n == 1:
        r = results[0]
        return {
            "vencedor": r["winner"],
            "jogadores": r["ranking"],
            "rodadas": r["rounds"],
            "rodadas_str": f"{r['rounds']} rodadas",
        }

    wins: Dict[str, int] = {k: 0 for k in STRATEGIES.keys()}
    total_rounds = 0
    for r in results:
        wins[r["winner"]] = wins.get(r["winner"], 0) + 1
        total_rounds += r["rounds"]

    percentages = {k: (wins[k] / n) * 100 for k in wins}
    avg_rounds = total_rounds / n if n else 0
    media_rodadas_str = f"{avg_rounds:.3f} rodadas"

    return {
        "simulacoes": n,
        "seed": seed,
        "vitorias": wins,
        "percentuais": percentages,
        "media_rodadas": avg_rounds,
        "media_rodadas_str": media_rodadas_str,
    }


def simulateGame() -> dict:
    return simulateGames(1, None)
