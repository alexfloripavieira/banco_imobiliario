"""Game engine / use case: simulate single or multiple games and aggregate statistics."""

import random
from random import Random
from typing import Any, Dict, List, Optional, Tuple

from ..adapters.strategies import STRATEGIES
from ..domain.models import Player, Property


class Game:
    def __init__(self, rng: Optional[Random] = None):
        self.board: List[Property] = []
        self.players: List[Player] = []
        self.max_rounds = 1000
        self.rng = rng or random.Random()

    def setup(self):
        self.board = [Property(pos, 100 + pos * 10, 10 + pos * 5) for pos in range(20)]

    def create_players(self):
        order = ["impulsivo", "exigente", "cauteloso", "aleatorio"]
        self.rng.shuffle(order)
        self.players = [Player(name=s, strategy=s) for s in order]

    def active_players(self) -> List[Player]:
        return [p for p in self.players if p.active]

    def simulate(self) -> Tuple[str, List[str], int]:
        self.setup()
        self.create_players()
        round_count = 0

        while round_count < self.max_rounds and len(self.active_players()) > 1:
            round_count += 1
            for player in self.players:
                if not player.active:
                    continue

                steps = self.rng.randint(1, 6)
                completed = player.move(steps, len(self.board))
                if completed:
                    player.receive(100)

                prop = self.board[player.position]
                if prop.owner is None:
                    strategy = STRATEGIES[player.strategy]
                    if player.balance >= prop.price and strategy(player, prop):
                        player.buy(prop)
                elif prop.owner is not player:
                    player.pay(prop.rent)
                    prop.owner.receive(prop.rent)
                    if not player.active:
                        player.release_properties()

                if len(self.active_players()) == 1:
                    break

        active = self.active_players()
        if len(active) == 1:
            winner = active[0]
        else:
            sorted_players = sorted(self.players, key=lambda p: p.balance, reverse=True)
            winner = sorted_players[0]

        ranking = sorted(self.players, key=lambda p: p.balance, reverse=True)
        return winner.strategy, [p.strategy for p in ranking], round_count


def simulate_games(n: int = 1, seed: Optional[int] = None) -> Dict[str, Any]:
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


def simulate_game() -> dict:
    return simulate_games(1, None)
